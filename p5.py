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
        body { font-family: Arial, sans-serif; margin: 30px; background: #f7f7f7; }
        h1 { color: #333; }
        input, button { padding: 8px; margin: 5px; }
        .definition { background: #fff; padding: 10px; margin: 5px 0; border-radius: 6px; }
    </style>
</head>
<body>
    <h1>📖 Dictionary App</h1>
    <input type="text" id="word" placeholder="Enter word">
    <button onclick="searchWord()">Search</button>

    <div id="results" style="margin-top:20px;"></div>

    <script>
        async function searchWord() {
            let word = document.getElementById('word').value;
            if (!word) return alert('Enter a word!');
            let res = await fetch('/define?word=' + word);
            let data = await res.json();
            let container = document.getElementById('results');
            container.innerHTML = '';
            if (data.error) {
                container.innerHTML = '<p>' + data.error + '</p>';
                return;
            }
            data[0].meanings.forEach(m => {
                let html = '<div class="definition"><h3>' + m.partOfSpeech + '</h3><ul>';
                m.definitions.forEach(d => {
                    html += '<li>' + d.definition + '</li>';
                });
                html += '</ul></div>';
                container.innerHTML += html;
            });
        }
    </script>
</body>
</html>
"""

# Route to serve frontend
@app.route('/')
def home():
    return render_template_string(frontend_html)

# Route to get word meaning
@app.route('/define', methods=['GET'])
def define_word():
    word = request.args.get('word')
    if not word:
        return jsonify({"error": "No word provided"}), 400
    response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
    if response.status_code != 200:
        return jsonify({"error": "Word not found"}), 404
    return jsonify(response.json())

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
