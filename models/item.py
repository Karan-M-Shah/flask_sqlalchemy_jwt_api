# Import the SQLAlchemy object from our db.py file
from db import db 

# Inherit from db which is an object of type SQLAlchemy
# This creates the mapping between the database and the objects
class ItemModel(db.Model):
    # The table name in SQLAlchemy where the model should be stored
    __tablename__ = 'items'
    # The columns we want our table to contain
    id = db.Column(db.Integer, primary_key=True) # Unique index
    name = db.Column(db.String(80)) # Maximum length of the string
    price = db.Column(db.Float(precision=2)) # The number of numbers after a decimal
    store_id = db.Column(db.Integer, db.ForeginKey('stores.id')) # Create a foreign key to the StoreModel's id using table_name.column_name
    # This relationship creates a new store property within the ItemModel using the store_id foreign key
    store = db.relationship('StoreModel')

    # These properties must match the SQLAlchemy column names for them to be saved to the database
    # We can have additional properties, they just won't be saved
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id
    
    # Returns a JSON representation of the model
    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, 'store_id': self.store_id}
    
    # This is a class method because it will return an object of type ItemModel
    @classmethod
    def find_by_name(cls, name):
        # the query-builder method comes from the SQLAlchemy class we've inherited from
        # We are querying the Model / Table and filtering by the name column
        # Returns an ItemModel object with self.name and self.price
        return ItemModel.query.filter_by(name=name).first() # SELECT * from items WHERE name=name LIMIT 1
    
    # Returns all items and their properties from the database
    @classmethod
    def find_all(cls):
        return ItemModel.query.find_all()
    
    # Saving the Model to the Database
    # When we retrieve an object with a particular id, we can change its name, add it to the session and commit it
    # and SQLAlchemy will do an UPDATE instead of an INSERT. So this method can do both an insert or an update (upserting)
    def save_to_db(self):
        # SQLAlchemy can translate from an object to a row
        # A session is a collection of object that we're going to write to the database. We can write multiple objects if we wanted
        db.session.add(self)
        # save the changes
        db.session.commit()

    # Delete an item from the database and save the changes
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()