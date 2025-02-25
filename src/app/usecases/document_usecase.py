from fastapi import Depends, UploadFile
from app.services.document_service import DocumentService
import time

class DocumentUsecase:
    
    def __init__(self, document_service: DocumentService = Depends()):
        self.document_service = document_service
        
    async def task_upload_doc(self, uploaded_file: UploadFile):
        file_path = await self.document_service.save_file(uploaded_file = uploaded_file)
        
        text = await self.document_service.get_text_from_doc(file_path = file_path)
        
        doc_chunks = await self.document_service.get_text_chunks(text = text)
        
        return await self.document_service.save_text_chunks(doc_chunks = doc_chunks)
        
        