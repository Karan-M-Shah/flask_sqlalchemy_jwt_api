# Import flask libraries
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
# Import our registers
from resources.user import User, UserRegister, UserLogin, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList
# Import out database code
from db import db 

# Create the Flask application, passing in the file name
app = Flask(__name__)

# Specify a configuration property for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # Connect SQLAlchemy to our sqlite database which lives in the root of our project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLAlchemy has its own modification tracker, so we can turn off Flask's version
app.config['PROPOGATE_EXCEPTIONS'] = True # Without this, if Flask JWT raises a custom error, you won't see it

# Should be something long, complicated and secure. It is used to encrypt the JWT
app.secret_key = 'karan'
# Allows us to easily add resources and routes. Every resource has to be a class
api = Api(app)

# Use a flask decorator to affect the method below it | It will run that method before the first request into the app
@app.before_first_request
# This will create our sqlite database using the config above unless it has been created already
def create_tables():
    # It is important to import the modals above so that SQLAlchemy knows which tables to create
    db.create_all()

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    # If the user is the first user in the database, they are an admin
    if identity == 1: # Instead of hard-coding, you should read from a config file or database
        return {'is_admin': True}
    return {'is_admin': False}

''' Configure token error messages. JWT has its own default messages, but if we wanted to configure them, here is how '''

@jwt.expired_token_loader
# When JWT realizes that a token has has expired, it will call this function to know what message it should send to the user
def expired_token_callback():
    return jsonify({'description': 'Your token has expired', 'error': 'token_expired'}), 401

# Called when the token sent to us in the header is not an actual JWT
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'description': 'Signature verification failed', 'error': 'Invalid Token'}), 401

# Called when a JWT is not sent at all
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'description': 'Request does not contain an access token', 'error': 'authorization required'}), 401

# Called when a non-fresh token is sent but we require a fresh token for the endpoint
@jwt.needs_fresh_token_loader
def token_not_fresh_callback(error):
    return jsonify({'description': 'This Token is not Fresh', 'error': 'Fresh token required'}), 401

# Called when a revokved token is used (Like when a user logs out)
@jwt.revoked_token_loader
def revoked_token_callback(error):
    return jsonify({'description': 'This token has been revoked', 'error': 'Token Revoked'}), 401

''' Add endpoints to the API '''

# Tells our Api that this resource should become accessible through our Api. A resource is a route with different methods POST, GET, etc.
# But we need an endpoint / route. We cannot use the @app.route decorator anymore though
# The first parameter is the name of our resource, the second is the route URI
api.add_resource(Item, '/item/<string:name>') # The name variable goes into the function parameter
api.add_resource(ItemList, '/items')

api.add_resource(User, '/user/<int:user_id>') # Pass in the user id 
api.add_resource(UserRegister, '/register') # UserRegister is a resource in our user.py file
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# This ensures that if we ever imported app.py from another file, it would not automatically start a Flask server
# This will only run if app.py specifically is executed
if __name__ == '__main__':
    # Initializ our database
    db.init_app(app) 
    # Port 5000 is the default, but you can put it in to be explicit
    # setting debug to true will improve the error messages
    app.run(port=5000, debug=True) 

