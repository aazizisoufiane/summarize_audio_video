# Summarize Audio and Video with Semantic Retrieval, Chatbot, and LLM

## Description

This project is an all-in-one solution for audio and video content analysis:

1. **Summarization**: Generates concise summaries using advanced Natural Language Processing, powered by HuggingFace Transformers.
2. **Semantic Retrieval**: Enables you to find specific words, phrases, or segments, thanks to Whisper Timestamped by Linto.
3. **Chatbot Interface**: Features a chatbot that can answer queries about the audio or video content, leveraging Language Models for Machines (LLM).

The project is built using Python and integrates various libraries including Whisper Timestamped, HuggingFace Transformers, and Streamlit for a seamless user experience.

## Project Structure

```plaintext
.
├── Dockerfile                   # Dockerfile for setting up the environment
├── LICENSE                      # License file
├── README.md                    # This README file
├── YoutubeAudios                # Directory containing YouTube audio files
├── _requirements.txt            # Requirements file
├── app.py                       # Streamlit application file
├── config.py                    # Configuration file
├── keyword_retriever            # Module for keyword retrieval
│   └── keyword_retreiver.py     # Keyword retriever script
├── logger.py                    # Logging utility
├── notebooks                    # Jupyter notebooks for development and testing
├── pdf_test.py                  # PDF testing script
├── query_service                # Query service module
│   └── query_engine.py          # Query engine script
├── requirements.txt             # Requirements file
├── resource_loader              # Resource loader module
│   ├── json_loader.py           # JSON loader script
│   ├── linkedin_loader.py       # LinkedIn loader script
│   ├── uploaded_video_loader.py # Uploaded video loader script
│   ├── video_loader_interface.py# Video loader interface script
│   └── youtube_loader.py        # YouTube loader script
├── summarization_service        # Summarization service module
│   └── summarizer.py            # Summarizer script
├── transcription_service        # Transcription service module
│   └── transcriber.py           # Transcriber script
└── utils.py                     # Utility functions

```

## Prerequisites

- Python 3.8+
- Docker (optional)

## Built With

- [Llama_index](https://www.llamaindex.ai/) Framework for  LLM application
- [Whisper Timestamped](https://github.com/linto-ai/whisper-timestamped) - For semantic retrieval and timestamping
- [HuggingFace Transformers](https://huggingface.co/transformers/) - For summarization and NLP
- [Streamlit](https://streamlit.io/) - For the web interface


## Setup and Installation
## Setup and Installation

There are two methods to get the project up and running:

### Method 1: Using Docker

1. Clone the repository.
2. Navigate to the project directory.
3. Build the Docker image:
    ```bash
    docker build -t summarizer .
    ```
4. Run the Docker container:
    ```bash
    docker run -p 8501:8501 summarizer
    ```
5. Open your web browser and go to `http://localhost:8501`.

### Method 2: Using Python Environment

1. Clone the repository.
2. Navigate to the project directory.
3. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
5. Open your web browser and go to `http://localhost:8501`.
### Using Python Environment

1. Clone the repository.
2. Navigate to the project directory.
3. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## Usage

1. Open the Streamlit app in your web browser.
2. Follow the instructions on the screen to upload or specify your audio/video content.
3. Click "Submit" to generate a summary, perform semantic retrieval, or interact with the chatbot.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
