import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="AI API Documentation Generator",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Load API key
# -----------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found. Please check your .env file.")
    st.stop()

# -----------------------------
# Connect to Gemini
# -----------------------------

client = genai.Client(api_key=api_key)


# -----------------------------
# Documentation generator
# -----------------------------

def generate_documentation(api_code):

    prompt = f"""
You are an expert API documentation generator.

Analyze the following API source code and create clear,
accurate developer documentation.

Include:

1. API overview
2. Available endpoints
3. HTTP methods
4. Endpoint paths
5. Parameters
6. Request examples
7. Response examples
8. Possible errors

Format the result using Markdown.

Do not invent endpoints that are not present in the code.

API SOURCE CODE:
{api_code}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt
        )

    except Exception:
        st.warning("Primary model unavailable. Trying backup model...")

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

    return response.text


# -----------------------------
# User Interface
# -----------------------------

st.title("🤖 AI API Documentation Generator")

st.write(
    "Upload your API source code and let AI automatically "
    "generate developer-friendly documentation."
)

st.divider()

# File upload
uploaded_file = st.file_uploader(
    "📁 Upload your API source code",
    type=["py", "js", "java", "ts"]
)

# Generate button
if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    # Read uploaded file
    api_code = uploaded_file.read().decode("utf-8")

    # Show source code
    with st.expander("👀 View uploaded source code"):
        st.code(api_code, language="python")

    if st.button("🚀 Generate Documentation"):

        with st.spinner("AI is analyzing your API..."):

            documentation = generate_documentation(api_code)

        st.success("Documentation generated successfully!")

        st.divider()

        st.subheader("📚 Generated API Documentation")

        st.markdown(documentation)

        # Download button
        st.download_button(
            label="⬇️ Download Documentation",
            data=documentation,
            file_name="api_documentation.md",
            mime="text/markdown"
        )