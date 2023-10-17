import json
import os
import time

import chromadb
from llama_index import (ServiceContext, StorageContext, VectorStoreIndex, )
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.schema import Document
from llama_index.vector_stores import ChromaVectorStore

import config
from logger import logger


class MediaRetriever:
    def __init__(self, media_id, similarity_top_k=5):
        self.media_id = media_id
        self.similarity_top_k = similarity_top_k

        self._initialize_retriever()

    def _initialize_retriever(self):
        docs = self._load_documents()

        # Create client and a new collection
        chroma_client = chromadb.EphemeralClient()
        try:
            chroma_collection = chroma_client.create_collection(f"quickstart-{time.time()}")
        except Exception as e:
            logger.error(f"Exception encountered: {e}")
            chroma_collection = None

        # Define embedding function
        embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

        # Set up ChromaVectorStore and load in data
        if chroma_collection is not None:
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        else:
            logger.error("chroma_collection is not initialized.")  # handle this case

        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        service_context = ServiceContext.from_defaults(embed_model=embed_model)

        logger.info("Start indexing transcription")
        self.index = VectorStoreIndex.from_documents(docs, storage_context=storage_context,
                                                     service_context=service_context, show_progress=True)
        logger.info("End indexing transcription")

        self.retreiver = self.index.as_retriever(similarity_top_k=self.similarity_top_k)

    def _load_documents(self):
        with open(os.path.join(config.output_path_transcription, f"{self.media_id}.json"), "r") as f:
            json_data = json.load(f)

        documents = []
        for segment in json_data["segments"]:
            text = segment["text"]
            start = segment["start"]
            metadata = {"start": start}
            documents.append(Document(text=text, metadata=metadata))
        return documents

    def search(self, query):
        response = self.retreiver.retrieve(query)
        return response
