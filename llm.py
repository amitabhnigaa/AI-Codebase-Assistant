import os
import streamlit as st
from google import genai

# -----------------------------
# Load API Key
# -----------------------------
API_KEY = os.getenv("GEMINI_API_KEY")

# Show whether Streamlit Cloud loaded the key
if API_KEY:
    st.sidebar.success(f"✅ API Key Loaded: {API_KEY[:10]}...")
else:
    st.sidebar.error("❌ GEMINI_API_KEY NOT FOUND")

# Create Gemini client
client = genai.Client(api_key=API_KEY)


def ask_gemini(prompt: str) -> str:
    """
    Send prompt to Gemini and return response.
    Also displays detailed errors in Streamlit.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        if response.text:
            return response.text

        return "No response received."

    except Exception as e:
        # Print full error in terminal/logs
        print("Gemini Error:", repr(e))

        # Show full error inside Streamlit
        st.error(f"Gemini Error:\n\n{repr(e)}")

        return f"Gemini Error:\n{repr(e)}"