# Import Streamlit
import os

import openai
import streamlit as st
from streamlit_chat import message

from config import output_path_video, output_path_transcription
from keyword_retriever.keyword_retreiver import VideoRetriever
from logger import logger
from resource_loader.uploaded_video_loader import UploadedVideoLoader
from resource_loader.youtube_loader import YouTubeLoader
from summarization_service.summarizer import TranscriptSummary
from utils import check_file_exists, download_video, transcribe_video, load_transcription

st.set_page_config(page_title="Summary", layout="wide")
# from  main import factory

# Initialize chat history
chat_history = []

logger.info(f"Build retriever")


def generate_response(prompt_input):
    answer = transcript_summary.query_summary(prompt_input)

    return answer


@st.cache_resource()
def factory_transcript(video_id, model):
    ts = TranscriptSummary(doc_id=video_id, model=model)
    logger.info("TranscriptSummary initialized")
    return ts


@st.cache_resource()
def factory_video(video_id, top_k):
    retriever = VideoRetriever(video_id=video_id, similarity_top_k=top_k)
    logger.info("video_retriever initialized")
    return retriever


with st.sidebar:
    # Sidebar
    st.title("Controls")
    # Create a sidebar for the YouTube URL, search bar, and settings
    # st.title("Settings")
    # youtube_url = st.text_input("Enter YouTube URL:", value="https://www.youtube.com/watch?v=reUZRyXxUs4")
    youtube_url = st.text_input("Enter YouTube URL:")
    uploaded_video = st.file_uploader("Or upload a video...", type=['mp4', 'mov', 'avi', 'flv', 'mkv'])
    if uploaded_video:
        original_name = uploaded_video.name  # Get the original name of the uploaded file
        video_loader = UploadedVideoLoader(uploaded_video,
                                           original_name)  # youtube_url = st.text_input("Enter YouTube URL:")

        # video_loader.download()


    elif youtube_url:
        # youtube_url = st.text_input("Enter YouTube URL:", value="https://www.youtube.com/watch?v=reUZRyXxUs4")
        video_loader = YouTubeLoader(youtube_url, output_path_video)

    similarity_top_k = st.number_input("Maximum Number of Results to Display", min_value=1, max_value=100, value=10)

    chosen_LLM = st.selectbox("Choose Language Model", ["gpt-3.5-turbo", "default"])
    api_key = st.text_input("OpenAI API Key", type="password")

if api_key:
    openai.api_key = api_key

if youtube_url or uploaded_video:
    video_file_path = os.path.join(output_path_video, f"{video_loader.video_id}.mp3")
    transcription_file_path = os.path.join(output_path_transcription, f"{video_loader.video_id}.json")

    if not check_file_exists(video_file_path):
        download_video(video_loader, output_path_video)
    else:
        logger.info(f"Video already downloaded: {video_file_path}")
    if not check_file_exists(transcription_file_path):
        transcribe_video(video_loader, output_path_video, output_path_transcription)
    else:
        logger.info(f"Transcription already exists: {transcription_file_path}")

    video_retriever = factory_video(video_loader.video_id, top_k=int(similarity_top_k))
    transcript_summary = factory_transcript(video_loader.video_id, model=chosen_LLM)

    docs = load_transcription(video_loader, output_path_transcription)

    if 'current_video' not in st.session_state:
        st.session_state.current_video = youtube_url
    # Main Content - Top Section
    col2, col3 = st.columns([3, 1])

    # Main Content - Middle Section
    video_slot = col2.empty()

    with col2:
        if isinstance(video_loader, UploadedVideoLoader):
            video_slot.video(uploaded_video)
        elif isinstance(video_loader, YouTubeLoader):
            video_slot.video(youtube_url)

        st.title("Summary")
        # Display summary here
        st.write(transcript_summary.get_document_summary())
        # Initialize session_state for chat history if it doesn't exist
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        # Main Content - Bottom Section for Chat
        st.title("Ask me")

    with col3:
        user_input = st.text_input("Search:")
        if user_input:
            if st.session_state.current_video:
                video_slot.video(st.session_state.current_video)
            else:
                if isinstance(video_loader, UploadedVideoLoader):
                    video_slot.video(uploaded_video)
                elif isinstance(video_loader, YouTubeLoader):
                    video_slot.video(youtube_url)

            raw_results = video_retriever.search(user_input)
            for i, result in enumerate(raw_results):
                text_content = result.node.text
                start_time = int(result.node.metadata['start'])

                full_youtube_url = f"{youtube_url}&t={start_time}s"

                if st.button(text_content, key=f"button_{i}"):
                    st.session_state.current_video = full_youtube_url
                    if isinstance(video_loader, UploadedVideoLoader):
                        video_slot.video(uploaded_video, start_time=start_time)
                    elif isinstance(video_loader, YouTubeLoader):
                        video_slot.video(youtube_url, start_time=start_time)

    with col2:
        chat_placeholder = st.empty()


        def on_btn_click():
            del st.session_state.past[:]
            del st.session_state.generated[:]


        def on_input_change():
            user_input = st.session_state.user_input
            st.session_state.past.append(user_input)
            st.session_state.generated.append("The messages from Bot\nWith new line")


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
