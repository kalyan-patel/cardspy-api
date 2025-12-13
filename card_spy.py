import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()

BASE_API_URL = "https://api.clashroyale.com/v1"

CLASH_ROYALE_API_TOKEN = os.getenv("CLASH_ROYALE_API_TOKEN")
if not CLASH_ROYALE_API_TOKEN:
    raise RuntimeError("Missing <CLASH_ROYALE_API_TOKEN>")


def query_api(path: str, params: dict={}):
    resp = requests.get(
        BASE_API_URL + path,
        headers={
            "Authorization": f"Bearer {CLASH_ROYALE_API_TOKEN}"
        },
        params=params
    )

    if resp.status_code != 200:
        raise RuntimeError(f"API request failed ({resp.status_code}): {resp.text}")
    
    data = resp.json()
    return data["items"] if isinstance(data, dict) and "items" in data else data


def encode_tag(tag: str):
    if not tag.startswith("#"):
        return tag
    return "%23" + tag[1:]


def get_last_deck(player_name: str, clan_name: str):

    clans = query_api("/clans", params={ "name": clan_name })
    
    for clan in clans:
        if clan["name"] == clan_name:    # Need exact match since API query is fuzzy

            tag = clan["tag"]
            members = query_api(f"/clans/{encode_tag(tag)}/members")

            for member in members:
                if member["name"] == player_name:
                    return last_pvp_deck(member["tag"])


def last_pvp_deck(player_tag: str):

    icon_keys = {0: "medium", 1: "evolutionMedium", 2: "heroMedium"}

    logs = query_api(f"/players/{encode_tag(player_tag)}/battlelog")

    first_pvp_log = next((log for log in logs if log["type"] == "PvP"), None)
    player = first_pvp_log["team"][0]
    cards = player["cards"]

    deck = []
    for card in cards:
        # Get appropriate image using "evolutionLevel" field (normal vs evo vs hero)
        icon_idx = card["evolutionLevel"] if "evolutionLevel" in card else 0
        img_url = card["iconUrls"][icon_keys[icon_idx]]

        deck.append({
            "name": card["name"],
            "img": img_url
        })
    
    return deck