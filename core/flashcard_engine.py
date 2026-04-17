from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from typing import List
import json
import re
import datetime

def generate_flashcards(documents: List[Document], api_key: str, num_cards: int = 10) -> List[dict]:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=api_key, 
        temperature=0.3
    )
    
    combined = "\n\n".join(d.page_content for d in documents[:30])
    
    prompt = f"""Analyze the document and extract the {num_cards} most important concepts, terms, or facts.
    Create study flashcards for them. Return ONLY a valid JSON array of objects. 
    Do not include markdown blocks like ```json.
    Each object must have a "term" and a "definition".
    Language: Same as the document.
    
    Example format:
    [
      {{"term": "Machine Learning", "definition": "A branch of AI..."}},
      {{"term": "Algorithm", "definition": "A step-by-step procedure..."}}
    ]
    
    DOCUMENT:
    {combined[:10000]}"""
    
    response = llm.invoke(prompt)
    
    # JSON verisini metinden temizleyip çıkarıyoruz
    clean_text = response.content.replace("```json", "").replace("```", "").strip()
    try:
        cards = json.loads(clean_text)
        # Leitner Sistemi için gerekli varsayılan ayarları her karta ekliyoruz
        today = datetime.datetime.now().date()
        for card in cards:
            card["box"] = 1 # Herkes 1. kutudan başlar
            card["next_review"] = today.isoformat() # Bugün çalışılacak
        return cards
    except Exception as e:
        print(f"JSON Parse Error: {e}")
        return []