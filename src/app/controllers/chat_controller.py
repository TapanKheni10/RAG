from fastapi import Depends
from app.usecases.chat_usecase import ChatUsecase

class ChatController:
    def __init__(self, chat_usecase: ChatUsecase = Depends()):
        self.chat_usecase = chat_usecase
        
    async def get_answer(self, question: str):
        return await self.chat_usecase.task_get_answer(question = question)