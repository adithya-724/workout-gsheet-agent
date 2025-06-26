import requests
import os
from dotenv import load_dotenv
import json
import re

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def call_gemini_api(prompt, api_key=None, model="gemini-2.0-flash"):
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


# Example usage (remove or comment out in production)
TRANSCRIPT = """
Hey, so today’s the 25th of June.

I weighed in at 72.3 kilos this morning. My resting heart rate was around 60, and I checked my blood glucose—it was 92.

I drank about two and a half liters of water, and I think I had maybe 150 milligrams of caffeine—mostly from coffee.

I did a push workout in the evening. I’d say my strength felt about a 7 out of 10—not my best, but decent. Didn’t do cardio today though.

Step count was around 8500.

My morning readiness felt like a 6, energy throughout the day was a 7, hunger was manageable—maybe a 4—and stress was pretty low, I’d say around a 5.

No sickness or digestive issues today.

I went to bed at 11:30 PM and slept for 7 hours and 15 minutes. Sleep quality was a solid 8.

And yes, I stuck to the plan for the day.
"""


prompt = f"""
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
# print(call_gemini_api(prompt))
