import streamlit as st
from transcribe import load_model, transcribe_audio
import tempfile


st.title("Record Audio in Streamlit")


@st.cache_resource
def get_model():
    return load_model()


model = get_model()

uploaded_file = st.file_uploader(
    "Upload an audio file", type=["wav", "mp3", "ogg", "m4a"]
)
if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")
    st.success("Audio file uploaded successfully!")
    # Save the uploaded file to a temporary location

    with tempfile.NamedTemporaryFile(
        delete=False, suffix="." + uploaded_file.name.split(".")[-1]
    ) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    transcription = transcribe_audio(model, tmp_file_path)
    st.write(transcription)
