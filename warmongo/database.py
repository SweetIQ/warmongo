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
    ''' Connect to a database. '''
    global default_database

    identifier = (host, port)

    connection = connections.get(identifier)

    if connection is None:
        connection = pymongo.MongoClient(host, port)

    connections[identifier] = connection

    if not database in databases:
        db = connection[database]

        if username is not None and password is not None:
            db.authenticate(username, password)

        databases[database] = db

        if default_database is None:
            default_database = db


def get_database(database=None):
    ''' Get a database by name, or the default database. '''
    global default_database

    # Check default
    if database is None:
        if default_database is None:
            raise NotConnected("no connection to the database has been made.")
        else:
            return default_database
    try:
        return databases[database]
    except KeyError:
        raise NotConnected("connect() hasn't been called on '%s'" % database)


def get_collection(collection, database=None):
    return get_database(database)[collection]
