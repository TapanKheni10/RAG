from fastapi import Depends
from app.services.chat_service import ChatService

class ChatUsecase:
    
    def __init__(self, chat_service: ChatService = Depends()):
        self.chat_service = chat_service
        
    async def task_get_answer(self, question: str):
        
        relevant_text_list = await self.chat_service.get_relevant_text(question = question)
        
        relevant_text = "\n".join(relevant_text_list)
        
        return await self.chat_service.get_answer(question = question, relevant_text = relevant_text)
    
        
        