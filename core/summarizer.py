from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from typing import List

def generate_summary(documents: List[Document], api_key: str, length: str = "Medium") -> str:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=api_key, 
        temperature=0.2
    )
    
    if length == "Short":
        structure_prompt = """
        Use this exact markdown structure:
        ## Document Overview
        A very concise 2-sentence description of the main topic.

        ## Key Takeaways
        - Limit to 3-5 most essential bullet points only.
        """
    elif length == "Medium":
        structure_prompt = """
        Use this exact markdown structure:
        ## Document Overview
        A 2-3 sentence description.

        ## Key Takeaways
        - 5 to 8 important bullet points.

        ## Glossary of Key Terms
        | Term | Definition |
        |------|------------|
        | Term | Brief Definition |
        (Include maximum 5 essential terms)
        """
    else: # Detailed
        structure_prompt = """
        Use this exact markdown structure:
        ## Document Overview
        A comprehensive overview of the document.

        ## Key Takeaways
        - 10+ detailed bullet points covering all major concepts.

        ## Glossary of Key Terms
        | Term | Definition |
        |------|------------|
        | Term | Detailed Definition |
        (Include all important technical terms)

        ## Important Sections
        List the most important sections with a brief description for each.
        """

    combined = "\n\n".join(
        f"[Page {d.metadata.get('page', '?')}]\n{d.page_content}" 
        for d in documents[:60]
    )

    prompt = f"""Analyze the following document thoroughly and produce a structured study guide.
    Return your response in the SAME language as the document (auto-detect Turkish or English).

    {structure_prompt}
    
    DOCUMENT:
    {combined[:12000]}"""
    
    response = llm.invoke(prompt)
    return response.content