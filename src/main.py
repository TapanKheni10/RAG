from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config.database import database
from app.routes import (
    document_routes,
    chat_routes
)

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Starting the application 🎬")
    await database.create_pinecone_client()
    await database.create_pinecone_index()
    print('database connection established...')
    yield
    await database.delete_pinecone_index()
    print("your database connection closed.")
    
version = "0.1.0"
app = FastAPI(
    title = 'API for RAG (Retrieval and Generation)',
    version = version,
    lifespan = life_span
)

app.include_router(router = document_routes.doc_router, prefix=f"/api/{version}")
app.include_router(router = chat_routes.chat_router, prefix=f"/api/{version}")
