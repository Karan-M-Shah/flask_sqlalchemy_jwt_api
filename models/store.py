# Import the SQLAlchemy object from our db.py file
from db import db 

# Inherit from db which is an object of type SQLAlchemy
# This creates the mapping between the database and the objects
class StoreModel(db.Model):
    # The table name in SQLAlchemy where the model should be stored
    __tablename__ = 'stores'
    # The columns we want our table to contain
    id = db.Column(db.Integer, primary_key=True) # Unique index
    name = db.Column(db.String(80)) # Maximum length of the string
    # Checks for the relationship between between the StoreModel and ItemModel 
    # So SQLAlchemy goes to the ItemModel and sees the store_id foreign-key as well as the single store property
    # and create a many-to-one relationship between the ItemModel and the StoreModel
    # Therefore, the items property below is a list of items
    # When we use lazy='dynamic', self.items is no longer a list of items, 
    # but instead a querybuilder that we can use .all() to retrieve all of the items
    items = db.relationship('ItemModel', lazy='dynamic')

    # These properties must match the SQLAlchemy column names for them to be saved to the database
    # We can have additional properties, they just won't be saved
    def __init__(self, name):
        self.name = name
    
    # Returns a JSON representation of the model
    def json(self):
        return {'id': self.id, 'name': self.name, 'items': [item.json() for item in self.items.all()]}
    
    # This is a class method because it will return an object of type StoreModel
    @classmethod
    def find_by_name(cls, name):
        # the query-builder method comes from the SQLAlchemy class we've inherited from
        # We are querying the Model / Table and filtering by the name column
        # Returns a StoreModel object 
        return StoreModel.query.filter_by(name=name).first() # SELECT * from stores WHERE name=name LIMIT 1
    
    # Returns all stores and their properties from the database
    @classmethod
    def find_all(cls):
        return StoreModel.query.find_all()
    
    # Saving the Model to the Database
    # When we retrieve an object with a particular id, we can change its name, add it to the session and commit it
    # and SQLAlchemy will do an UPDATE instead of an INSERT. So this method can do both an insert or an update (upserting)
    def save_to_db(self):
        # SQLAlchemy can translate from an object to a row
        # A session is a collection of object that we're going to write to the database. We can write multiple objects if we wanted
        db.session.add(self)
        # save the changes
        db.session.commit()

    # Delete a store from the database and save the changes
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()