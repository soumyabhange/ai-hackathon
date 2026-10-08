import json


def create_rag_documents(endpoints):
    documents = []

    for endpoint in endpoints:

        methods = ", ".join(endpoint["method"]) if endpoint["method"] else "Not specified"

        parameters = ", ".join(endpoint["parameters"]) if endpoint["parameters"] else "None"

        document = {
            "endpoint": endpoint["endpoint"],
            "method": methods,
            "function": endpoint["function"],
            "parameters": parameters,
            "description": endpoint["description"]
        }

        documents.append(document)

    return documents


if __name__ == "__main__":

    from parser import parse_python_code

    test_code = """
from flask import Flask

app = Flask(__name__)

@app.route("/users", methods=["GET"])
def get_users():
    \"\"\"Get all users from the system.\"\"\"
    return {"users": []}

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    \"\"\"Get a specific user by ID.\"\"\"
    return {"user_id": user_id}

@app.route("/users", methods=["POST"])
def create_user():
    \"\"\"Create a new user.\"\"\"
    return {"message": "created"}
"""

    endpoints = parse_python_code(test_code)

    documents = create_rag_documents(endpoints)

    with open("rag_documents.json", "w", encoding="utf-8") as file:
        json.dump(documents, file, indent=4)

    print("RAG documents created successfully!")
    print("Saved to: rag_documents.json")