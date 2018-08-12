from flask import request
from flask_restplus import Namespace, Resource
from GameMicroservice.Game.api_var import api
from GameMicroservice.Game.api_def import list_of_games, game, game_name, player, player_turn
from GameMicroservice.DomainModel.GameManager import create_game, get_games, load_from_json
from GameMicroservice.Game.login_methods import validate_login
from flask import abort
import json

gamenamespace = Namespace('games/', description='Information about all games')

@gamenamespace.route('/<int:id>')
class GameResource(Resource):
    @api.marshal_with(game)
    def get(self, id):
        game = load_from_json(id)
        players = game.get_players()
        my_json = {
            "id": game.game_dto.id,
            "winning_player": game.game_dto.winner_id,
            "players": [{"id":x} for x in players],
            'open_slots': game.open_slots(),
            "game_state": game.game_dto.game_state.name,
            "game_name": game.game_dto.game_name,
            "active_player": game.active_player,
            "history": [{"board":x} for x in game.history]
        }
        return my_json

@gamenamespace.route('/<int:id>/registerPlayer')
class RegisterResource(Resource):
    @api.expect(player)
    def post(self, id):
        if not validate_login(request.json['id'], request.json['token']):
            return False
        game = load_from_json(id)
        open_slots = game.open_slots()
        if open_slots <= 0:
            return False
        return game.register_player(request.json['id'])

@gamenamespace.route('/<int:id>/makeTurn')
class TurnResource(Resource):
    @api.expect(player_turn)
    def post(self, id):
        player = request.json['player']
        turn = json.loads(request.json['turn'])
        if not validate_login(player['id'], player['token']):
            abort(401)
        game = load_from_json(id)
        if not game.is_ongoing():
            abort(403)
        if game.is_active_player(player['id']):
            return game.turn_wrapper(turn)
        abort(403)


@gamenamespace.route('/')
class GameManagerResource(Resource):
    @api.marshal_with(list_of_games)
    def get(self):
        game_state = request.args.get('game_state', default=None)
        user_ids = request.args.get('user_ids', default=None) #?user_ids=12_42_1337
        if user_ids is not None:
            user_ids = user_ids.split("_")
        else:
            user_ids = []
        game_name = request.args.get('game_name', default=None)
        game_ids = get_games(game_state, user_ids, game_name)
        ret = {'games': [{'id':x} for x in game_ids]}
        return ret

@gamenamespace.route('/createGame')
class CreateGameManagerResource(Resource):
    @api.expect(game_name)
    def post(self):
        #TODO limit for DDoS Protection
        val = create_game(request.json['game_name'])
        if val == 0:
            abort(501)
        return val