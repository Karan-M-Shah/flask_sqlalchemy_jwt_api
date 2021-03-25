# Import libraries
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):

    # Retrieves the store object if it exists otherwise returns an error
    def get(self, name):
        # Create an object of type StoreModel using the name
        store = StoreModel.find_by_name(name)
        # if the store exists, return the json string
        if store:
            return store.json()
        # if the store does not exist, return an error
        return {'Message': 'Store not found!'}, 404

    # Creates a new store and saves it in the database
    def post(self, name):
        # Check whether the store already exists, if so return an error
        if StoreModel.find_by_name(name):
            return {'Message': f'Store {name} already exists!'}, 400
        
        # If the store does not exist, instantiate a new object
        store = StoreModel(name)
        try: # Try saving the store to the database
            store.save_to_db()
            return store.json(), 201
        except: # If an error occurs
            return {'Message': 'An error occurred while creating the store.'}, 500

    def delete(self, name):
        # Check whether the store exists
        store = StoreModel.find_by_name(name)
        # If the store exists, delete it from the database
        if store:
            store.delete_from_db()
            return {'Message': 'Store Deleted'}
        else:
            return {'Message': 'Store does not exist'}

# Return a list of stores and their properties
class StoreList(Resource):
    def get(self):
        # The find_all() method returns a list of all items in the DB as objects, 
        # but we cannot return objects, we need to convert them into JSON
        # So we use a list comprehension to convert each object into JSON
        return {'stores': [store.json for store in StoreModel.find_all()]}

