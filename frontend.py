from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dictionary App</title>
</head>
<body>
    <h2>Dictionary App</h2>
    <form method="post" action="/search">
        <input type="text" name="word" placeholder="Enter a word" required>
        <button type="submit">Search</button>
    </form>

    {% if result %}
        <h3>Results for '{{ result.word }}'</h3>
        <ul>
        {% for meaning in result.meanings %}
            <li>{{ meaning }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/search", methods=["POST"])
def search():
    word = request.form.get("word")
    response = requests.get(f"{BACKEND_URL}/define", params={"word": word})
    return render_template_string(HTML_TEMPLATE, result=response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
