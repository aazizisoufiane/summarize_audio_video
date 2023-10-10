import json

from llama_index.schema import Document


def load_json_file_and_extract_text(json_file_path):
    documents = []
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)
        documents.append(Document(doc_id=json_file_path, text=json_data["text"]))
    return documents
