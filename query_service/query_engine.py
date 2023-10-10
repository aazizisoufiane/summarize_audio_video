from llama_index import ServiceContext, DocumentSummaryIndex, get_response_synthesizer
from llama_index.llms import OpenAI



def create_query_engine(document):
    chatgpt = OpenAI(temperature=0, model="gpt-3.5-turbo")
    service_context = ServiceContext.from_defaults(llm=chatgpt, chunk_size=1024)

    response_synthesizer = get_response_synthesizer(response_mode="tree_summarize", use_async=True)
    doc_summary_index = DocumentSummaryIndex.from_documents(document, service_context=service_context,
        response_synthesizer=response_synthesizer, show_progress=True, )
    query_engine = doc_summary_index.as_query_engine(response_mode="tree_summarize", use_async=True)
    return query_engine


def query_summary(query_engine, query):
    response = query_engine.query(query)
    return response.response

