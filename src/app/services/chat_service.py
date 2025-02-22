from fastapi import Depends
from app.repositories.chat_repository import ChatRepository
from app.config.settings import Config
from groq import Groq

class ChatService:
    
    def __init__(self, chat_repo: ChatRepository = Depends()):
        self.chat_repo = chat_repo
    
    async def get_relevant_text(self, question: str):
        return await self.chat_repo.get_relevant_text(question = question)
    
    async def get_answer(self, question: str, relevant_text: str):
        
        groq_client = Groq(api_key = Config.GROQ_API_KEY)
        
        prompt_template = """
        
            <question>
            {question}
            </question>

            <context>
            {relevant_text}
            </context>
            
            Ensure that your answer directly addresses the question enclosed in the <question> tags, based on the provided context enclosed in the <context> tags. 
            
            Keep your response clear, concise, and grounded solely in the information from the relevant text. 
            Avoid including any unrelated information, assumptions, or speculative content.
        """
        
        chat_completion = groq_client.chat.completions.create(
            messages = [
                {
                    "role" : "system",
                    "content" : "You are a question-answering AI. Please provide a well-reasoned and accurate response to the questions ask by the user."
                },
                {
                    "role" : "user",
                    "content" : prompt_template.format(question = question, relevant_text = relevant_text)
                }
            ],
            model = 'gemma2-9b-it'
        )
        
        response = chat_completion.choices[0].message.content

        return response
        