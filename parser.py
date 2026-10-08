import ast


def parse_python_code(code):
    tree = ast.parse(code)

    endpoints = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            endpoint = {
                "function": node.name,
                "method": None,
                "endpoint": None,
                "parameters": [],
                "description": ""
            }

            # Get function parameters
            for arg in node.args.args:
                endpoint["parameters"].append(arg.arg)

            # Get function description/docstring
            endpoint["description"] = ast.get_docstring(node) or ""

            # Look for Flask route decorators
            for decorator in node.decorator_list:

                if isinstance(decorator, ast.Call):

                    if isinstance(decorator.func, ast.Attribute):

                        if decorator.func.attr == "route":

                            # Get endpoint path
                            if decorator.args:
                                endpoint["endpoint"] = ast.literal_eval(
                                    decorator.args[0]
                                )

                            # Get HTTP method
                            for keyword in decorator.keywords:

                                if keyword.arg == "methods":
                                    endpoint["method"] = ast.literal_eval(
                                        keyword.value
                                    )

            if endpoint["endpoint"]:
                endpoints.append(endpoint)

    return endpoints


if __name__ == "__main__":

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

    result = parse_python_code(test_code)

    print(result)