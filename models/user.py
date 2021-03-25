# Import the SQLAlchemy object from our db.py file
from db import db

# Inherit from db which is an object of type SQLAlchemy
# This creates the mapping between the database and the objects
class UserModel(db.Model):
    # Tell SQLAlchemy the table name where these models should be stored
    __tablename__ = 'users'
    # Tell SQLAlchemy what columns we want our table to contain
    id = db.Column(db.Integer, primary_key=True) # Our unique index
    username = db.Column(db.String(80)) # Limits the size of the username
    password = db.Column(db.String(80)) # Limits the size of the password

    # These properties must match the SQLAlchemy column names for them to be saved to the database
    # We can have additional properties, they just won't be saved
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # JSON method for printing the contents of a user object
    def json(self):
        return {'id': self.id, 'username': self.username}

    # Saving the Model to the Database
    # When we retrieve an object with a particular id, we can change its name, add it to the session and commit it
    # and SQLAlchemy will do an UPDATE instead of an INSERT. So this method can do both an insert or an update (upserting)
    def save_to_db(self):
        # SQLAlchemy can translate from an object to a row
        # A session is a collection of object that we're going to write to the database. We can write multiple objects if we wanted
        db.session.add(self)
        # save the changes
        db.session.commit()
    
    # Delete a user from the database
    def delete_from_db(self):
        # Delete the passed in user object
        db.session.delete(self)
        # Save the changes
        db.session.commit()
    
    # Class method, meaning that we use cls instead of self. We are using the current class of User
    @classmethod
    def find_by_username(cls, username):
        # the query-builder method comes from the SQLAlchemy class we've inherited from
        # We are querying the Model / Table and filtering by the name column
        # Returns a UserModel object with self.username and self.password
        return UserModel.query.filter_by(username=username).first() # SELECT * from users WHERE name=name LIMIT 1
    
    # Class method, meaning that we use cls instead of self. We are using the current class of User
    @classmethod
    def find_by_id(cls, _id):
        # the query-builder method comes from the SQLAlchemy class we've inherited from
        # We are querying the Model / Table and filtering by the name column
        # Returns a UserModel object with self.username and self.password
        return UserModel.query.filter_by(id=_id).first() # SELECT * from users WHERE name=name LIMIT 1