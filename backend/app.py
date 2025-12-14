from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    CORS(app) # Enable CORS for frontend

    from routes import api
    app.register_blueprint(api, url_prefix='/api')

    @app.route('/')
    def hello():
        return {"message": "Hello from Flask backend!"}

    with app.app_context():
        db.create_all()
        
    return app

app = create_app()

if __name__ == '__main__': # pragma: no cover
    app.run(host='0.0.0.0', port=5001)
