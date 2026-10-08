import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found")
    exit()

# Connect to Gemini
client = genai.Client(api_key=api_key)

# Example API code
api_code = """
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def get_users():
    return {"users": ["Alice", "Bob"]}

@app.post("/users")
def create_user(name: str):
    return {"message": f"User {name} created"}
"""

# Ask Gemini to generate documentation
prompt = f"""
You are an API documentation generator.

Analyze the following API code and create clear developer documentation.

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

API CODE:
{api_code}
"""

try:
    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt
    )
except Exception as e:
    print("3.7 Flash unavailable. Trying backup model...")
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

print("\n========== GENERATED API DOCUMENTATION ==========\n")
print(response.text)