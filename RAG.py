from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.memory import VectorMemory
from llama_index.llms.gemini import Gemini
from llama_index.core.llms import ChatMessage
from pinecone import Pinecone
from dotenv import load_dotenv
from llama_index.core import Settings
from fastapi import HTTPException
import os
import json
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReasoningLoopQueryEngine:
    def __init__(self):
        pc = Pinecone(os.environ.get("PINECONE_API_KEY"))
        self.index_name = "cocktails-1"
        self.index_namespace = "ckts1"

        self.llm = Gemini(model="models/gemini-2.0-flash", api_key=os.environ.get("GEMINI_API_KEY"))
        self.embed_model = HuggingFaceEmbedding(os.environ.get("EMBEDDING_MODEL_NAME"))
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model
        Settings.chunk_size = 512

        pinecone_index = pc.Index(self.index_name)
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        vector_store.namespace = self.index_namespace
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        retriever = VectorIndexRetriever(index=index, similarity_top_k=5)
        self.query_engine = RetrieverQueryEngine(retriever=retriever)

        self.vector_memory: VectorMemory = VectorMemory.from_defaults(
            vector_store=None,
            embed_model=self.embed_model,
            retriever_kwargs={"similarity_top_k": 1}
        )

    def extract_info(self, query):
        prompt = f"""
        Extract personal information from user about their taste preferences regarding cocktails, such as favorite ingredients,
        flavors. Format it in JSON format with fields like 'ingredients', 
        'flavors', 'fruits', 'drinks'
        
        User Query: '{query}'
        JSON Output:
        """
        info = self.llm.complete(prompt).text.replace("```json", '').replace("```", '')
        info_json = json.loads(info)
        return info_json

    def upsert_info(self, info):
        if info:
            info_str = json.dumps(info)
            node = ChatMessage.from_str(info_str, 'user')
            self.vector_memory.put(node)

    def query(self, query):
        try:
            additional_info = self.vector_memory.get(f"What does user {os.environ.get('USER_ID')} like?")
            if additional_info:
                additional_info = additional_info[0].content
                query = query + f". Note that I like {additional_info}"
        except Exception as e:
            logger.error(f"Critical error, unable to parse additional info")
            raise HTTPException(status_code=500, detail=str(e))
        try:
            response = self.query_engine.query(query)
        except Exception as e:
            logger.error(f"Critical error, unable to get response from LLM")
            raise HTTPException(status_code=500, detail=str(e))
        try:
            user_info = self.extract_info(query, response)
        except Exception as e:
            logger.error(f"Critical error, unable to extract info from query")
            raise HTTPException(status_code=500, detail=str(e))
        try:
            self.upsert_info(user_info)
        except Exception as e:
            logger.error(f"Critical error, unable to upsert to vector database")
            raise HTTPException(status_code=500, detail=str(e))

        return response

