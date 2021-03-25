# Import libraries
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required
from models.item import ItemModel

# Every resource has to be a class that inherents from Resource class
# This allows us to use features from the Resource class 
# So it is basically a copy of that class, but we can change things
class Item(Resource):
    # Used to parse requests. Belongs to the class itself, and not to specific objects
    parser = reqparse.RequestParser()
    # This will look in the JSON payload but it will also look in form payloads if needed
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help="Every Item must belong to a Store!")
    # Get the payload using the parser instead of request
    # This will parse the arguments that pass through the payload and put the valid ones in data variable
    # So anything other than price will be erased completely

    def get(self, name):
        try: # Search for the item in the database
            item = Item.find_by_name(name)
            # Check whether the item exists, if so return it
            if item:
                return item.json()
            return {'message': 'Item not found'}, 404
        except: # catch any errors
            return {'message': 'An error occured while searching the database'}, 500 # Internal server error

    # This means we have to authenticate before sending the request
    @jwt_required
    def post(self, name):
        # If an item already exists, return an error
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists.'}, 400

        # Parse the response
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        
        try: # Add the new item to the database
            item.save_to_db()
        except: # Catch any errors
            return {"message": "An error occured while inserting the item"}, 500 # Internal server error

        # Let the application know it was successful with the 201 code, meaning a resource was created
        return item.json(), 201 
    
    # This means we have to authenticate before sending the request
    @jwt_required
    def delete(self, name):
        # Use the claim we made in app.py to interpret the jwt and extract any claims that have been attached
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege is required'}, 401

        # Create an object of type ItemModel if the named item exists in the database
        item = ItemModel.find_by_name(name)
        if item:
            # If the item exists, call its method to delete it from the database
            item.delete_from_db()
        return {'Message': 'Item deleted'}, 410
    
     # This requires a FRESH JWT - check the TokenRefresh Resource in the User.py file for more information
    @fresh_jwt_required
    # Create or update an existing item
    def put(self, name):
        # Parse and validate the JSON payload
        data = Item.parser.parse_args()

        # Retrieve the item from the database if it exists or set item equal to none if not
        item = ItemModel.find_by_name(name)

        if item is None:
            # If the item does not exist, then create a new item 
            item = ItemModel(name, data['price'], data['store_id'])
        else: 
            # If the item does exist, update the price property
            item.price = data['price']

        # Save the item to the database (this either inserts or updates based on whether it exists)
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    # Returns all items from our database
    @jwt_optional
    def get(self):
        # This gets us whatever we save in the access token as the identity - in our case, the id of the user
        # Because jwt is optional, it could also give us none - in case they are not logged in or didnd't send the jwt token
        # If we wanted, we could then return a partial set of items if they are not logged in. I was too lazy to do this
        user_id = get_jwt_identity()
        # The find_all() method returns a list of all items in the DB as objects, 
        # but we cannot return objects, we need to convert them into JSON
        # So we use a list comprehension to convert each object into JSON
        return {'items': [item.json() for item in ItemModel.find_all()]}, 200
