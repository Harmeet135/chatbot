from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from images.models import PdfDocument

class PdfDocumentTestCase(TestCase):
    def test_pdf_document_creation(self):
        # Create a sample PDF file
        sample_pdf_content = b'This is a sample PDF content.'
        sample_pdf = SimpleUploadedFile('sample.pdf', sample_pdf_content, content_type='application/pdf')

        # Create a PdfDocument instance with the sample PDF file
        pdf_document = PdfDocument.objects.create(pdf=sample_pdf)

        # Check if the PdfDocument object is created successfully
        self.assertIsNotNone(pdf_document)
        self.assertEqual(pdf_document.pdf.name, 'pdfs/sample.pdf')  # Ensure correct file path
        self.assertIsNone(pdf_document.conversational_rag_chain)  # Ensure conversational_rag_chain is initially None

        # Test the __str__ method
        self.assertEqual(str(pdf_document), f"PDF Document - {pdf_document.id}")
