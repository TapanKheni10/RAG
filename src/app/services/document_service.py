from fastapi import UploadFile, Depends
from app.repositories.document_repository import DocumentRepository
import fitz
import re
import os
from typing import List

class DocumentService:
    
    def __init__(self, document_repo: DocumentRepository = Depends()):
        self.document_repo = document_repo
        
    async def get_text_from_doc(self, file_path: str):
        text = ""
    
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text('text') + "\n"
            
        text = re.sub(r'\n+', '\n', text).strip()
        text = re.sub(r'\s+', ' ', text)
        
        return text
        
    async def save_file(self, uploaded_file: UploadFile):
        file_location = f"../../../data/{uploaded_file.filename}"
        
        if not os.path.exists(file_location):
            os.makedirs(os.path.dirname(file_location), exist_ok=True)
        
        with open(file_location, "wb") as file_object:
            file_object.write(await uploaded_file.read())
            
        return file_location
    
    async def get_text_chunks(self, text: str):
        chunk_size = 512
        chunk_overlap = 70
        
        words = text.split()
    
        chunks = []
        for i in range(0, len(words), chunk_size - chunk_overlap):
            chunks.append(" ".join(words[i:i+chunk_size]))
            
        return chunks
    
    async def save_text_chunks(self, doc_chunks: List[str]):
        
        return await self.document_repo.save_text_chunks(doc_chunks = doc_chunks)