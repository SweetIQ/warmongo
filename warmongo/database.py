''' Interface to pymongo '''
import pymongo

class NotConnected(RuntimeError):
    pass

# List of all the databases we have connected to
connections = {}

# List of databases
databases = {}

# The first connection we make is the default database
default_database = None

def connect(database, username=None, password=None, host="localhost", port=27017):
    global default_database

    identifier = (host, port)

    connection = connections.get(identifier, pymongo.Connection(host, port))
    connections[identifier] = connection

    if not database in databases:
        db = connection[database]
    
        if username != None and password != None:
            db.authenticate(username, password)

        databases[database] = db

        if default_database == None:
            default_database = db

''' Get a database by name, or the default database. '''
def get_database(database=None):
    global default_database

    # Check default
    if database == None:
        if default_database == None:
            raise NotConnected("no connection to the database has been made.")
        else:
            return default_database
    try:
        return databases[database]
    except KeyError:
        raise NotConnected("connect() hasn't been called on '%s'" % database)

def get_collection(collection, database=None):
    return get_database(database)[collection]
