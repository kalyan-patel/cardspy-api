from fastapi import FastAPI
from pydantic import BaseModel
from card_spy import get_last_deck

app = FastAPI()

class DeckRequest(BaseModel):
    player: str
    clan: str

@app.post("/deck")
def deck(req: DeckRequest):
    return {
        "deck": get_last_deck(req.player, req.clan)
    }
