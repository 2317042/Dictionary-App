# app.py
from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# Frontend HTML
frontend_html = """
<!DOCTYPE html>
<html>
<head>
  <title>Dictionary App</title>
  <style>
    body { font-family: Arial; padding: 30px; background: #f0f0f0; }
    input, button { padding: 8px; margin: 5px; }
    #result { margin-top: 20px; }
  </style>
</head>
<body>
  <h1>📖 Dictionary App</h1>
  <input type="text" id="word" placeholder="Enter word" />
  <button onclick="searchWord()">Search</button>
  <div id="result"></div>

  <script>
    async function searchWord() {
      let word = document.getElementById('word').value;
      if (!word) return alert("Enter a word!");
      let res = await fetch('/search?word=' + word);
      let data = await res.json();
      let container = document.getElementById('result');
      container.innerHTML = '';
      if (data.error) {
        container.innerHTML = '<b>Error:</b> ' + data.error;
      } else {
        data.meanings.forEach(m => {
          container.innerHTML += `<div><b>${m.partOfSpeech}:</b> ${m.definitions.join(', ')}</div>`;
        });
      }
    }
  </script>
</body>
</html>
"""

# Route for frontend
@app.route('/')
def home():
    return render_template_string(frontend_html)

# Route for dictionary API
@app.route('/search')
def search():
    word = request.args.get('word')
    if not word:
        return jsonify({"error": "No word provided"}), 400
    try:
        # Free dictionary API
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        data = response.json()
        meanings = [{"partOfSpeech": m['partOfSpeech'], "definitions": [d['definition'] for d in m['definitions']]} 
                    for m in data[0]['meanings']]
        return jsonify({"word": word, "meanings": meanings})
    except:
        return jsonify({"error": "Word not found"}), 404

# Run Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
