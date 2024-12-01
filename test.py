# List available indexes
import os
from pinecone import Pinecone
from dotenv import load_dotenv
load_dotenv()
from codebase_rag_completed import add_repo_to_pinecone
# pinecone_api_key = os.getenv("PINECONE_API_KEY")
# pinecone_index_name = "codebase-rag"
# pinecone_client = Pinecone(api_key=pinecone_api_key)
# pinecone_index = pinecone_client.Index(pinecone_index_name)


# available_indexes = pinecone_client.list_indexes()
# print("Available indexes:", available_indexes)

# # Ensure 'codebase-rag' exists
# if pinecone_index_name not in available_indexes:
#     raise ValueError(f"Index '{pinecone_index_name}' not found. Available indexes: {available_indexes}")
add_repo_to_pinecone("https://github.com/rChwiecko/Vestique")

