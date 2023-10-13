# Import Streamlit
import os

import streamlit as st
from streamlit_chat import message

from config import output_path_youtube, output_path_transcription
from keyword_retriever.keyword_retreiver import VideoRetriever
from logger import logger
from resource_loader.youtube_loader import YouTubeLoader
from summarization_service.summarizer import TranscriptSummary
from utils import check_file_exists, download_video, transcribe_video, load_transcription

st.set_page_config(page_title="Summary", layout="wide")
# from  main import factory

# Initialize chat history
chat_history = []

logger.info(f"Build retriever")


@st.cache_resource()
def factory(video_id):
    retriever = VideoRetriever(video_id=video_id)
    ts = TranscriptSummary(doc_id=video_id)

    logger.info("video_retriever initialized")
    return retriever, ts

with st.sidebar:
    # Sidebar
    st.title("Controls")
    # Create a sidebar for the YouTube URL, search bar, and settings
    # st.title("Settings")
    youtube_url = st.text_input("Enter YouTube URL:", value="https://www.youtube.com/watch?v=reUZRyXxUs4")

    chosen_LLM = st.selectbox("Choose Language Model", ["LLM-1", "LLM-2", "LLM-3"])
    api_key = st.text_input("OpenAI API Key", type="password")

yt_loader = YouTubeLoader(youtube_url, output_path_youtube)
video_retriever, transcript_summary = factory(yt_loader.video_id)

video_file_path = os.path.join(output_path_youtube, f"{yt_loader.video_id}.mp3")
transcription_file_path = os.path.join(output_path_transcription, f"{yt_loader.video_id}.json")

if not check_file_exists(video_file_path):
    download_video(yt_loader, output_path_youtube)
else:
    logger.info(f"Video already downloaded: {video_file_path}")

if not check_file_exists(transcription_file_path):
    transcribe_video(yt_loader, output_path_youtube, output_path_transcription)
else:
    logger.info(f"Transcription already exists: {transcription_file_path}")

docs = load_transcription(yt_loader, output_path_transcription)

if 'current_video' not in st.session_state:
    st.session_state.current_video = youtube_url
# Main Content - Top Section
col2, col3 = st.columns([3, 1])

# Main Content - Middle Section
video_slot = col2.empty()

with col2:
    video_slot.video(youtube_url)

    st.title("Summary")
    # Display summary here
    st.write(transcript_summary.get_document_summary())
    # Initialize session_state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Main Content - Bottom Section for Chat
    st.title("Chat UI")

with col3:
    user_input = st.text_input("Search:")
    if user_input:
        if st.session_state.current_video:
            video_slot.video(st.session_state.current_video)
        else:
            video_slot.video(youtube_url)

        raw_results = video_retriever.search(user_input)
        for i, result in enumerate(raw_results):
            text_content = result.node.text
            start_time = int(result.node.metadata['start'])

            full_youtube_url = f"{youtube_url}&t={start_time}s"

            if st.button(text_content, key=f"button_{i}"):
                st.session_state.current_video = full_youtube_url
                video_slot.video(full_youtube_url, start_time=start_time)

with col2:
    chat_placeholder = st.empty()


    def on_btn_click():
        del st.session_state.past[:]
        del st.session_state.generated[:]


    def on_input_change():
        user_input = st.session_state.user_input
        st.session_state.past.append(user_input)
        st.session_state.generated.append("The messages from Bot\nWith new line")


    def generate_response(prompt_input):
        answer = transcript_summary.query_summary(prompt_input)

        return answer


    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []

    with chat_placeholder.container():
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
            message(generate_response(st.session_state['past'][i]), key=f"{i}", allow_html=True, is_table=False)

        st.button("Clear message", on_click=on_btn_click)

    with st.container():
        st.text_input("User Input:", on_change=on_input_change, key="user_input")
