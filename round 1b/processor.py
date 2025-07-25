from PyPDF2 import PdfReader
import os

class DocsProcessor:
    def extract_articles(self, pdf_path):
        reader = PdfReader(pdf_path)
        articles = []
        filename = os.path.basename(pdf_path)

        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text:
                continue

            # Split into paragraphs
            paragraphs = text.split("\n\n")
            for para in paragraphs:
                clean = para.strip().replace("\n", " ")
                if len(clean) > 80 and "header" not in clean.lower():  # filter junk
                    articles.append({
                        "document": filename,
                        "page": page_num + 1,
                        "title": clean[:60],  # Use first 60 chars as title
                        "content": clean
                    })
        return articles
