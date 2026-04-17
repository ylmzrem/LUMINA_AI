from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.vectorstores import FAISS
from typing import List


SYSTEM_PROMPT = """You are Lumina AI, a personalized learning assistant.
You answer questions EXCLUSIVELY based on the provided document context.
Never use outside knowledge.

Rules:
- Always cite specific page numbers using [Page X] notation in your answer.
- If the answer is not in the document, say exactly: "This information is not found in the uploaded document."
- Detect the language of the question and respond in the SAME language (Turkish or English).
- For Turkish responses use [Sayfa X] notation instead of [Page X].

Document Context:
{context}"""


def _format_docs(docs) -> str:
    parts = []
    for doc in docs:
        page = doc.metadata.get("page", "?")
        parts.append(f"[Page {page}]\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def build_rag_chain(vector_store: FAISS, api_key: str):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.3,
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ])

    def retrieve_with_history(inputs: dict):
        question = inputs["question"]
        docs = retriever.invoke(question)
        return {
            "context": _format_docs(docs),
            "question": question,
            "chat_history": inputs.get("chat_history", []),
            "_source_docs": docs,
        }

    chain = (
        RunnableLambda(retrieve_with_history)
        | RunnablePassthrough.assign(
            answer=(prompt | llm | StrOutputParser())
        )
    )

    return chain
