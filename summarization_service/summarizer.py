import json
import os

from llama_index import (ServiceContext, get_response_synthesizer, Document)
from llama_index.indices.document_summary import DocumentSummaryIndex
from llama_index.llms import OpenAI

from config import output_path_transcription
from logger import logger


class TranscriptSummary:
    def __init__(self, doc_id, model):
        self.doc_id = doc_id
        self.document = self.load_json_file_and_extract_text()
        self.model = model

        # Check for the presence of the openai_key
        if "gpt" in self.model and "OPENAI_KEY" in os.environ:
            try:
                self.llm = OpenAI(temperature=0, model=self.model)
            except:
                self.llm = "default"

        else:
            self.llm = "default"
        # logger.info(f"LLM ")
        logger.info(f"LLM used: {self.llm}"*50)

        self.service_context = ServiceContext.from_defaults(llm=self.llm, chunk_size=1024)
        self.response_synthesizer = get_response_synthesizer(response_mode="tree_summarize", use_async=True)
        self.doc_summary_index = DocumentSummaryIndex.from_documents(self.document,
                                                                     service_context=self.service_context,
                                                                     response_synthesizer=self.response_synthesizer,
                                                                     show_progress=True)
        self.query_engine = self.doc_summary_index.as_query_engine(response_mode="tree_summarize", use_async=True)

    def load_json_file_and_extract_text(self):
        documents = []
        file_path = os.path.join(output_path_transcription, f"{self.doc_id}.json")
        with open(file_path, "r") as json_file:
            json_data = json.load(json_file)
            documents.append(Document(doc_id=self.doc_id, text=json_data["text"]))
        return documents

    def get_document_summary(self):
        return self.doc_summary_index.get_document_summary(doc_id=self.doc_id)

    def query_summary(self, query):
        response = self.query_engine.query(query)
        return response.response


# Example usage:
if __name__ == "__main__":
    ts = TranscriptSummary(doc_id="youtube_5p248yoa3oE.json")
    print(ts.get_document_summary())
    result = ts.query_summary("What are the author's thoughts on the risks and benefits of AI for humanity")
    print(result)
