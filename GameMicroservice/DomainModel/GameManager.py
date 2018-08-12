from GameMicroservice.Database.db import db
from GameMicroservice.Database.GameDTO import GameDTO
from GameMicroservice.DomainModel.GameState import GameState

from GameMicroservice.DomainModel.GameInstance import GameInstance
from GameMicroservice.CoRe.CoReInstance import CoReInstance

def create_game(game_name):
    if game_name == GameInstance.GAME_NAME:
        game = create_gamedto(game_name)
        game_instance = GameInstance(game.id, game_dto=game)
        return game.id
    elif game_name == CoReInstance.GAME_NAME:
        game = create_gamedto(game_name)
        game_instance = CoReInstance(game.id, game_dto=game)
        return game.id
    return 0

def load_from_json(id):
    game = GameDTO.query.filter_by(id=id).first()
    if game is None:
        return None
    game_name = game.game_name
    if game_name == GameInstance.GAME_NAME:
        return GameInstance.load_from_json(id)
    elif game_name == CoReInstance.GAME_NAME:
        return CoReInstance.load_from_json(id)
    return None


def create_gamedto(game_name):
    game = GameDTO(game_name)
    db.session.add(game)
    db.session.commit()
    return game


def get_games(game_state, user_ids, game_name):
    if game_name is not None:
        games = GameDTO.query.filter_by(game_name=game_name)
    else:
        games = GameDTO.query.all()
    ret = []
    for i in games:
        if game_state is not None:
            if not i.game_state == GameState[game_state]:
                continue
        user_id_missing = False
        for id in user_ids:
            id = int(id)
            if id not in i.get_players_as_list():
                user_id_missing = True
                break
        if not user_id_missing:
            ret.append(i.id)
    return ret
