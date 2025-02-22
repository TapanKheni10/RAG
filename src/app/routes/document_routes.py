from fastapi import APIRouter, UploadFile, File, Depends
from app.controllers import document_controller

doc_router = APIRouter()

@doc_router.post('/doc/upload')
async def upload_document(uploaded_file: UploadFile = File(...), document_controller: document_controller.DocumentController = Depends()):
    return await document_controller.upload_doc(uploaded_file = uploaded_file)