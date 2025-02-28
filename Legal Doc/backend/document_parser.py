from PyPDF2 import PdfReader
from docx import Document
from fastapi import HTTPException
import io
import re

async def parse_document(file):
    try:
        content = await file.read()
        
        if file.filename.endswith('.pdf'):
            reader = PdfReader(io.BytesIO(content))
            text = "\n".join([page.extract_text() for page in reader.pages])
            return re.sub(r'\s+', ' ', text).strip()
        
        elif file.filename.endswith('.docx'):
            doc = Document(io.BytesIO(content))
            return "\n".join([para.text for para in doc.paragraphs])
        
        raise HTTPException(400, "Unsupported file format")
    
    except Exception as e:
        raise HTTPException(500, f"Document parsing failed: {str(e)}")