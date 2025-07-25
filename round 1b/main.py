from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List
import os
import tempfile
from datetime import datetime
from fastapi import FastAPI

app = FastAPI(
    title="Persona-Driven Document Intelligence API",
    description="Upload PDFs to extract persona-relevant content",
    version="1.0.0"
)

from .core.news_processor import NewsProcessor  # ✅ use news processor
from .core.analyzer import PersonaAnalyzer
from .core.scorer import RelevanceScorer

@app.post ("/analyze", summary="Analyze uploaded PDFs based on persona and job")
async def analyze_documents(
    files: List[UploadFile] = File(..., description="Upload 3–5 PDF files"),
    persona: str = Form(..., description="Persona (e.g., Journalist reporting on education)"),
    job: str = Form(..., description="Job to be done (e.g., Summarize key education impact stories)")
):
    doc_paths = []

    try:
        for file in files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
                tmp.write(await file.read())
                doc_paths.append(tmp.name)

        # ✅ Extract content using NewsProcessor
        documents = []
        for path in doc_paths:
            articles = news_processor.extract_articles(path)
            for article in articles:
                documents.append({
                    "name": article["document"],
                    "page": article["page"],
                    "sections": [{
                        "title": article["title"],
                        "content": article["content"]
                    }]
                })

        # Analyze persona + score content
        persona_analysis = analyzer.analyze_persona(persona, job)
        scored_docs = scorer.score_documents(documents, persona_analysis)
        top_sections = scorer.get_top_sections(scored_docs)

        # ✅ Enhanced output: Include extracted content
        output = {
            "metadata": {
                "input_documents": [f.filename for f in files],
                "persona": persona,
                "job": job,
                "processing_timestamp": datetime.utcnow().isoformat()
            },
            "extracted_sections": [
                {
                    "document": s["document"],
                    "page_number": s["page"],
                    "section_title": s["title"],
                    "importance_rank": i + 1,
                    "score": float(s["score"]),
                    "refined_text": s["content"][:800]  # show top 800 chars
                } for i, s in enumerate(top_sections)
            ]
        }

        return JSONResponse(content=output)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        for path in doc_paths:
            os.remove(path)
