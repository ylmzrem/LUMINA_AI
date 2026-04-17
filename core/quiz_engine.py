import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from typing import List


QUIZ_PROMPT = """Based on the following document, generate exactly {n} multiple-choice questions \
to test deep comprehension of the material.

IMPORTANT: Return ONLY a valid JSON array — no markdown fences, no extra text.

Each element must follow this exact schema:
{{
  "question": "Question text",
  "options": {{
    "A": "First option",
    "B": "Second option",
    "C": "Third option",
    "D": "Fourth option"
  }},
  "correct_answer": "A",
  "explanation": "Explanation of why this is correct, referencing the document.",
  "page_reference": "Page X"
}}

Rules:
- Generate questions in the SAME language as the document.
- Questions must test understanding, not trivial recall.
- All four options must be plausible.
- correct_answer must be one of: A, B, C, D.

DOCUMENT:
{text}"""


def generate_quiz(documents: List[Document], api_key: str,
                  num_questions: int = 5) -> List[dict]:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.7,
    )

    combined = "\n\n".join(d.page_content for d in documents[:40])
    prompt = QUIZ_PROMPT.format(n=num_questions, text=combined[:8000])
    response = llm.invoke(prompt)
    content = response.content.strip()

    match = re.search(r'\[.*\]', content, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return []
