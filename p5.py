from flask import Flask, request, jsonify, render_template_string
import requests
from threading import Timer
import webbrowser

app = Flask(__name__)

# Frontend HTML
frontend_html = """
<!DOCTYPE html>
<html>
<head>
  <title>Dictionary App</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 30px; background: #f0f0f0; }
    h1 { color: #333; }
    input, button { padding: 8px; margin: 5px; }
    #result { margin-top: 20px; }
    .meaning { background: #fff; padding: 10px; border-radius: 5px; margin: 5px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
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
      let res = await fetch('/define?word=' + word);
      let data = await res.json();
      let container = document.getElementById('result');
      container.innerHTML = '';
      if(data.error){
        container.innerHTML = '<div class="meaning">' + data.error + '</div>';
      } else {
        data.meanings.forEach(m => {
          container.innerHTML += '<div class="meaning"><strong>' + m.partOfSpeech + ':</strong> ' + m.definition + '</div>';
        });
      }
    }
  </script>
</body>
</html>
"""

# Frontend route
@app.route('/')
def home():
    return render_template_string(frontend_html)

# Dictionary API route
@app.route('/define')
def define_word():
    word = request.args.get('word')
    if not word:
        return jsonify({"error": "No word provided"})
    
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        data = response.json()
        meanings = [{"partOfSpeech": m['partOfSpeech'], "definition": m['definitions'][0]['definition']} 
                    for m in data[0]['meanings']]
        return jsonify({"meanings": meanings})
    except:
        return jsonify({"error": "Word not found or API error"})

# Auto open browser when server starts
if __name__ == "__main__":
    port = 5000
    Timer(1, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()
    app.run(host="0.0.0.0", port=port, debug=True)
