import requests
import time
import json

url = "http://0.0.0.0:1337/api/"
account_management_url = "http://0.0.0.0:1338/api/"

#CAREFUL!!! NEVER PUSH CODE TO GITHUB ETC WHEN IT CONTAINS YOUR PASSWORD!!!!!
username = "Morpheus2" #TODO CHANGE!
password = "asdf_1234" #TODO CHANGE!

'''If True, you will - if available - rejoin a game which has already started but is not finished yet.'''
play_games_i_already_left = True

def turn(board, symbol):
    '''
    ITS YOUR TURN TO CODE THE AI!
    :param board: Contains the current state of the game
    :param symbol: Contains your symbol on the board - either X if you are the first player or O if you are the 2nd.
    :return: pos_x, pos_y where your AI wants to place a stone
    '''
    #TODO CODE!
    for i in range(8):
        for j in range(8):
            if free(i, j, board):
                return i, j

def free(x, y, board):
    if board[x][y] == '#':
        return True
    return False

def create_game():
    '''
    creates a game and returns the game id
    :return: the game id
    '''
    resp = requests.post(url + "games/createGame", json={"game_name": "Core"})
    assert resp.status_code == 200
    return int(resp.text)

def register_player(game_id, player_id, token):
    '''
    Registers the player for a match by id
    :param game_id: The match to register on
    :param player_id: The id of the player
    :param token: Login-Token for the player
    '''
    resp = requests.post(url+"games/"+str(game_id) + "/registerPlayer", json={"id": player_id, "token": token})
    assert resp.status_code == 200
    return 'true' in resp.text

def login(username, password):
    '''
    Logs a user in with credentials of the registration for obtaining valid credentials for playing a game.
    :param username: username for logging in. NOT THE PLAYER ID!!!
    :param password: password for logging in. NOT THE TOKEN.
    :return: A tuple containing player_id and login token. Credentials are valid for 1 day.
    '''
    login_data = {
        "username": username,
        "password": password
    }
    resp = requests.post(account_management_url + "iam/login", json=login_data)
    if not resp.status_code == 200:
        exit("Account Management temporarily unavailable")
    if resp.json()["userid"] is None or resp.json()["token"] is None or resp.json()["session_token"] is None:
        exit("Invalid login credentials")
    return (resp.json()["userid"], str([resp.json()["token"], resp.json()["session_token"]]))

def get_symbol(active_player):
    return 'XO'[active_player]

def check_and_update_token(playerid, token):
    unwrapped_token = token.replace("['", "").replace("']", "").split("', '")
    data = {
        "userid": playerid,
        "token": unwrapped_token[0],
        "session_token": unwrapped_token[1]
    }
    resp = requests.post(account_management_url + "iam/validateToken", json=data)
    if not resp.status_code == 200 or resp.json()["success"] == False:
        return login(username, password)[1]
    return token

def play(username, password):
    '''
    Plays the game for you! (Make sure to enter code in the turn-function.
    :param username: Your username like you registered.
    :param password: Your password of registration.
    :return: True if you won or False if lost.
    '''
    #LOGIN
    player_id, token = login(username, password)
    print("logged in successfully")

    game_id = -1
    if play_games_i_already_left:
        registered_games = requests.get(url + "games/?game_state=STARTED&game_name=Core&user_ids="+str(player_id)).json()["games"]
        if len(registered_games) > 0:
            game_id = registered_games[0]['id']

    if game_id == -1:
        #TRY USING EXISTING GAMES FOR SHORTER WAITING TIME
        open_games = requests.get(url + "games/?game_state=WAITING&game_name=Core").json()["games"]
        for i in open_games:
            if register_player(i['id'], player_id, token):
                game_id = i['id']
                print("Found a game!")
                continue

    #NO OPEN GAME, TRY CREATING A NEW ONE
    while game_id == -1:
        game_id = create_game()
        if not register_player(game_id, player_id, token):
            print("Created new game!")
            game_id = -1

    #WAIT FOR ALL PLAYERS TO REGISTER
    waiting = True
    while waiting:
        game_state = requests.get(url + "games/" + str(game_id)).json()["game_state"]
        if not game_state == "WAITING":
            waiting = False
            continue
        print("WAITING FOR OTHER PLAYERS")
        time.sleep(5)

    #CHECK IF ALL WENT WELL
    game_info = requests.get(url + "games/" + str(game_id)).json()
    registered = False
    for counter, i in enumerate(game_info["players"]):
        if i['id'] == player_id:
            registered = True
            break
    assert registered
    assert game_info["game_name"] == "Core"
    assert game_info["id"] == game_id
    assert game_info["game_state"] == "STARTED"
    assert game_info["open_slots"] == 0

    #PLAY
    is_ongoing = True
    print("PLAYING THE GAME " + str(game_id))
    while is_ongoing:
        game_info = requests.get(url + "games/" + str(game_id)).json()
        if not game_info["game_state"] == "STARTED":
            break
        is_active = game_info["players"][game_info["active_player"]]["id"] == player_id
        if is_active:
            pos_x, pos_y = turn(game_info['history'][-1]['board'], get_symbol(game_info["active_player"]))
            print("MOVING TO (" + str(pos_x) + ", " + str(pos_y) + ")")
            status_code = 401
            while status_code == 401:
                token = check_and_update_token(player_id, token)
                data = {"player": {"id": player_id, "token": token}, "turn": str([pos_x, pos_y])}
                resp = requests.post(url + "games/" + str(game_id) + "/makeTurn", json=data)
                if resp.status_code == 200 and 'false' in resp.text:
                    is_ongoing = False
                status_code = resp.status_code
        time.sleep(5)
    return True

if __name__ == "__main__":
    play(username, password)