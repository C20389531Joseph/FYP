from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['SECRET_KEY'] = 'secret123'

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from .controllers import main
    app.register_blueprint(main)

    return app
