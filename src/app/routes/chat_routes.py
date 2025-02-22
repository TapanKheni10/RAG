from fastapi import APIRouter, Depends, Body
from app.controllers import chat_controller

chat_router = APIRouter()

@chat_router.post('/doc/chat')
async def get_answer(input_dict: dict = Body(...), chat_controller: chat_controller.ChatController = Depends()):
    return await chat_controller.get_answer(question = input_dict['question'])