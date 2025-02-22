from fastapi import Depends, UploadFile
from app.usecases.document_usecase import DocumentUsecase

class DocumentController:
    def __init__(self, doc_usecase: DocumentUsecase = Depends()):
        self.doc_usecase = doc_usecase
        
    async def upload_doc(self, uploaded_file: UploadFile):
        return await self.doc_usecase.task_upload_doc(uploaded_file = uploaded_file)