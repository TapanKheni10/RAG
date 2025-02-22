from sentence_transformers import SentenceTransformer
from app.config.database import database

class ChatRepository:
    
    def __init__(self):
        self.database = database
        self.embedding_fn = SentenceTransformer('all-MiniLM-L12-v2')
        
    async def get_relevant_text(self, question: str):
        
        query_vector = self.embedding_fn.encode([question])
        
        search_result = await self.database.qdrant_client.query_points(
            collection_name = "document_embeddings_collection",
            query = query_vector[0].tolist(),
            with_payload = True,
            with_vectors = False,
            limit = 2
        )
        
        relevant_text = []
        for result in search_result:
            print('='*50)
            print(result)
            print('='*50)
            relevant_text.append(result[1][0].payload['source_text'])
            relevant_text.append(result[1][1].payload['source_text'])
            
        print(relevant_text)
        print('='*50)
            
        return relevant_text