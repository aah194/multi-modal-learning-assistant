import streamlit as st
import os
import speech_recognition as sr
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from PIL import Image
from google import genai
from modules.text_chunker import create_chunks
from modules.embeddings import create_embeddings, model
from modules.vector_store import create_vector_store
from modules.search import search_chunks
from modules.gemini_helper import get_answer
from modules.image_helper import analyze_image
from modules.multimodal_helper import multimodal_answer
from modules.voice_helper import speech_to_text, text_to_speech,stop_speaking

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="Multi-Modal Learning Assistant",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Multi-Modal Learning Assistant")
st.subheader("Phase 6.0 - Voice Assistant")

tab1, tab2, tab3 = st.tabs(
    [
        "📄 PDF Chat",
        "🖼️ Image Understanding",
        "🎤 Voice Assistant"
    ]
)

# ====================================================
# PDF CHAT
# ====================================================

with tab1:

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "current_pdfs" not in st.session_state:
        st.session_state.current_pdfs = None

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True,
        key="pdfs"
    )

    if uploaded_files:

        pdf_names = [file.name for file in uploaded_files]

        if st.session_state.current_pdfs != pdf_names:

            st.session_state.current_pdfs = pdf_names
            st.session_state.messages = []

            if "chunks" in st.session_state:
                del st.session_state["chunks"]

            if "index" in st.session_state:
                del st.session_state["index"]

        if "chunks" not in st.session_state:

            text = ""

            for pdf in uploaded_files:

                reader = PdfReader(pdf)

                for page in reader.pages:

                    extracted = page.extract_text()

                    if extracted:
                        text += extracted

            chunks = create_chunks(text)

            embeddings = create_embeddings(chunks)

            index = create_vector_store(embeddings)

            st.session_state.chunks = chunks
            st.session_state.index = index

        chunks = st.session_state.chunks
        index = st.session_state.index

        st.success(
            f"Knowledge Base Ready ({len(chunks)} chunks)"
        )

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):
                st.write(message["content"])

        question = st.chat_input(
            "Ask a question..."
        )

        if question:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.chat_message("user"):
                st.write(question)

            query_embedding = model.encode(question)

            retrieved_chunks = search_chunks(
                query_embedding,
                index,
                chunks
            )

            context = "\n\n".join(retrieved_chunks)

            history = ""

            for msg in st.session_state.messages[-6:]:

                history += (
                    f"{msg['role']}: "
                    f"{msg['content']}\n"
                )

            answer = get_answer(
                context=context,
                question=question,
                chat_history=history,
                api_key=api_key
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            with st.chat_message("assistant"):
                st.write(answer)

# ====================================================
# IMAGE UNDERSTANDING
# ====================================================

with tab2:

    image_file = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"],
        key="image"
    )

    if image_file:

        image = Image.open(image_file)

        st.image(
            image,
            width=300
        )

        prompt = st.text_input(
            "Ask about image",
            value="Describe the image"
        )

        if st.button("Analyze Image"):

            response = analyze_image(
                image_file,
                prompt,
                api_key
            )

            st.write(response)
# ====================================================
# VOICE ASSISTANT
# ====================================================
with tab3:

    st.write(
        "Click record and speak."
    )

    if st.button(
        "🎤 Record Voice"
    ):

        recognizer = sr.Recognizer()

        with sr.Microphone() as source:

            st.info(
                "Listening..."
            )

            audio = recognizer.listen(
                source,
                timeout=10
            )

        try:

            text = recognizer.recognize_google(
                audio
            )

            st.success(
                f"You said: {text}"
            )

            client = genai.Client(
                api_key=api_key
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=text
            )

            st.session_state.voice_answer = (
                response.text
            )

        except Exception as e:

            st.error(
                str(e)
            )

    if "voice_answer" in st.session_state:

        st.subheader(
            "AI Response"
        )

        st.write(
            st.session_state.voice_answer
        )

    if st.button(
        "🔊 Speak Answer"
    ):

        text_to_speech(
        st.session_state.voice_answer
    )

    if st.button(
        "⏹ Stop Speaking"
    ):

        stop_speaking()
        
            