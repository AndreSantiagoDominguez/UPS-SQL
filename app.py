from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config
from src.models import db 
from src.routes.doneesRoutes import doneesBlueprint
from src.routes.donorsRouter import donorsBlueprint
from src.routes.profileRouter import profileBlueprint
from src.routes.contributionsRouter import contributiosBlueprint
from src.routes.addressRouter import addressBlueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app)

    app.config.from_object(config['development'])
    app.config['UPLOAD_FOLDER'] = './photos'
    
    db.init_app(app)
    jwt = JWTManager(app)
    app.register_blueprint(doneesBlueprint, url_prefix="/donees")
    app.register_blueprint(donorsBlueprint, url_prefix="/donors")
    app.register_blueprint(profileBlueprint, url_prefix="/profile")
    app.register_blueprint(contributiosBlueprint, url_prefix="/contributions")
    app.register_blueprint(addressBlueprint, url_prefix="/address")
    return app

# Define app globalmente
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
