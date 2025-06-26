# transcribe_audio.py

import whisper

# Load the English-only model (small and accurate)
model = whisper.load_model("base.en")

# Path to your audio file (WAV, MP3, MP4, M4A, etc.)
audio_path = "sample.mp3"

# Transcribe the audio
result = model.transcribe(
    audio_path, language="en", fp16=False
)  # set fp16=False for CPU

# Print the result
print("Transcription:")
print(result["text"])
