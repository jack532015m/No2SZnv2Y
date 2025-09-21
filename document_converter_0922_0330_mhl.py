# 代码生成时间: 2025-09-22 03:30:44
import os
import celery
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml.ns import nsdecls
from docx.oxml import OxmlElement
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Configuration for Celery
app = Celery('document_converter', broker='pyamqp://guest@localhost//')

# Celery task to convert docx to pdf
@app.task(bind=True)
def convert_docx_to_pdf(self, docx_path, pdf_path):
    try:
        # Check if the docx file exists
        if not os.path.exists(docx_path):
            raise FileNotFoundError(f"No file at {docx_path}")

        # Load the docx file
        doc = Document(docx_path)

        # Create a PDF path if it does not exist
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        # Save the document as a PDF
        doc.save(pdf_path, 'pdf')

        # Return success message
        return {'status': 'success', 'message': 'Document converted to PDF successfully.'}

    except FileNotFoundError as e:
        # Handle file not found error
        self.retry(exc=e)
    except SoftTimeLimitExceeded:
        # Handle soft time limit exceeded error
        return {'status': 'error', 'message': 'Task exceeded the soft time limit.'}
    except Exception as e:
        # Handle any other exceptions
        return {'status': 'error', 'message': str(e)}

# Example usage of the Celery task
if __name__ == '__main__':
    docx_path = 'path_to_your_docx_file.docx'
    pdf_path = 'path_to_your_pdf_output.pdf'
    
    result = convert_docx_to_pdf.delay(docx_path, pdf_path)
    print(result.get())