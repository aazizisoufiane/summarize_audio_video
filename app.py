# Import Streamlit
import os

import openai
import streamlit as st
from streamlit_chat import message

from config import output_path_video, output_path_transcription
from keyword_retriever.keyword_retreiver import MediaRetriever
from logger import logger
from resource_loader.uploaded_media_loader import UploadedMediaLoader
from resource_loader.youtube_loader import YouTubeLoader
from summarization_service.summarizer import TranscriptSummary
from utils import check_file_exists, download_video, transcribe_video, load_transcription

st.set_page_config(page_title="Summary", layout="wide")
# from  main import factory

# Initialize chat history
chat_history = []
# Initialize variables for LLM options and chosen LLM
llm_options = []
chosen_LLM = "default"

logger.info(f"Build retriever")


def generate_response(prompt_input):
    answer = transcript_summary.query_summary(prompt_input)

    return answer


@st.cache_resource()
def factory_transcript(media_id, model, llm_provider):
    ts = TranscriptSummary(doc_id=media_id, model=model, llm_provider=llm_provider)
    logger.info("TranscriptSummary initialized")
    return ts


@st.cache_resource()
def factory_media(media_id, top_k):
    retriever = MediaRetriever(media_id=media_id, similarity_top_k=top_k)
    logger.info("video_retriever initialized")
    return retriever


with st.sidebar:
    # Sidebar
    st.title("Controls")
    # Create a sidebar for the YouTube URL, search bar, and settings
    youtube_url = st.text_input("Enter YouTube URL:")
    uploaded_file = st.file_uploader("Or upload a video...", type=['mp4', 'mov', 'avi', 'flv', 'mkv'])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]

        if file_extension in ['mp4', 'mov', 'avi', 'flv', 'mkv']:
            media_type = 'video'
        elif file_extension in ['mp3', 'wav', 'aac', 'ogg']:
            media_type = 'audio'
        else:
            media_type = 'unknown'

        media_loader = UploadedMediaLoader(uploaded_file, uploaded_file.name, media_type=media_type)

    elif youtube_url:
        # youtube_url = st.text_input("Enter YouTube URL:", value="https://www.youtube.com/watch?v=reUZRyXxUs4")
        media_loader = YouTubeLoader(youtube_url, output_path_video)

    similarity_top_k = st.number_input("Maximum Number of Results to Display", min_value=1, max_value=100, value=10)

    # Selecting the provider
    chosen_provider = st.selectbox("Choose Provider", ["OpenAI", "Replicate", "Default"])

    # Based on provider, display relevant LLMs
    if chosen_provider == "OpenAI":
        llm_options = ["gpt-3.5-turbo-0301", "gpt-3.5-turbo-16k", "gpt-4", "gpt-4-32k-0314"]
    elif chosen_provider == "Replicate":
        llm_options = ["mistralai/mistral-7b-v0.1:3e8a0fb6d7812ce30701ba597e5080689bef8a013e5c6a724fafb108cc2426a0",
                       "mistralai/mistral-7b-instruct-v0.1:83b6a56e7c828e667f21fd596c338fd4f0039b46bcfa18d973e8e70e455fda70",
                       "joehoover/zephyr-7b-alpha:14ec63365a1141134c41b652fe798633f48b1fd28b356725c4d8842a0ac151ee",
                       "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
                       "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
                       "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e", ]
    else:
        llm_options = ["default"]

    # Allow users to type a custom LLM or choose from list
    chosen_LLM = st.selectbox("Type or Choose Language Model", llm_options)

    api_key = st.text_input("OpenAI API Key", type="password")

if api_key and chosen_provider == "OpenAI":
    logger.info("OpenAI API KEY")
    try:
        openai.api_key = api_key
    except:
        st.sidebar.write("Incorrect API key provided")
elif api_key and chosen_provider == "Replicate":
    logger.info("Replicate API KEY")

    os.environ['REPLICATE_API_TOKEN'] = api_key
else:
    chosen_LLM = "default"
    chosen_provider = "Default"

if youtube_url or uploaded_file:
    video_file_path = os.path.join(output_path_video, f"{media_loader.media_id}.mp3")
    transcription_file_path = os.path.join(output_path_transcription, f"{media_loader.media_id}.json")

    if not check_file_exists(video_file_path):
        download_video(media_loader)
    else:
        logger.info(f"Video already downloaded: {video_file_path}")
    if not check_file_exists(transcription_file_path):
        transcribe_video(media_loader, output_path_video, output_path_transcription)
    else:
        logger.info(f"Transcription already exists: {transcription_file_path}")

    video_retriever = factory_media(media_loader.media_id, top_k=int(similarity_top_k))
    transcript_summary = factory_transcript(media_loader.media_id, model=chosen_LLM, llm_provider=chosen_provider)

    docs = load_transcription(media_loader, output_path_transcription)

    # if 'current_video' not in st.session_state:
    #     st.session_state.current_video = youtube_url
    # Main Content - Top Section
    col2, col3 = st.columns([3, 1])

    # Main Content - Middle Section
    video_slot = col2.empty()

    with col2:
        if isinstance(media_loader, UploadedMediaLoader):
            video_slot.video(uploaded_file)

        elif isinstance(media_loader, YouTubeLoader):
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

            if isinstance(media_loader, UploadedMediaLoader):
                video_slot.video(uploaded_file)
            elif isinstance(media_loader, YouTubeLoader):
                video_slot.video(youtube_url)

            raw_results = video_retriever.search(user_input)
            for i, result in enumerate(raw_results):
                text_content = result.node.text
                start_time = int(result.node.metadata['start'])

                full_youtube_url = f"{youtube_url}&t={start_time}s"

                if st.button(text_content, key=f"button_{i}"):
                    st.session_state.current_video = full_youtube_url
                    if isinstance(media_loader, UploadedMediaLoader):
                        video_slot.video(uploaded_file, start_time=start_time)

                    elif isinstance(media_loader, YouTubeLoader):
                        video_slot.video(youtube_url, start_time=start_time)

    with col2:
        chat_placeholder = st.empty()


        def on_btn_click():
            del st.session_state.past[:]
            del st.session_state.generated[:]

        def on_input_change():
            user_input = st.session_state.user_input
            st.session_state.past.append(user_input)

            # Generate response only for the latest input
            latest_response = generate_response(st.session_state['past'][-1])

            st.session_state.generated.append(latest_response)
            st.session_state.user_input = ""  # This will empty the "User Input:" text box


        if 'generated' not in st.session_state:
            st.session_state['generated'] = []
        if 'past' not in st.session_state:
            st.session_state['past'] = []

        with chat_placeholder.container():
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=f"{i}_user")

                # Displaying generated message
                message(st.session_state['generated'][i], key=f"{i}", allow_html=True, is_table=False)
            st.button("Clear message", on_click=on_btn_click)

        with st.container():
            st.text_input("User Input:", on_change=on_input_change, key="user_input")
