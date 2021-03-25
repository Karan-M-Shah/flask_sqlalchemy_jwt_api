from flask_sqlalchemy import SQLAlchemy

# An object of type SQLAlchemy. This links to our Flask app and allows us to map our objects to rows in a database
# For example, our ItemModel object with a name and price column can easily be placed into a database
db = SQLAlchemy()