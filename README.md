
# Multi-Modal AI 

This repository contains a basic project of a multi-modal artificial intelligence (AI), developed in Python. The system enables interaction with the AI through multiple modalities, including text, audio, images, and PDF documents.

## Features

- **Text-based interaction with Mistral**: You can send questions or requests to the Mistral model and receive text responses.
- **Audio recognition and processing**: Allows voice input, which is transcribed to text for Mistral to interpret.
- **PDF document analysis**: The system can load and understand PDF documents, answering specific questions about their content.
- **Image description**: You can upload images, and the model will automatically generate a description.

## Technologies

- **Python**: Main development language.
- **Streamlit**: Tecnologia usada para la interfaz visual
- **Transformers**: Dependency to execute the model
- **Chromadb**: saves messages between the user and the AI

## Installation

1. Clone the repository:

```bash
git clone https://github.com/JoakinGC/multi-modal-chat.git
cd multi-modal-chat
```

2. Create a virtual environment and install dependencies:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

3. Donwload modal in ``modals/``:

https://huggingface.co/TheBloke
https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF


4. Start the web server:

```bash
streamlit run .\app.py
```

5. Open your browser at `http://localhost:8501/` to interact with the AI.

## Usage

1. **Text interaction**: Write your questions directly in the text field on the web interface.
2. **Voice interaction**: Click the record button to provide audio input. The system will transcribe it and generate a response.
3. **PDF analysis**: Upload a PDF file and ask questions about its content.
4. **Image analysis**: Upload an image, and the model will generate a description.


## License

This project is licensed under the [MIT License](LICENSE).

