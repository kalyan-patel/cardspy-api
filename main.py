from fastapi import FastAPI
from pydantic import BaseModel
from spy_deck import spy_deck
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for now, restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DeckRequest(BaseModel):
    player: str
    clan: str

@app.post("/deck")
def deck(req: DeckRequest):
    return {
        "deck": spy_deck(req.player, req.clan)
    }
