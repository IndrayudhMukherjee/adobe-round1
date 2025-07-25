# tests/test_pdf_processor.py
import pytest # type: ignore
import os
from app.core.processor import DocumentProcessor

@pytest.fixture
def sample_pdf():
    return os.path.join("data", "sample_inputs", "sample.pdf")

@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_pdf_extraction(sample_pdf):
    processor = DocumentProcessor()
    result = processor.extract_text(sample_pdf)
    assert len(result) > 0
    assert "text" in result[0]
    assert len(result[0]["text"]) > 100