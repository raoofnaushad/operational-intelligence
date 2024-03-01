from llama_index import StorageContext
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores import PGVectorStore
from urllib.parse import quote_plus
import openai
from dotenv import load_dotenv
import os

from llama_index import download_loader

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def to_vectorize_interview(interview_id, table_name='interviewboard'):
    try:
        encoded_password = quote_plus(os.environ["POSTGRES_PASSWORD"])

        # Assuming download_loader is a function that loads your DatabaseReader
        DatabaseReader = download_loader('DatabaseReader')

        reader = DatabaseReader(
            scheme="postgresql",
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            user=os.environ["POSTGRES_USER"],
            password=encoded_password,
            dbname=os.environ["POSTGRES_DB"],
        )

        query = f"""
                SELECT meeting_summary
                FROM {table_name}
                WHERE id = {interview_id}
                """

        documents = reader.load_data(query=query)

        # Assuming PGVectorStore and StorageContext are properly defined elsewhere
        vector_store = PGVectorStore.from_params(
            database=os.environ["POSTGRES_DB"],
            host=os.environ["POSTGRES_HOST"],
            password=encoded_password,
            port=os.environ["POSTGRES_PORT"],
            user=os.environ["POSTGRES_USER"],
            table_name=os.environ["POSTGRES_VECTOR_TABLE"],
            # table_name="vector_table",
            embed_dim=1536,  # OpenAI embedding dimension
        )

        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, show_progress=True
        )

        return index
    except Exception as e:
        print("Failed to vectorize interview: %s", e)
        raise



if __name__ == "__main__":
    id = 13
    to_vectorize_interview(id)