# Application

This is an intermediate Python Flask REST API which is used to perform JWT authenticated CRUD operations on a SQLite Database using SQLAlchemy

# Routes

**POST** */register*: Used to register a new User using the UserRegister resource
**POST** */login*: Used to log in a User using the UserLogin resource
**GET** */user/<int:user_id>*: Used to get the information about a specific user
**DELETE** */user/<int:user_id>*: Used to delete a specific user
**POST** */refresh*: Used to refresh JWT access tokens

**GET** */items*: Resource for printing a list of items in the SQLite Database

**GET** */item/<name>*: Resource to retrieve a specific item from the database
**POST** */item/<name>*: Resource to create a new item within the database
**PUT** */item/<name>*: Resource for updating an existing item or creating an item if it does not exist
**DELETE** */item/<name>*: Resource to delete an existing item from the database

**GET** */stores*: Resource for printing a list of stores in the SQLite Database

**GET** */store/<name>*: Resource to retrieve a specific store from the database
**POST** */store/<name>*: Resource to create a new store within the database
**DELETE** */store/<name>*: Resource to delete an existing store from the database

# Structure

> root
*Dockerfile*: Program does not need to be run within a Docker container, but this file exists in case we want to add more services later
*docker-compose.yml*: Same as above
*requirements.txt*: Used to install requirements if run within a Docker container
*app.py*: Entrypoint. Includes main method, secret key, JWT configuration and route creation
*data.db*: Our SQLite database

> models
*user.py*: Contains the UserModel to find users by username or id, save users and print user information
*item.py*: Contains our ItemModel to print, find, save and delete items
*store.py*: Contains the StoreModel for finding and deleting stores

> resources
*user.py*: Contains resources for user login, registration, finding and tokens
*item.py*: Contains the ItemList and Item resources for creating, reading, updating and deleting items
*store.py*: Contains the Store and StoreList resource

# Postman

Routes are set up in Postman as a front-end is not a part of this application. 