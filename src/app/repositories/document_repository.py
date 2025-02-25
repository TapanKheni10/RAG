from typing import List
from tqdm.auto import tqdm
from sentence_transformers import SentenceTransformer
from app.config.database import database


class DocumentRepository:
    
    def __init__(self):
        self.embedding_fn = SentenceTransformer('all-mpnet-base-v2')
    
    async def save_text_chunks(self, doc_chunks: List[str]):
        
        batch_size = 96
        
        sparse_embeddings = []
        
        for i in tqdm(range(0, len(doc_chunks), batch_size)):
            i_end = min(i + batch_size, len(doc_chunks))
            
            sp_embed = database.pinecone_client.inference.embed(
                model = 'pinecone-sparse-english-v0',
                inputs = doc_chunks[i:i_end],
                parameters = {
                    'input_type' : 'passage',
                    'return_tokens' : True
                }
            )
            sparse_embeddings.extend(sp_embed)
        
        embeddings = self.embedding_fn.encode(doc_chunks)
    
        index = database.pinecone_client.Index('hybrid-search-index')

        for i in tqdm(range(0, len(doc_chunks), batch_size)):
            
            i_end = min(i + batch_size, len(doc_chunks))
            
            sparse_embeds = sparse_embeddings[i:i_end]
            dense_embeds = embeddings[i:i_end]
            
            ids = [str(x) for x in range(i, i_end)]
            
            records = []
            
            for j in range(len(ids)):
                records.append({
                    "id" : ids[j],
                    "sparse_values" : {
                        "indices" : sparse_embeds[j]['sparse_indices'],
                        "values" : sparse_embeds[j]['sparse_values']
                    },
                    "values" : dense_embeds[j],
                    "metadata" : {
                        "source_text" : doc_chunks[i+j]
                    }
                }) 
                
            index.upsert(
                vectors = records,
                namespace = 'hybrid-search-attention-namespace'
            )
            
        return {"message": "Text chunks saved successfully into the vectorDB."}