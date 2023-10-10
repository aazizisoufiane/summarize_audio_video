import json
import os
from getpass import getpass
from urllib.request import urlopen

import openai
import pandas as pd
import phoenix as px
from gcsfs import GCSFileSystem
from llama_index import ServiceContext, StorageContext, load_index_from_storage, set_global_handler
from llama_index.embeddings import OpenAIEmbedding
from llama_index.graph_stores.simple import SimpleGraphStore
from llama_index.llms import OpenAI
from phoenix.experimental.evals import (
    OpenAIModel,
    compute_precisions_at_k,
    run_relevance_eval,
)
from tqdm import tqdm

import nest_asyncio
from llama_index import (
    SimpleDirectoryReader,
    ServiceContext,
    get_response_synthesizer,
)
from llama_index.indices.document_summary import DocumentSummaryIndex
from llama_index.llms import OpenAI
from llama_index.schema import Document
nest_asyncio.apply()

import json
from llama_index import Document

def load_json_file_and_extract_text(json_file_path):
    """Loads a JSON file and extracts the content of the "text" key.

    Args:
    json_file_path: The path to the JSON file.

    Returns:
    A list of Document objects, containing the extracted content of the "text" key.
    """

    documents = []

    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)
        # return json_data
        documents.append(Document(doc_id=json_file_path , text=json_data["text"]))

    return documents
document = load_json_file_and_extract_text("transcriptions/youtube_5p248yoa3oE.json")

# LLM (gpt-3.5-turbo)
chatgpt = OpenAI(temperature=0, model="gpt-3.5-turbo")
service_context = ServiceContext.from_defaults(llm=chatgpt, chunk_size=1024)

# default mode of building the index
response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize", use_async=True
)
doc_summary_index = DocumentSummaryIndex.from_documents(
    document,
    service_context=service_context,
    response_synthesizer=response_synthesizer,
    show_progress=True,
)
query_engine = doc_summary_index.as_query_engine(
    response_mode="tree_summarize", use_async=True
)

print(doc_summary_index.get_document_summary(doc_id='transcriptions/youtube_5p248yoa3oE.json'))

def query_summary(query):
    response = query_engine.query(query)
    return response.response
r = query_summary("What are the author's thoughts on the risks and benefits of AI for humanity")
r
