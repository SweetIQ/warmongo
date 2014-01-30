# Warmongo!

## Description

This is a package for generating classes from a JSON-schema that are to be
saved in MongoDB.

This extends the JSON schema by supporting extra BSON types:
* ObjectId - use the `"object_id"` type in your JSON schema to validate that
             a field is a valid ObjectId.
* datetime - use the `"date"` type in your JSON schema to validate that a field
             is a valid datetime

## Usage

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

    >>> sweden = Country({"name": 'Sweden', "abbreviation": 'SE'})
    >>> sweden.save()
    >>> sweden._id
    ObjectId('50b506916ee7d81d42ca2190')

5) Let the object validate itself!

    >>> sweden = Country.find_one({"name" : "Sweden"})
    >>> sweden.name = 5
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "warmongo/model.py", line 254, in __setattr__
        self.validate_field(attr, self._schema["properties"][attr], value)
      File "warmongo/model.py", line 189, in validate_field
        self.validate_simple(key, value_schema, value)
      File "warmongo/model.py", line 236, in validate_simple
        (key, value_type, str(value), type(value)))
    warmongo.exceptions.ValidationError: Field 'name' is of type 'string', received '5' (<type 'int'>)

    >>> sweden.overlord = 'Bears'
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "warmongo/model.py", line 257, in __setattr__
        raise ValidationError("Additional property '%s' not allowed!" % attr)
    warmongo.exceptions.ValidationError: Additional property 'overlord' not allowed!

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

## Production Examples

I use warmongo every day at my startup http://www.sweetiq.com/ to share data
definitions between our Python and Node.js applications. It has been running in
production for some time now, so it has been reasonably tested for robustness
and performance.
