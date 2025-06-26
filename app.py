import streamlit as st
from transcribe import load_model, transcribe_audio
import tempfile
from entity_extraction import call_gemini_api

st.title("Record Audio in Streamlit")

prompt = """
You are an assistant that extracts structured health and performance data from a free-form audio diary.

The transcript you receive is a spoken summary of the person's day, health metrics, energy levels, and sleep.

Your job is to extract the following fields as JSON. Some fields may not be mentioned — in that case, set the value to null.

Output only valid JSON. No extra explanation.

Here are the fields you must extract:

 "date": "YYYY-MM-DD",
  "am_weight_kg": 0,
  "estimated_water_intake_liters": 0,
  "caffeine_mg": 0,
  "session_performed": "string (e.g. Upper Body, Yoga, Rest Day)",
  "strength_rating": 0,                  // 1 to 10
  "cardio_performed": "string",
  "daily_steps": 0,
  "morning_readiness": 0,               // 1 to 10
  "energy_level": 0,                    // 1 to 10
  "hunger_level": 0,                    // 1 to 10
  "stress_level": 0,                    // 1 to 10
  "ill_or_sick": "Y/N",
  "digestion_issue": "Y/N",
  "bedtime": "HH:MM (24h format)",     
  "sleep_duration": "HH:MM",
  "sleep_quality": 0,                   // 1 to 10
  "stuck_to_plan": "Y/N"

Make sure values like "Y" or "N" are capitalized. If the speaker said they don’t remember, use null.

Transcript:

{TRANSCRIPT}

"""


@st.cache_resource
def get_model():
    return load_model()


with st.spinner("Loading model..."):
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

    with st.spinner("Transcribing audio..."):
        transcription = transcribe_audio(model, tmp_file_path)
    st.write(transcription)
    prompt = prompt.format(TRANSCRIPT=transcription)
    with st.spinner("Extracting entities..."):
        json_op = call_gemini_api(prompt)
    st.write(json_op)
