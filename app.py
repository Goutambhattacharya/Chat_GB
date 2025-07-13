from flask import Flask, render_template, request, session
from chatbot_logic import ask_bot
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")  # Needed for session

@app.route("/", methods=["GET", "POST"])
def index():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        user_input = request.form["user_input"]
        try:
            response = ask_bot(user_input)
        except Exception as e:
            response = f"⚠️ Error occurred: {str(e)}"
            print("Error in ask_bot:", e)  # Logged to error log

        session["chat_history"].append({"sender": "user", "text": user_input})
        session["chat_history"].append({"sender": "bot", "text": response})
        session.modified = True

    return render_template("index.html", chat_history=session["chat_history"])

if __name__ == "__main__":
    app.run(debug=True)
