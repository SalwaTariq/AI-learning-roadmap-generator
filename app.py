import os
import time
import streamlit as st
from google import genai
from google.genai import types

MODEL = "gemini-3.8-flash"

st.set_page_config(page_title="AI Roadmap Generator", page_icon="🗺️")
st.title("🗺️ AI Learning Roadmap Generator")


def get_api_key():
    """Read the key from an environment variable (Colab/local) or Streamlit secrets (Streamlit Cloud)."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


api_key = get_api_key()
if not api_key:
    st.error("GEMINI_API_KEY not found. Set it as an environment variable or in Streamlit secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

def generate_with_retry(prompt, retries=4):
    """Call Gemini, retrying with a growing wait when the model is overloaded (503/429)."""
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="You are an expert career and learning mentor.",
                    temperature=0.7,
                ),
            )
            return response.text
        except Exception as e:
            temporary = any(code in str(e) for code in ("503", "429", "UNAVAILABLE"))
            if temporary and attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))  # waits 2s, 4s, 8s
                continue
            raise


field = st.text_input("What do you want to learn?", placeholder="e.g. Data Science")
level = st.selectbox("Your current level", ["Beginner", "Intermediate", "Advanced"])
duration = st.slider("Time available (weeks)", 1, 52, 12)
hours = st.slider("Hours per week", 1, 40, 8)

if st.button("Generate Roadmap"):
    if not field.strip():
        st.warning("Please enter a field first.")
    else:
        prompt = f"""
Create a detailed learning roadmap for: {field}
Skill level: {level}
Total time: {duration} weeks, {hours} hours per week.

Format:
1. A short overview
2. A week-by-week (or phase-by-phase) plan with topics
3. Recommended free resources for each phase
4. One hands-on project per phase
5. Final tips to stay on track
Use clean Markdown.
"""
        with st.spinner("Building your roadmap..."):
            try:
                roadmap = generate_with_retry(prompt)
                st.markdown(roadmap)
                st.download_button("Download roadmap", roadmap, file_name="roadmap.md")
            except Exception as e:
                st.error(f"Error: {e}")
   
   
