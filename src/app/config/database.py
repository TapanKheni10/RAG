from app.config.settings import Config
from pinecone.grpc import PineconeGRPC
from pinecone import ServerlessSpec
from pymilvus import MilvusClient
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance

class VectorDB:
    def __init__(self):
        self.pinecone_client = None
        self.milvus_client = None
        self.qdrant_client = None
        
    async def create_pinecone_client(self):
        self.pinecone_client = PineconeGRPC(api_key = Config.PINECONE_API_KEY)
        
    async def create_pinecone_index(self):
        if not self.pinecone_client.has_index(name = 'hybrid-search-index'):
            
            self.pinecone_client.create_index(
                name = 'hybrid-search-index',
                dimension = 768,
                metric = 'dotproduct',
                spec = ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"        
                )
            )
        
    async def delete_pinecone_index(self):
        self.pinecone_client.delete_index(name = 'hybrid-search-index')
        
    async def create_qdrant_client(self):
        self.qdrant_client = AsyncQdrantClient(
            url = 'http://localhost:6333'
        )
        
    async def create_qdrant_collection(self):
        if not await self.qdrant_client.collection_exists(collection_name = 'document_embeddings_collection'):
            await self.qdrant_client.create_collection(
                collection_name = "document_embeddings_collection",
                vectors_config = VectorParams(
                    size = 384,
                    distance = Distance.COSINE
                )
            )
        
    async def delete_qdrant_collection(self):
        await self.qdrant_client.delete_collection(collection_name = 'document_embeddings_collection')
    
    async def create_milvus_client(self):
        self.milvus_client = MilvusClient(uri = '../database/milvus_demo.db')
        
    async def create_milvus_db_collection(self):
        if self.milvus_client.has_collection(collection_name = 'document_embeddings_collection'):
            self.milvus_client.drop_collection(collection_name = 'document_embeddings_collection')
        
        self.milvus_client.create_collection(collection_name = 'document_embeddings_collection', dimension = 768)
        
    async def drop_milvus_db_collection(self):
        self.milvus_client.drop_collection(collection_name = 'document_embeddings_collection')
            
database = VectorDB()