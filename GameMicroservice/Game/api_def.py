from flask_restplus import fields
from GameMicroservice.Game.api_var import api

game_id = api.model('A single Game ID', {
    'id': fields.Integer(required=True, description='The game ID of the game')
})

list_of_games = api.inherit('List of Games', {
    'games': fields.List(fields.Nested(game_id))
})

player_id = api.model('An ID of a player', {
    'id': fields.Integer(required=True, description='The User ID of a player')
})

board = api.model('A games board', {
    'board': fields.Raw()
})


game = api.model('A game instance', {
    'id': fields.Integer(required=True, description='The ID of the game'),
    'winning_player': fields.Integer(description='The User ID of the player who won the match. Not used if match not over.'),
    'players': fields.List(fields.Nested(player_id)),
    'open_slots': fields.Integer(description='How many players can still join'),
    'game_state': fields.String(required=True, description='Enum of Game State: WAITING, STARTED, ABORTED, FINISHED'),
    'game_name': fields.String(required=True, description='The name of the game, e.g. CoRe, Check,...'),
    'active_player': fields.Integer(description='User ID of player whose turn it is'),
    'history': fields.List(fields.Nested(board))
})

game_name = api.model('The name of a game mode', {
    'game_name': fields.String(required=True, description='The name of the game mode')
})

player = api.model('A player', {
    'id': fields.Integer(required=True, description='The User ID of a player'),
    'token': fields.String(required=True, description='Login token. Obtain it via Login-API')
})

player_turn = api.model('A player and a turn', {
    'player': fields.Nested(player),
    'turn': fields.String(required=True, description="Your turn in json format")
})