import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from typing import List


MIND_MAP_PROMPT = """Analyze the following document and extract a hierarchical mind map structure.

Return ONLY a valid JSON object (no markdown, no code blocks, just raw JSON) with this exact structure:
{{
  "name": "Document Main Topic",
  "children": [
    {{
      "name": "Main Topic 1",
      "children": [
        {{"name": "Subtopic 1.1", "children": []}},
        {{"name": "Subtopic 1.2", "children": []}}
      ]
    }},
    {{
      "name": "Main Topic 2",
      "children": [
        {{"name": "Subtopic 2.1", "children": []}},
        {{"name": "Subtopic 2.2", "children": []}}
      ]
    }}
  ]
}}

Rules:
- Root node = main title or topic of the document
- Include 4-7 main branches (top-level children)
- Each branch should have 2-5 sub-nodes
- Keep node names SHORT (2-5 words maximum)
- Use the SAME language as the document (Turkish or English)
- Return ONLY the JSON, nothing else

DOCUMENT:
{text}"""


def generate_mind_map(documents: List[Document], api_key: str) -> dict:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.2,
    )

    combined = "\n\n".join(
        f"[Page {d.metadata.get('page', '?')}]\n{d.page_content}"
        for d in documents[:40]
    )

    prompt = MIND_MAP_PROMPT.format(text=combined[:10000])
    response = llm.invoke(prompt)
    content = response.content.strip()

    content = re.sub(r"^```(?:json)?\s*", "", content)
    content = re.sub(r"\s*```$", "", content)

    return json.loads(content)
