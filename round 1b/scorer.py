from typing import List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

class RelevanceScorer:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def score_documents(self, documents: List[Dict], persona: Dict) -> List[Dict]:
        scored_docs = []
        persona_embedding = persona["embedding"]

        for doc in documents:
            scored_sections = []
            for section in doc["sections"]:
                section_embedding = self.analyzer.model.encode(section["content"])
                similarity = cosine_similarity(
                    np.array([persona_embedding]),
                    np.array([section_embedding])
                )[0][0]

                keyword_score = sum(
                    1 for kw in persona["keywords"]
                    if kw in section["content"].lower()
                ) / len(persona["keywords"]) if persona["keywords"] else 0

                final_score = 0.7 * similarity + 0.3 * keyword_score

                scored_sections.append({
                    **section,
                    "score": final_score,
                    "page": doc["page"]
                })

            scored_docs.append({
                "document": doc.get("name", "unknown"),
                "sections": scored_sections
            })

        return scored_docs

    def get_top_sections(self, scored_docs: List[Dict], top_n: int = 5) -> List[Dict]:
        """Extract top N sections across all documents"""
        all_sections = []
        for doc in scored_docs:
            for section in doc["sections"]:
                all_sections.append({
                    "document": doc["document"],
                    **section
                })

        return sorted(all_sections, key=lambda x: x["score"], reverse=True)[:top_n]

