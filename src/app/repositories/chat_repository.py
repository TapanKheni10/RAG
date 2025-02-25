from sentence_transformers import SentenceTransformer
from app.config.database import database
from cohere import ClientV2
from app.config.settings import Config
from httpx import Client

class ChatRepository:
    
    def __init__(self):
        self.database = database
        self.embedding_fn = SentenceTransformer('all-mpnet-base-v2')
        self.cohere_client = ClientV2(api_key = Config.COHERE_API_KEY, httpx_client = Client(verify = False))
        
    async def get_relevant_text(self, question: str):
        
        query_vector = self.embedding_fn.encode([question])
        
        query_sparse_vector = self.database.pinecone_client.inference.embed(
            model = 'pinecone-sparse-english-v0',
            inputs = [question],
            parameters = {
                'input_type' : 'query',
                'return_tokens' : True
            }
        )
        
        index = self.database.pinecone_client.Index('hybrid-search-index')
        
        results = index.query(
            namespace = 'hybrid-search-attention-namespace',
            vector = query_vector[0].tolist(),
            sparse_vector = {
                "indices" : query_sparse_vector[0]['sparse_indices'],
                "values" : query_sparse_vector[0]['sparse_values']
            },
            top_k = 10,
            include_values = False,
            include_metadata = True
        )
        
        relevant_text = []

        for result in results['matches']:
            relevant_text.append(result['metadata']['source_text'])
                
        reranked_results = self.cohere_client.rerank(
            model = 'rerank-v3.5',
            query = question,
            documents = relevant_text,
            return_documents = True,
            top_n = 3
        )
        
        reranked_text = []
        for doc in reranked_results.results:
            reranked_text.append(doc.document.text)
            
        return reranked_text