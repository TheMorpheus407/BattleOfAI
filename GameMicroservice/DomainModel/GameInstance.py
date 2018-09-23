from GameMicroservice.Database.GameDTO import GameDTO
import json
from GameMicroservice.DomainModel.json_writer import write_to_file, save_folder


class GameInstance:
    """
    Overwrite these attributes
    """
    GAME_NAME = "Interface"
    AMOUNT_PLAYERS = 2

    def __init__(self, id, active_player=0, history=None, game_dto=None):
        if game_dto is None:
            self.game_dto = GameDTO.query.filter(GameDTO.id == id).first()
        else:
            self.game_dto = game_dto
        self.active_player = active_player
        self.history = []
        if history is None:
            self.board = self.initialize_board()
            self.update_history()
        else:
            self.history = history
            self.board = self.history[-1]

    def initialize_board(self):
        """
        Overwrite this method
        """
        return []

    def turn(self, vars):
        """
        Overwrite this method
        """
        self.board.append(self.active_player)

    def valid(self, vars):
        """
        Overwrite this method
        """
        if vars == []:
            return True
        return False

    def won_check(self):
        """
        Overwrite this method
        """
        if len(self.history) > 10:
            self.won(self.active_player)
            return True

    @classmethod
    def load_from_json(cls, id):
        with open(save_folder + str(id)+'.json', 'r') as f:
            my_json = json.load(f)
        return cls(id, active_player=my_json["active_player"], history=my_json["history"])

    def save_to_file(self):
        write_to_file(self.game_dto.id, self)

    def get_players(self):
        return [x for x in self.game_dto.get_players_as_list() if x is not None]

    def open_slots(self):
        return self.AMOUNT_PLAYERS - len(self.get_players())

    def register_player(self, player_id):
        self.game_dto.set_player(player_id)
        if self.open_slots() <= 0:
            self.game_dto.next_state()
        return True

    def is_active_player(self, player_id):
        return self.get_players()[self.active_player] == player_id

    def is_ongoing(self):
        return self.game_dto.is_running()

    def next_player(self):
        self.active_player = (self.active_player+1)%self.AMOUNT_PLAYERS

    def turn_wrapper(self, vars):
        """
        :param vars:Variables for making a turn in the game
        :return:If the game is unfinished
        """
        if not self.valid(vars):
            self.won((self.active_player+1)%2)
            self.game_dto.abort_game()
            return False
        self.turn(vars)
        self.next_player()
        self.update_history()
        if self.won_check():
            return False
        return True

    def update_history(self):
        self.history.append(self.board)
        self.save_to_file()

    def won(self, player):
        self.game_dto.set_winner(player)
        self.game_dto.next_state()