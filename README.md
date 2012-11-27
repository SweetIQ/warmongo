# Warmongo!

Most of this README is shamelessly forked from https://github.com/bcwaldon/warlock.

## Wat

Extended warlock to support saving to a MongoDB database.

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

    >>> sweden = Country(name='Sweden', abbreviation='SE')
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
