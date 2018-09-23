from flask import Flask, Blueprint
from GameMicroservice.Game.api_var import api
from GameMicroservice.Game.endpoints.GameRessources import gamenamespace
from GameMicroservice.Database.db import db
import GameMicroservice.settings as settings
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def config(app):
    app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
    app.config['RESTPLUS_MASK_SWAGGER'] = False
    app.config['RESTPLUS_VALIDATE'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def init(app):
    config(app)
    blueprint = Blueprint('api', __name__, url_prefix="/api")
    api.init_app(blueprint)
    api.add_namespace(gamenamespace)
    app.register_blueprint(blueprint)
    with app.app_context():
        db.init_app(app)
        db.create_all()


def main():
    init(app)
    app.run(debug=settings.debug, threaded=True, host='0.0.0.0', port=settings.port)


if __name__ == "__main__":
    main()

