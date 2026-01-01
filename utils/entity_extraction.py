import requests
import json
import re
import streamlit as st


# Get the Gemini API key from environment variable
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]


def call_gemini_api(prompt, api_key=None, model="gemini-2.5-flash"):
    """
    Makes an API call to Google Gemini with the given prompt.
    Args:
        prompt (str): The input prompt to send to Gemini.
        api_key (str): Your Google Gemini API key. If None, uses GEMINI_API_KEY from environment.
        model (str): The Gemini model to use (default: "gemini-2.0-flash").
    Returns:
        dict: The JSON-decoded response from the Gemini API, or None if parsing fails.
    """

    if api_key is None:
        api_key = GEMINI_API_KEY
    if not api_key:
        raise ValueError(
            "Google Gemini API key not found. Please set GEMINI_API_KEY in your .env file."
        )
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    try:
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        # Attempt to extract JSON substring from the text
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            json_str = match.group(0)
            json_output = json.loads(json_str)
        else:
            json_output = None
    except (KeyError, IndexError, json.JSONDecodeError):
        json_output = None
    return json_output
