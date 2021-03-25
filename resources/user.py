from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource, reqparse
from models.user import UserModel

# This is a resource | we are inheriting from the Resource class
class UserRegister(Resource):
    # Request Parser to parse incoming JSON request arguments to the resource
    parser = reqparse.RequestParser()
    # Add two arguments to the parser: The username and password
    parser.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

    # This will get called whenever we post to the register
    def post(self):
        # Parse the incoming request arguments
        data = UserRegister.parser.parse_args()

        # Check whether a user already exists within the database. If an object is returned, that means it exists
        if UserModel.find_by_username(data['username']):
            return {"message": "User already exists!"}, 400

        # Instantiate a new usermodel object
        user = UserModel(data['username'], data['password'])
        # Save the user to the database
        user.save_to_db()
        
        return {"message": "User created successfully."}, 201


# Retrieve user details and delete users
class User(Resource):
    # Retrieve a user
    @classmethod
    def get(cls, user_id):
        # Retrieve a UserModel object from the database
        user = UserModel.find_by_id(user_id)

        # If the user does not exist, print an error
        if not user:
            return {'message': 'User not found'}, 404
        
        # Print the user's properties if it exists
        return user.json()

    # Delete a user from the database 
    @classmethod
    def delete(cls, user_id):
        # Retrieve a UserModel object from the database or none if none exists
        user = UserModel.find_by_id(user_id)

        # If the user does not exist, print an error
        if not user:
            return {'message': 'User not found'}, 404

        # If the user exists, delete them from the database
        user.delete_from_db()
        return {'message': 'User deleted'}, 200


# User login resource to authenticate users 
class UserLogin(Resource):
    # Request Parser to parse incoming JSON request arguments to the resource
    parser = reqparse.RequestParser()
    # Add two arguments to the parser: The username and password
    parser.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

    # Get data from the parser, find the user in the database and check for a matching password
    # Create and return an access token and refresh token
    @classmethod
    def post(cls):
        # Get data from the parser (username and password)
        data = UserLogin.parser.parse_args()

        # Find the user in the database
        user = UserModel.find_by_username(data['username'])

        # Check for a matching password between the passed in password and the one saved in the database
        if user and safe_str_cmp(user.password, data['password']):
            # Part of flask-jwt-extended - allows us to identify users based on their token
            access_token = create_access_token(identity=user.id, fresh=True) # fresh is for token refreshing
            refresh_token = create_refresh_token(identity=user.id)

            # Return the tokens
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        
        # If the user did not exist
        return {'message': 'Invalid credentials'}, 401


# Resource to receive refresh token we created initially in UserLogin Resource and generate a new access token
class TokenRefresh(Resource):
    # Requires a refresh token in the request
    @jwt_refresh_token_required
    def post(self):
        # Extract the user id from the jwt token
        current_user = get_jwt_identity()
        # We are giving back an access token that is not going to be fresh
        # If it's fresh, that means they have recently given us their username and password 
        # If it's not fresh, it means it has been hours or day since they've authenticated, so for security we will
        # ask them for their credentials when performing critical tasks and generate a fresh token for them
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200