import os
import base64
import io
from dotenv import load_dotenv
from PIL import Image
import pyttsx3
import pytesseract
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import ctypes

load_dotenv()

api_key="AIzaSyD0l2NvnqRN7RBcPYibN3z7V3wNFevXEX4"
if not api_key:
    st.error("API key not found! Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

# Set page title, favicon, and layout
st.set_page_config(
    page_title="Perceiva - AI Assistant for Visually Impaired",
    layout="centered",
)

chat_model = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-1.5-pro")

st.sidebar.title("Select option for page navigation")
option = st.sidebar.radio("Go to", ["Scene Understanding", "Text Extraction", "Text to Speech"])

# Add description about the functionality in the sidebar
st.sidebar.markdown("""
### About the App

**Perceiva - AI Assistant for Visually Impaired**

This application is designed to assist visually impaired individuals by providing:

1. **Scene Understanding**: Analyzes and describes uploaded images in real-time to provide vivid and empathetic interpretations.
2. **Text Extraction**: Extracts text from uploaded images and converts it into speech using Text-to-Speech (TTS) technology.
3. **AI Chat Support**: Powered by Google Generative AI (Gemini), offering actionable insights and descriptions.

**Instructions**:
- Upload an image in **PNG, JPG, or JPEG** format.
- Navigate between the functionalities using the sidebar options.
- Use Text-to-Speech to listen to descriptions or extracted text.
""")

# Display different images based on the selected option
if option == "Scene Understanding":
    st.image(r"C:\Users\cgkis\Downloads\ai.jpg")
elif option == "Text Extraction":
    st.image(r"C:\Users\cgkis\Downloads\text.jpg",use_container_width=True)
elif option == "Text to Speech":
    st.image(r"C:\Users\cgkis\Downloads\text to speech.png",use_container_width=True)

# Conditionally show file uploader
uploaded_file = None
if option in ["Scene Understanding", "Text Extraction"]:
    uploaded_file = st.file_uploader("Upload an image file", type=["png", "jpg", "jpeg"])

# Convert button
def text_to_speech(text):
    ctypes.windll.ole32.CoInitialize(None)
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed
    engine.setProperty('volume', 1)  # Volume
    audio_file = "text-to-speech-local.mp3"
    try:
        engine.save_to_file(text, audio_file)
        engine.runAndWait()
        st.audio(audio_file, format="audio/mp3")
        return audio_file
    except Exception as e:
        st.error(f"Audio generation failed: {e}")

def real_time_scene_understanding(image_base64):
    hmessage = HumanMessage(
        content=[{
            "type": "text", 
            "text": """You are a real-time scene interpreter for visually impaired users. Your task is to analyze and describe images vividly, empathetically, and without technical jargon. Focus on delivering concise, actionable information that enhances understanding and safety."""},
            {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
        ]
    )
    try:
        response = chat_model.invoke([hmessage])
        response_text = response.content
        st.write(response_text)
        text_to_speech(response_text)
    except Exception as e:
        st.error(f"Scene understanding failed: {e}")

def text_extraction(uploaded_image):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\cgkis\Ocr_files\Tesseract-OCR\tesseract.exe"
    try:
        extracted_text = pytesseract.image_to_string(uploaded_image)
        st.write(extracted_text)
        text_to_speech(extracted_text)
    except Exception as e:
        st.error(f"Text extraction failed: {e}")

if uploaded_file is not None:
    # Open the image file using PIL
    image = Image.open(uploaded_file)

    # Display the image in the app
    st.image(image, caption="Uploaded Image", use_container_width=True)

    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Page Content
    if option == "Scene Understanding":
        if st.button("Click here for Scene understanding"):
            with st.spinner("Please be patient..."):
                real_time_scene_understanding(image_base64)

    elif option == "Text Extraction":
        if st.button("Click here to extract text"):
            with st.spinner("Please be patient..."):
                text_extraction(image)
else:
    if option in ["Scene Understanding", "Text Extraction"]:
        st.write("Please upload a valid image.")

if option == "Text to Speech":
    txt = st.text_area("Enter text")
    if st.button("Click here to convert the text to speech"):
        with st.spinner("Please be patient..."):
            text_to_speech(txt)
