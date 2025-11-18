import streamlit as st
from utils.transcribe import load_model, transcribe_audio
import tempfile
from utils.entity_extraction import call_gemini_api
from utils.write_to_gsheet import add_values_to_sheet
import yaml

st.subheader("Describe your day")

# Short instruction for mobile + collapsible full details/example
SHORT_INSTR = "Tap record and speak the fields (comma or newline separated). Then tap 'Process' to submit."
st.info(SHORT_INSTR)

with st.expander("Full fields / example"):
    st.write(
        "- Date\n"
        "- AM Weight (Kg)\n"
        "- RHR\n"
        "- Blood Glucose\n"
        "- Est Water (L)\n"
        "- Caffeine (MG)\n"
        "- Session Performed\n"
        "- Strength (1-10)\n"
        "- Cardio Performed\n"
        "- Daily Steps\n"
        "- Morning Readiness (1-10)\n"
        "- Energy (1-10)\n"
        "- Hunger (1-10)\n"
        "- Stress (1-10)\n"
        "- Ill/Sickness (Y/N)\n"
        "- Digestion Issue?\n"
        "- Bedtime\n"
        "- Duration (Hrs:Mins)\n"
        "- Quality/Efficiency (1-10)\n"
        "- Have you stuck to the plan? (Y/N)\n\n"
        "Example:\n2025-11-18, 72.5, 58, 5.6, 2.5, 100, Yes, 8, Yes, 8500, 7, 6, 4, 3, N, No, 23:00, 7:30, 8, Y"
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


audio = st.audio_input("Record your entry")

# uploaded_file = st.file_uploader(
#     "Upload an audio file", type=["wav", "mp3", "ogg", "m4a"]
# )

if audio is not None:
    process_btn = st.button("Process")
    if process_btn:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix="." + audio.name.split(".")[-1]
        ) as tmp_file:
            tmp_file.write(audio.read())
            tmp_file_path = tmp_file.name

        with st.spinner("Transcribing audio..."):
            transcription = transcribe_audio(model, tmp_file_path)

        with st.expander("Transcript", expanded=False):
            st.write(transcription)

        prompt = prompt.format(TRANSCRIPT=transcription)
        with st.spinner("Extracting entities..."):
            json_op = call_gemini_api(prompt)

        with st.expander("Extracted data (preview)", expanded=False):
            st.json(json_op)

        with st.spinner("Writing data to sheet"):
            add_values_to_sheet(json_op)
