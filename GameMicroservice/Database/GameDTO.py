from GameMicroservice.Database.db import db
from GameMicroservice.DomainModel.GameState import GameState


class GameDTO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(255))
    game_state = db.Column(db.Enum(GameState))
    player1_id = db.Column(db.Integer)
    player2_id = db.Column(db.Integer)
    player3_id = db.Column(db.Integer)
    player4_id = db.Column(db.Integer)
    player5_id = db.Column(db.Integer)
    player6_id = db.Column(db.Integer)
    player7_id = db.Column(db.Integer)
    player8_id = db.Column(db.Integer)
    player9_id = db.Column(db.Integer)
    player10_id = db.Column(db.Integer)
    player11_id = db.Column(db.Integer)
    player12_id = db.Column(db.Integer)
    player13_id = db.Column(db.Integer)
    player14_id = db.Column(db.Integer)
    player15_id = db.Column(db.Integer)
    player16_id = db.Column(db.Integer)
    winner_id = db.Column(db.Integer)

    def __init__(self, game_name):
        self.game_name = game_name
        self.game_state = GameState.WAITING

    def next_state(self):
        if self.game_state == GameState.WAITING:
            self.game_state = GameState.STARTED
        elif self.game_state == GameState.STARTED:
            self.game_state = GameState.FINISHED
        db.session.commit()

    def is_running(self):
        return self.game_state == GameState.STARTED

    def abort_game(self):
        self.game_state = GameState.ABORTED
        db.session.commit()

    def set_player(self, player_id):
        if self.player1_id is None:
            self.player1_id = player_id
        elif self.player2_id is None:
            self.player2_id = player_id
        elif self.player3_id is None:
            self.player3_id = player_id
        elif self.player4_id is None:
            self.player4_id = player_id
        elif self.player5_id is None:
            self.player5_id = player_id
        elif self.player6_id is None:
            self.player6_id = player_id
        elif self.player7_id is None:
            self.player7_id = player_id
        elif self.player8_id is None:
            self.player8_id = player_id
        elif self.player9_id is None:
            self.player9_id = player_id
        elif self.player10_id is None:
            self.player10_id = player_id
        elif self.player11_id is None:
            self.player11_id = player_id
        elif self.player12_id is None:
            self.player12_id = player_id
        elif self.player13_id is None:
            self.player13_id = player_id
        elif self.player14_id is None:
            self.player14_id = player_id
        elif self.player15_id is None:
            self.player15_id = player_id
        elif self.player16_id is None:
            self.player16_id = player_id
        db.session.commit()

    def set_winner(self, player_id):
        self.winner_id = player_id
        db.session.commit()

    def get_players_as_list(self):
        lst = [
            self.player1_id,
            self.player2_id,
            self.player3_id,
            self.player4_id,
            self.player5_id,
            self.player6_id,
            self.player7_id,
            self.player8_id,
            self.player9_id,
            self.player10_id,
            self.player11_id,
            self.player12_id,
            self.player13_id,
            self.player14_id,
            self.player15_id,
            self.player16_id
        ]
        return lst
