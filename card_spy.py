import json
import requests


CLASH_ROYALE_API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6Ijc3N2Q3NjVmLTZhZDktNDJkNi1iZjBiLWQ3ZWM2MmY4YjU4NiIsImlhdCI6MTc2NTU1Nzc2OCwic3ViIjoiZGV2ZWxvcGVyLzYzYzQwZjA0LTNiMmUtYzJlMi1jNjNhLTU2NDFiYTA1ZjQ5YyIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIyNC42Mi4xNDEuMTkxIl0sInR5cGUiOiJjbGllbnQifV19.ON0aOt7anGd58zkCq8Cbyss9Zy2CPyKhcDkP4Dp9dzpN-t6VVjDwaHmgsF8-T2y8-UzktF8NYmg4kw8UKFMzsA"
BASE_API_URL = "https://api.clashroyale.com/v1"


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


# logs = query_api(f"/players/{encode_tag("#VL2VYURJ0")}/battlelog")
# print(len(logs))