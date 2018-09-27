import time
from enum import Enum

import requests


class GameState(Enum):
    WAITING = "WAITING"
    STARTED = "STARTED"
    ABORTED = "ABORTED"
    FINISHED = "FINISHED"
    ANY = "ANY"
    ANY_DICT = "ANY_DICT"


class MatchMethod(Enum):
    CREATE = 1
    JOIN = 2


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

    def get_games(self, own=False, game_state=GameState.WAITING, user_id=None):
        addition = ("&user_ids=" + str(self.player_id)) if own else ""
        if user_id is not None:
            assert own is False, "Can't use specified user_id and own=True at the same time."
            addition = "&user_ids=" + str(user_id)
        if game_state == GameState.ANY:
            r = []
            for gs in GameState:
                if gs != GameState.ANY and gs != GameState.ANY_DICT:
                    r += self.get_games(own=True, game_state=gs, user_id=user_id)
            return r
        elif game_state == GameState.ANY_DICT:
            r = {}
            for gs in GameState:
                if gs != GameState.ANY and gs != GameState.ANY_DICT:
                    r[gs.value] = self.get_games(own=True, game_state=gs, user_id=user_id)
            return r
        else:
            url = f"{self.games_api_url}games/?game_state={game_state.value}&game_name=Core{addition}"
            self.log("get_games", url, requirement=2)
            raw_matches = requests.get(url).json()["games"]
            return list(k["id"] for k in raw_matches)

    def create_game(self):
        """
        creates a game and returns the game id
        :return: the game id
        """
        resp = requests.post(self.games_api_url + "games/createGame", json={"game_name": "Core"})
        assert resp.status_code == 200
        return int(resp.text)

    def join(self, game_id):
        """
        Joins a match
        :param game_id: The match to join
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
            self.token = self._login()[1]
        return self.token

    def status(self, game_id):
        return requests.get(self.games_api_url + "games/" + str(game_id)).json()

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
        """
        # TODO is this redundant?
        :param game_id:
        :return:
        """
        game_info = self.status(game_id)
        participants = list(k["id"] for k in self.status(game_id)["players"])

        assert participants, "[BOAIapi] assert_basics: You weren't registered for the game?"
        assert game_info["game_name"] == "Core", "[BOAIapi] assert_basics: Wrong game mode?"
        assert game_info["id"] == game_id, "[BOAIapi] assert_basics: You weren't in the correct game?"
        assert game_info["game_state"] == "STARTED", "[BOAIapi] assert_basics: Tried playing in a not yet started game?"
        assert game_info["open_slots"] == 0, "[BOAIapi] assert_basics: Game ist not full?"

    def is_my_turn(self, game_id, game_status=None) -> bool:
        """
        This function returns true if its your turn in "game_id"

        :param game_id: The game id
        :param game_status: If you already requested the game status and don't want to request it again, you can pass
        it here to save some network traffic
        :return: True if its your turn
        """
        if game_status is None:
            game_status = self.status(game_id)
        return game_status["players"][game_status["active_player"]]["id"] == self.player_id

    def participants(self, game_id, game_status=None) -> list:
        """
        This function returns all players participating in "game_id"

        :param game_id: The game id
        :param game_status: If you already requested the game status and don't want to request it again, you can pass
        it here to save some network traffic
        :return: Players
        """
        if game_status is None:
            game_status = self.status(game_id)
        return list(k["id"] for k in game_status["players"])

    def make_move(self, game_id, x, y):
        status_code = 401
        while status_code == 401:
            data = {"player": {"id": self.player_id, "token": self.token}, "turn": str([y, x])}
            resp = requests.post(self.games_api_url + "games/" + str(game_id) + "/makeTurn", json=data)
            self.check_and_update_token()
            status_code = resp.status_code

    def handle_available(self, game_ids=None):
        """
        Handles the games specified in "game_ids" or all started games.

        # TODO auto create games if no games available

        Example usage:
        while True:
            api.handle_available()
            time.sleep(10)

        :param game_ids: Optional game_ids
        :return: None
        """
        self.check_and_update_token()
        if game_ids is None:
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

    def match(self, user_id, mode: MatchMethod = MatchMethod.JOIN, force_chosen_game_id=None):
        """
        This method can be used, if you want to play against a specified player.
        If you use mode=MatchMethod.JOIN, the he will have to user mode=MatchMethod.CREATE.
        TLDR one of you has to create a lobby and the other one has to join

        Example usage:
        Player1:
            api.match(123, mode=MatchMethod.CREATE)
        Player2:
            api.match(123, mode=MatchMethod.JOIN)

        :param user_id:The specified player
        :param mode: MatchMethod (either create or join game)
        :param force_chosen_game_id: If the merhod is MatchMethod.JOIN and there are multiple available games,
        you will be asked to select a lobby. You cant skip that thing by specifying a "always i dont care" default value
        :return: None
        """

        if mode == MatchMethod.JOIN:
            self.log("match", "Method: JOIN")
            game_ids = self.get_games(user_id=user_id, game_state=GameState.WAITING)
            chosen_game_id = 0
            if len(game_ids) == 0:
                self.log("match", "User", user_id, "has no WAITING match")
                return
            elif len(game_ids) == 1:
                self.log("match", "Found waiting game", game_ids[0])
                chosen_game_id = game_ids[0]
            else:
                self.log("match", "User", user_id, "has to many WAITING matches. You have to select one.")
                if force_chosen_game_id is not None:
                    self.log("match", "Force mode enabled, set selected to", force_chosen_game_id)
                    chosen_game_id = force_chosen_game_id
                else:
                    self.log("match", "Available matches:", game_ids)
                    inp = input("$ ")
                    if not inp.isdigit():
                        self.log("match", "You have to enter a game id, for example \"3\"")
                        return
                    inp = int(inp)
                    if inp not in game_ids:
                        self.log("match", "You entered a invalid game id")
                        return
                    chosen_game_id = inp

            status = self.status(chosen_game_id)
            participants = self.participants(chosen_game_id, game_status=status)
            if self.player_id in participants:
                self.log("match", "You are already in that game.")
                return

            self.join(chosen_game_id)
            self.log("match", "Joined the match.")
            while status["game_state"] != GameState.FINISHED.value:
                self.handle_available([chosen_game_id])
                status = self.status(chosen_game_id)
                time.sleep(5)

        elif mode == MatchMethod.CREATE:
            self.log("match", "Method: CREATE")

            game_id = self.create_game()
            self.join(game_id)

            self.log("match", "Created and joined game")

            self.wait_for_participants(game_id)

            status = self.status(game_id)

            while status["game_state"] != GameState.FINISHED.value:
                self.handle_available([game_id])
                status = self.status(game_id)
