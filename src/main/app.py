from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from routes.userRoutes import user_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Register routes
app.register_blueprint(user_routes)

@app.route('/')
def home():
    return "Welcome to Pi Open Hub!"

if __name__ == '__main__':
    app.run(debug=True)
