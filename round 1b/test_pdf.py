import unittest
from app.core.processor import DocumentProcessor
import os

class TestPDFExtraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.processor = DocumentProcessor()
        cls.test_pdf = os.path.join("data", "sample_inputs", "sample.pdf")

    def test_extraction(self):
        result = self.processor.extract_text(self.test_pdf)
        self.assertGreater(len(result), 0)
        self.assertIn("text", result[0])
        print("\nExtracted text sample:", result[0]["text"][:100] + "...")

if __name__ == "__main__":
    unittest.main()