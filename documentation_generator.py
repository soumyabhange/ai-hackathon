import os
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found")
    exit()

# Connect to Gemini
client = genai.Client(api_key=api_key)


def generate_documentation(api_code):
    """
    Send API source code to Gemini and generate documentation.
    """

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

    # Try primary model
    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt
        )

    # If primary model is unavailable, use backup
    except Exception:
        print("Primary model unavailable. Trying backup model...")

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

    return response.text


# Test API code
# Read API source code from a file
file_name = "sample_api.py"

with open(file_name, "r", encoding="utf-8") as file:
    api_code = file.read()


# Generate documentation
documentation = generate_documentation(api_code)

print("\n========== GENERATED API DOCUMENTATION ==========\n")
print(documentation)