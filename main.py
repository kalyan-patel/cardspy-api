from fastapi import FastAPI
from pydantic import BaseModel
from card_spy import get_last_deck
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
        "deck": get_last_deck(req.player, req.clan)
    }
