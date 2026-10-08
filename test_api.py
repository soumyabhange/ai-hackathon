from flask import Flask, request
app = Flask(__name__)
@app.route("/users", methods=["GET"])
def get_users():
    return {"users": []}
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return {
        "id": user_id,
        "name": "John"
    }
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    return {
        "message": "User created",
        "user": data
    }
if __name__ == "__main__":
    app.run(debug=True)