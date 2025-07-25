import streamlit as st
from core.processor import DocumentProcessor
from core.analyzer import PersonaAnalyzer
from core.scorer import RelevanceScorer
import os
from datetime import datetime

# Initialize components
processor = DocumentProcessor()
analyzer = PersonaAnalyzer()
scorer = RelevanceScorer(analyzer)

st.title("Persona-Driven Document Intelligence")

# Inputs
persona = st.text_area("Persona Description", 
                      "PhD Researcher in Computational Biology")
job = st.text_area("Job to be Done", 
                  "Prepare literature review on GNN methodologies")
uploaded_files = st.file_uploader("Upload Documents", 
                                type="pdf", 
                                accept_multiple_files=True)

if uploaded_files and st.button("Analyze"):
    with st.spinner("Processing documents..."):
        # Save files
        doc_paths = []
        for file in uploaded_files:
            path = os.path.join("/tmp", file.name)
            with open(path, "wb") as f:
                f.write(file.getbuffer())
            doc_paths.append(path)
        
        # Process
        documents = []
        for path in doc_paths:
            documents.extend(processor.extract_text(path))
        
        persona_analysis = analyzer.analyze_persona(persona, job)
        scored_docs = scorer.score_documents(documents, persona_analysis)
        top_sections = scorer.get_top_sections(scored_docs, top_n=5)
        
        # Display results
        st.success("Analysis Complete!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top Sections")
            for i, section in enumerate(top_sections):
                with st.expander(f"{i+1}. {section['title']} (Score: {section['score']:.2f})"):
                    st.write(f"**Document:** {section['document']} (Page {section['page']})")
                    st.write(section["content"][:500] + "...")
        
        with col2:
            st.subheader("Analysis")
            st.write(f"**Persona Keywords:** {', '.join(persona_analysis['keywords'])}")
            
            # Simple visualization
            scores = [s["score"] for s in top_sections]
            st.bar_chart({"Scores": scores})