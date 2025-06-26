# transcribe_audio.py
import whisper


# Load the English-only model (small and accurate)
def load_model():
    model = whisper.load_model("base.en")
    return model


def transcribe_audio(model, audio_path):
    # model = load_model()
    result = model.transcribe(
        audio_path, language="en", fp16=True
    )  # set fp16=False for CPU

    return result["text"]


# model = load_model()
# print(transcribe_audio(model, "sample.mp3"))
