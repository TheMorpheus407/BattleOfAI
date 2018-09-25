import time
from enum import Enum

import requests


class GameState(Enum):
    WAITING = "WAITING"
    STARTED = "STARTED"
    ABORTED = "ABORTED"
    FINISHED = "FINISHED"


class BOAIapi:
    """

    PLEASE REPORT ANY BUGS
    THIS IS KINDA VERSION 0.1alpha-pre-test

    """

    def __init__(self, username, password, func, play_games_i_already_left=True, verbose=0,
                 games_api_url="https://games.battleofai.net/api/",
                 account_management_api_url="https://iam.battleofai.net/api/"):
        self.username = username
        self.password = password
        self.play_games_i_already_left = play_games_i_already_left
        self.func = func
        self.verbose = verbose
        self.games_api_url = games_api_url
        self.account_management_api_url = account_management_api_url

        self.player_id, self.token = self._login()

    def log(self, func, *text, requirement=1):
        if self.verbose >= requirement:
            print(f"{time.strftime('%a %H:%M:%S')} [BOAIapi] {func}:", *text)

    def _login(self):
        """
        Logs a user in with credentials of the registration for obtaining valid credentials for playing a game.
        :return: A tuple containing player_id and login token. Credentials are valid for 1 day.
        """
        login_data = {
            "username": self.username,
            "password": self.password
        }
        resp = requests.post(self.account_management_api_url + "iam/login", json=login_data)
        if not resp.status_code == 200:
            exit("Account Management temporarily unavailable")
        if resp.json()["userid"] is None or resp.json()["token"] is None or resp.json()["session_token"] is None:
            exit("Invalid login credentials")
        userid = resp.json()["userid"]
        token = str([resp.json()["token"], resp.json()["session_token"]])
        self.log("_login", "Logged in successfully as", self.username + " (ID: " + str(userid) + ")")
        return userid, token

    def get_games(self, own=False, game_state=GameState.WAITING):
        addition = ("&user_ids=" + str(self.player_id)) if own else ""
        url = f"{self.games_api_url}games/?game_state={game_state.value}&game_name=Core{addition}"
        self.log("get_games", url, requirement=2)
        raw_matches = requests.get(url).json()["games"]
        return list(k["id"] for k in raw_matches)

    # noinspection PyMethodMayBeStatic
    def create_game(self):
        """
        creates a game and returns the game id
        :return: the game id
        """
        resp = requests.post(self.games_api_url + "games/createGame", json={"game_name": "Core"})
        assert resp.status_code == 200
        return int(resp.text)

    def register(self, game_id):
        """
        Registers the player for a match by id
        :param game_id: The match to register on
        """
        resp = requests.post(self.games_api_url + "games/" + str(game_id) + "/registerPlayer",
                             json={"id": self.player_id, "token": self.token})
        assert resp.status_code == 200
        return 'true' in resp.text

    @staticmethod
    def get_symbol(active_player):
        return 'XO'[active_player]

    def check_and_update_token(self):
        unwrapped_token = self.token.replace("['", "").replace("']", "").split("', '")
        data = {
            "userid": self.player_id,
            "token": unwrapped_token[0],
            "session_token": unwrapped_token[1]
        }
        resp = requests.post(self.account_management_api_url + "iam/validateToken", json=data)
        if not resp.status_code == 200 or resp.json()["success"] is False:
            return self._login()[1]
        return self.token

    def status(self, game_id):
        return requests.get(self.games_api_url + "games/" + str(game_id)).json()

    def find_game(self, only_finish=False):
        # SEARCH FOR BROKEN GAMES
        if self.play_games_i_already_left:
            registered_games = self.get_games(own=True)
            if len(registered_games) > 0:
                self.log("join_first", "Found broken game", registered_games[0])
                return registered_games[0]

        # SEARCH FOR STARTED GAMES
        if self.play_games_i_already_left:
            started_games = self.get_games(own=True, game_state=GameState.STARTED)
            if len(started_games) > 0:
                self.log("join_first", "Found started game", started_games[0])
                return started_games[0]

        if only_finish:
            return None

        # NO BROKEN GAMES
        open_games = self.get_games()
        for i in open_games:
            self.log("join_first", "Found open games, trying to join", i)
            if self.register(i):
                self.log("join_first", "Joined", i)
                return i

        self.log("join_first", "No open games found, trying to create one myself...")

        # NO OPEN GAME, TRY CREATING A NEW ONE
        game_id = None
        while game_id is None:
            game_id = self.create_game()
            if not self.register(game_id):
                game_id = None
            else:
                self.log("join_first", "Joined newly created game", game_id)
                return game_id

    def wait_for_participants(self, game_id, ignore_other_lobby_error=False, delay=5):
        game_players = list(k["id"] for k in self.status(game_id)["players"])
        if not ignore_other_lobby_error:
            assert self.player_id in game_players, "You are currently not in game" + str(game_id)

        waiting = True
        while waiting:
            game_state = self.status(game_id)["game_state"]
            if game_state != "WAITING":
                return True
            else:
                self.log("fill_lobby", "Waiting for other players")
                time.sleep(delay)

    def assert_basics(self, game_id):
        game_info = self.status(game_id)
        participants = list(k["id"] for k in self.status(game_id)["players"])

        assert participants, "[BOAIapi] assert_basics: You weren't registered for the game?"
        assert game_info["game_name"] == "Core", "[BOAIapi] assert_basics: Wrong game mode?"
        assert game_info["id"] == game_id, "[BOAIapi] assert_basics: You weren't in the correct game?"
        assert game_info["game_state"] == "STARTED", "[BOAIapi] assert_basics: Tried playing in a not yet started game?"
        assert game_info["open_slots"] == 0, "[BOAIapi] assert_basics: Game ist not full?"

    def is_my_turn(self, game_id, game_status=None):
        if game_status is None:
            game_status = self.status(game_id)
        return game_status["players"][game_status["active_player"]]["id"] == self.player_id

    def make_move(self, game_id, x, y):
        status_code = 401
        while status_code == 401:
            data = {"player": {"id": self.player_id, "token": self.token}, "turn": str([x, y])}
            resp = requests.post(self.games_api_url + "games/" + str(game_id) + "/makeTurn", json=data)
            self.check_and_update_token()
            status_code = resp.status_code

    def handle_available(self):
        game_ids = self.get_games(own=True, game_state=GameState.STARTED)
        for game_id in game_ids:
            game_status = self.status(game_id)
            if self.is_my_turn(game_id, game_status=game_status):
                self.log("handle_available", "Handling", game_id)
                pos_x, pos_y = self.func(game_status['history'][-1]['board'],
                                         BOAIapi.get_symbol(game_status["active_player"]))
                self.log("handle_available", "Moving to (" + str(pos_x) + ", " + str(pos_y) + ")")
                self.make_move(game_id, pos_x, pos_y)
            else:
                self.log("handle_available", "Handled", game_id, "(Not your turn)")
        self.log("handle_available", "Done handling available")

    def play(self, only_finish=False):
        """
        TODO fixme?
        WARNING: basically copied from the "old" api, use "handle_available" instead
        Plays the game for you! (Make sure to enter code in the turn-function.
        :return: True if you won or False if lost.
        """
        game_id = self.find_game(only_finish=True)
        if game_id is None:
            if only_finish:
                self.log("play", "Finished.")
            else:
                self.log("play", "Found no open game and wasn't able to create a game (i guess?).")
            return None
        self.wait_for_participants(game_id)
        self.assert_basics(game_id)

        is_ongoing = True
        self.log("play", "Handling", game_id)
        while is_ongoing:
            game_info = self.status(game_id)
            if not game_info["game_state"] == "STARTED":
                self.log("play", "Game still not started?")
                break
            is_active = game_info["players"][game_info["active_player"]]["id"] == self.player_id
            if is_active:
                pos_x, pos_y = self.func(game_info['history'][-1]['board'],
                                         BOAIapi.get_symbol(game_info["active_player"]))
                self.log("play", "Moving to (" + str(pos_x) + ", " + str(pos_y) + ")")
                status_code = 401
                while status_code == 401:
                    self.check_and_update_token()
                    data = {"player": {"id": self.player_id, "token": self.token}, "turn": str([pos_x, pos_y])}
                    resp = requests.post(self.games_api_url + "games/" + str(game_id) + "/makeTurn", json=data)
                    if resp.status_code == 200 and 'false' in resp.text:
                        is_ongoing = False
                    status_code = resp.status_code
            time.sleep(5)
