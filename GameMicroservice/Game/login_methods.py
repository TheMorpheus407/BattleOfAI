import GameMicroservice.settings as settings
import requests
import json

def validate_login(player_id, player_token):
    player_token = player_token.replace("'", '"')
    tokens = json.loads(player_token)
    my_data = {
        "userid": player_id,
        "token": tokens[0],
        "session_token": tokens[1]
    }
    resp = requests.post(settings.account_management_url + "iam/validateToken", json=my_data)
    return resp.status_code == 200 and resp.json()["success"]