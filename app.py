import streamlit as st
from utils.transcribe import load_model, transcribe_audio
import tempfile
from utils.entity_extraction import call_gemini_api
from utils.write_to_gsheet import add_values_to_sheet
import yaml

st.subheader("Describe your day")

# Provide spoken-field instructions for the audio input
st.info(
    "When recording your audio, please speak the following fields in order, "
    "separated by commas or new lines:\n\n"
    "Date, AM Weight (Kg), RHR, Blood Glucose, Est Water (L), Caffeine (MG), "
    "Session Performed, Strength (1-10), Cardio Performed, Daily Steps, "
    "Morning Readiness (1-10), Energy (1-10), Hunger (1-10), Stress (1-10), "
    "Ill/Sickness (Y/N), Digestion Issue?, Bedtime, Duration (Hrs:Mins), "
    "Quality/Efficiency (1-10), Have you stuck to the plan? (Y/N)\n\n"
    "Example (speak or read): '2025-11-18, 72.5, 58, 5.6, 2.5, 100, Yes, 8, Yes, 8500, 7, 6, 4, 3, N, No, 23:00, 7:30, 8, Y'"
)

# Load prompt from YAML
with open("prompts/app.yaml", "r", encoding="utf-8") as f:
    prompt_yaml = yaml.safe_load(f)
    prompt = prompt_yaml["prompt"]


@st.cache_resource
def get_model():
    return load_model()


with st.spinner("Loading model..."):
    model = get_model()


audio = st.audio_input("")

# uploaded_file = st.file_uploader(
#     "Upload an audio file", type=["wav", "mp3", "ogg", "m4a"]
# )

if audio is not None:
    process_btn = st.button("process")
    # st.audio(audio, format="audio/wav")
    # st.success("Audio file uploaded successfully!")
    # Save the uploaded file to a temporary location
    if process_btn:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix="." + audio.name.split(".")[-1]
        ) as tmp_file:
            tmp_file.write(audio.read())
            tmp_file_path = tmp_file.name

        with st.spinner("Transcribing audio..."):
            transcription = transcribe_audio(model, tmp_file_path)
        st.subheader("**Transcript**")
        st.write(transcription)

        prompt = prompt.format(TRANSCRIPT=transcription)
        with st.spinner("Extracting entities..."):
            json_op = call_gemini_api(prompt)
        # st.write(json_op)
        with st.spinner("Writing data to sheet"):
            add_values_to_sheet(json_op)
