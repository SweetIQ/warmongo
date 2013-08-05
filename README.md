# Warmongo!

## Wat

This is a package for generating classes from a JSON-schema that are to be
saved in MongoDB.

This extends the JSON schema by supporting extra BSON types:
* ObjectId - use the `"object_id"` type in your JSON schema to validate that
             a field is a valid ObjectId.

Warmongo is based off of Warlock, which is a JSON-schema validator for Python:
- https://github.com/bcwaldon/warlock

## How

1) Build your schema

	>>> schema = {
	    'name': 'Country',
	    'properties': {
	        'name': {'type': 'string'},
	        'abbreviation': {'type': 'string'},
	    },
	    'additionalProperties': False,
	}

2) Connect to your database

    >>> import warmongo
    >>> warmongo.connect("test")

3) Create a model

    >>> Country = warmongo.model_factory(schema)

4) Create an object using your model

    >>> sweden = Country({"name: 'Sweden', "abbreviation": 'SE')
    >>> sweden.save()
    >>> sweden._id
    '50b506916ee7d81d42ca2190'

5) Let the object validate itself!

    >>> sweden = Country.find_one({"name" : "Sweden"})
    >>> sweden.name = 5
    Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
      File "warlock/model.py", line 47, in __setattr__
        self.__setitem__(key, value)
    warlock.errors.InvalidOperation: Unable to set 'name' to '5'

    >>> sweden.overlord = 'Bears'
    Traceback (most recent call last):
	  File "<stdin>", line 1, in <module>
      File "warlock/model.py", line 47, in __setattr__
        raise InvalidOperation(msg)
    warlock.error.InvalidOperation: Unable to set 'overlord' to 'Bears'

## Choosing a collection

By default Warmongo will use the pluralized version of the model's name. If
you want to use something else, put it in the JSON-schema:

    {
        "name": "MyModel",
        ...
        "collectionName": "some_collection",
        ...
    }

## Multiple Databases

To use multiple databases, simply call `connect()` multiple times:

    >>> import warmongo
    >>> warmongo.connect("test")
    >>> warmongo.connect("other_db")

By default all models will use the first database specified. If you want to use
a different one, put it in the JSON-schema:

    {
        "name": "MyModel",
        ...
        "databaseName": "other_db",
        ...
    }

## Licence

Apache Version 2.0
