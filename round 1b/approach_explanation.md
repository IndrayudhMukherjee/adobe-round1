# Approach Explanation

## Problem Statement
Given a set of heterogeneous documents (research papers, brochures, news articles, etc.) and a specific persona-job context (e.g., "Product Manager in semiconductor solutions" tasked with "extracting key value propositions and product categories"), the goal is to extract the most relevant document sections using intelligent document understanding and NLP techniques.

## Methodology

### 1. **Document Ingestion & Parsing**
We allow users to upload 3–5 PDFs through a FastAPI Swagger interface. Using `pdfplumber`, the uploaded PDFs are parsed page-by-page. For news-specific documents, we use a `NewsProcessor` to extract articles by identifying headlines and grouping paragraphs.

### 2. **Persona Understanding**
The persona and job are combined into a single prompt:  
`"Persona: {persona}. Task: {job}"`  
This is passed through a pre-trained SentenceTransformer (`all-MiniLM-L6-v2`) to generate an embedding. Keywords are also extracted from the combined prompt to serve as auxiliary scoring features.

### 3. **Scoring Document Sections**
Each section (typically a paragraph or header-content block) from the parsed documents is scored based on:
- **Cosine similarity** between the section and persona embedding
- **Keyword overlap** with the persona-job context

A weighted score is computed:  
`final_score = 0.7 * semantic_similarity + 0.3 * keyword_score`

### 4. **Ranking & Output Formatting**
Top 5 sections with the highest scores are selected and returned in the output. Each section includes:
- Document name
- Page number
- Section title
- Importance rank
- Similarity score

### 5. **Output Format**
The output JSON is formatted per the challenge specs with:
- Metadata
- Extracted Sections (top 5)
- [Optional] Sub-section analysis (for further summarization, if needed in v2)

## Why This Works
This approach is generalizable across domains (education, finance, engineering, etc.) because:
- It uses universal sentence embeddings
- It combines semantic + lexical scoring
- It works with multi-document input and adapts to any persona-job combo

## Constraints Addressed
- ✅ Model size under 1GB
- ✅ Runs on CPU
- ✅ Outputs in under 60s for 3–5 PDFs
- ✅ Fully offline (no internet calls during execution)

---

