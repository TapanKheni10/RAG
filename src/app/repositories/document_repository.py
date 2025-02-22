from typing import List
from sentence_transformers import SentenceTransformer
from app.config.database import database
from qdrant_client.models import PointStruct


class DocumentRepository:
    
    def __init__(self):
        self.embedding_fn = SentenceTransformer('all-MiniLM-L12-v2')
    
    async def save_text_chunks(self, doc_chunks: List[str]):
        
        embeddings = self.embedding_fn.encode(doc_chunks)
        
        points = []

        for i in range(len(doc_chunks)):
            points.append(PointStruct(
                id = i,
                vector = embeddings[i].tolist(),
                payload = {
                    "source_text": doc_chunks[i]
                }
            ))
                
        await database.qdrant_client.upsert(
            collection_name = "document_embeddings_collection",
            points = points,
            wait = True
        )
                
        return {"message": "Text chunks saved successfully into the vectorDB."}