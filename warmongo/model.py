# Copyright 2013 Rob Britton
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from warlock.model import Model as WarlockModel
from warlock.exceptions import ValidationError
from datetime import datetime
from dateutil.parser import parse as dateutil_parse
import database

import inflect
import re
import jsonschema

from bson import ObjectId

inflect_engine = inflect.engine()


class Model(WarlockModel):
    def __init__(self, fields, *args, **kwargs):
        ''' Creates an instance of the object.'''
        # Replace any sub-fields of mine with their respective defaults
        for field, value in self.schema.get("default", {}).items():
            if field not in kwargs:
                fields[field] = value

        if kwargs.get("from_find"):
            del kwargs["from_find"]
            self._from_find = True
            fields = self.from_mongo(fields)
        else:
            self._from_find = False

        # creating object in kwargs form
        WarlockModel.__init__(self, fields, *args, **self.from_mongo(kwargs))

    def reload(self):
        ''' Reload this object's data from the DB. '''
        fields = self.__class__.find_by_id(self._id)
        WarlockModel.__init__(self, fields)

    def convert_types(self, data, schema=None):
        ''' Returns a dict with any fields converted to proper bson types. '''
        if schema is None:
            schema = self.schema

        if not "properties" in schema:
            # The schema is likely an object, but it is an object that does
            # not have a properties field. Just return the whole object.
            return data

        def convert_type(value, subschema):
            value_type = subschema.get("type")

            # to convert: integers, ObjectID
            if value_type == "integer":
                return int(value)
            elif value_type == "object_id":
                return ObjectId(value)
            elif value_type == "date":
                return dateutil_parse(str(value))
            elif value_type == "array":
                # get the subkey type
                return [
                    convert_type(obj, subschema.get("items", {}))
                    for obj in value
                ]
            elif value_type == "object":
                return self.convert_types(value, subschema)
            else:
                return value

        result = {}
        for key, value in data.iteritems():
            if key in schema.get("properties", {}):
                subschema = schema["properties"][key]
                result[key] = convert_type(value, subschema)

        return result

    def save(self):
        ''' Saves an object to the database. '''
        d = dict(self)

        self._id = self.collection().save(self.to_mongo(d))

    def delete(self):
        ''' Removes an object from the database. '''
        if self._id:
            self.collection().remove({"_id": ObjectId(str(self._id))})

    @classmethod
    def find_or_create(cls, query, *args, **kwargs):
        ''' Retrieve an element from the database. If it doesn't exist, create
        it.  Calling this method is equivalent to calling find_one and then
        creating an object. Note that this method is not atomic.  '''
        result = cls.find_one(query, *args, **kwargs)

        if result is None:
            default = cls._schema.get("default", {})
            default.update(query)

            result = cls(default, *args, **kwargs)

        return result

    @classmethod
    def find(cls, *args, **kwargs):
        ''' Grabs a set of elements from the DB.
        Note: This returns a generator, so you can't to do an efficient count.
        To get a count, use the count() function which accepts the same
        arguments as find() with the exception of non-query fields like sort,
        limit, skip.
        '''
        options = {}

        for option in ["sort", "limit", "skip"]:
            if option in kwargs:
                options[option] = kwargs[option]
                del options[option]

        result = cls.collection().find(*args, **kwargs)

        if "sort" in options:
            result = result.sort(options["sort"])

        if "skip" in options:
            result = result.skip(options["skip"])

        if "limit" in options:
            result = result.limit(options["limit"])

        for obj in result:
            yield cls(obj, from_find=True)

    @classmethod
    def find_by_id(cls, id, **kwargs):
        ''' Finds a single object from this collection. '''
        if isinstance(id, basestring):
            id = ObjectId(id)

        args = {"_id": id}

        result = cls.collection().find_one(args, **kwargs)
        if result is not None:
            return cls(result, from_find=True)
        return None

    @classmethod
    def find_one(cls, *args, **kwargs):
        ''' Finds a single object from this collection. '''
        result = cls.collection().find_one(*args, **kwargs)
        if result is not None:
            return cls(result)
        return None

    @classmethod
    def count(cls, *args, **kwargs):
        ''' Counts the number of items:
            - not the same as pymongo's count, this is the equivalent to:
                collection.find(*args, **kwargs).count()
        '''
        return cls.collection().find(*args, **kwargs).count()

    @classmethod
    def collection(cls):
        ''' Get the pymongo collection object for this model. Useful for
        features not supported by Warmongo like aggregate queries and
        map-reduce. '''
        return database.get_collection(collection=cls.collection_name(),
                                       database=cls.database_name())

    @classmethod
    def collection_name(cls):
        ''' Get the collection associated with this class. The convention is
        to take the lowercase of the class name and pluralize it. '''
        global inflect_engine
        if cls._schema.get("collectionName"):
            return cls._schema.get("collectionName")
        elif cls._schema.get("name"):
            name = cls._schema.get("name")
        else:
            name = cls.__name__

        # convert to snake case
        name = (name[0] + re.sub('([A-Z])', r'_\1', name[1:])).lower()

        # pluralize
        return inflect_engine.plural(name)

    @classmethod
    def database_name(cls):
        ''' Get the database associated with this class. Meant to be overridden
        in subclasses. '''
        if cls._schema.get("databaseName"):
            return cls._schema.get("databaseName")
        return None

    def from_mongo(self, d):
        ''' Convert a dict from Mongo format to our format. '''
        return self.convert_types(d)

    def to_mongo(self, d):
        ''' Convert a dict to Mongo format from our format. '''
        return d

    def validate(self, obj):
        """ Apply a JSON schema to an object - this is an override from
        Warlock's model so that we can add the additional bson types. This
        will allow you to specify "object_id" as a valid type in your JSON
        schema. """
        bson_types = {
            "object_id": ObjectId,
            "date": datetime
        }
        try:
            # Since Mongo can query for non-required fields, strip those
            # required fields from the schema if we haven't sent them
            schema = self.schema
            if self._from_find:
                schema = self._remove_required(self.schema)

            jsonschema.validate(obj, schema, types=bson_types)
        except jsonschema.ValidationError as exc:
            raise ValidationError(str(exc))

    def _remove_required(self, schema):
        """ Remove required flags for a schema. """
        result = {}
        for key, value in schema.items():
            if key == "default":
                result[key] = False
            elif isinstance(value, dict):
                result[key] = self._remove_required(value)
            else:
                result[key] = value
        return result

    def __setattr__(self, key, value):
        """ Allow us to write to certain fields. """
        if key == "_from_find":
            return object.__setattr__(self, key, value)
        return WarlockModel.__setattr__(self, key, value)

    def _populate_required_fields(self, obj):
        """ Fill in any required fields with null values. This is used for find
        queries where the field is required, but we don't want to fetch it. """
        return obj
