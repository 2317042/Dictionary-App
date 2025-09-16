from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Dictionary Backend Running!"}

@app.get("/define")
def define_word(word: str):
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            data = response.json()
            meanings = []
            for meaning in data[0]["meanings"]:
                for definition in meaning["definitions"]:
                    meanings.append(definition["definition"])
            return {"word": word, "meanings": meanings}
        else:
            return {"word": word, "meanings": ["No definition found."]}
    except Exception as e:
        return {"error": str(e)}
