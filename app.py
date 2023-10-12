# Import Streamlit
import os
import time

import streamlit as st

from config import output_path_youtube, output_path_transcription
from keyword_retriever.keyword_retreiver import VideoRetriever
from logger import logger
from resource_loader.youtube_loader import YouTubeLoader
from summarization_service.summarizer import TranscriptSummary
from utils import check_file_exists, download_video, transcribe_video, load_transcription
st.set_page_config(
        page_title="Summary",
        layout="wide"
)
# from  main import factory

# Initialize chat history
chat_history = []

# Placeholder for the video; initially empty
# video_slot = st.empty()


# Layout Configuration
# st.set_page_config(page_title="Your Awesome App", layout="wide")


def my_hash_func(tokenizer):
    return tokenizer.to_str()


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
# from streamlit_player import st_player

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

    # Main Content - Bottom Section for Chat
    st.title("Chat UI")

    # Display chat history
    if chat_history:
        st.text_area("Chat History", "\n".join(chat_history), height=200)

    # Get user input
    user_input_chat = st.text_input("Type your message here...")

    # Check if the user has entered a new message
    if user_input_chat:
        chat_history.append(f'You: {user_input_chat}')
        st.text_area("Chat History", "\n".join(chat_history), height=200)

        # Clear the user input field
        answer = transcript_summary.query_summary(user_input_chat)
        st.text_input(answer, value="", key=1)

        # Simulate bot reply
        time.sleep(2)
        chat_history.append('Bot: Thank you for your message.')
        st.text_area("Chat History", "\n".join(chat_history), height=200)

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

