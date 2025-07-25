# core/analyzer.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
from transformers import pipeline

class PersonaAnalyzer:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.summarizer = pipeline(
            "summarization", 
            model="facebook/bart-large-cnn",
            device=-1  # CPU only
        )

    def analyze_persona(self, persona_desc: str, job_desc: str) -> Dict:
        """Generate embedding and keywords for persona-job combination"""
        combined = f"Persona: {persona_desc}. Task: {job_desc}"
        return {
            "embedding": self.model.encode(combined),
            "keywords": self._extract_keywords(combined),
            "description": persona_desc,
            "job": job_desc
        }

    def _extract_keywords(self, text: str) -> List[str]:
        """Naive keyword extraction"""
        stopwords = {"the", "and", "of", "in", "to", "a"}
        words = [word.lower() for word in text.split() if word.isalpha()]
        return list(set([w for w in words if w not in stopwords][:10]))

    def generate_summary(self, text: str, persona: Dict) -> str:
        """Generate persona-aware summary"""
        prompt = f"Summarize this for a {persona['description']} focusing on {persona['job']}:\n\n{text}"
        return self.summarizer(
            prompt,
            max_length=150,
            min_length=30,
            do_sample=False
        )[0]["summary_text"]
