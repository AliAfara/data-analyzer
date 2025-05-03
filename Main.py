from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from routes import main

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
