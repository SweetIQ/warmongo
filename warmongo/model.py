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
import database

import inflect, re, jsonschema

from bson import ObjectId

inflect_engine = inflect.engine()

class Model(WarlockModel):
    def __init__(self, *args, **kwargs):
        ''' Creates an instance of the object.'''
        if len(kwargs) == 0 and len(args) > 0:
            # creating object with first element in args as object
            kwargs = args[0]
            args = args[1:]

        # creating object in kwargs form
        WarlockModel.__init__(self, *args, **self.from_mongo(kwargs))


    def save(self):
        ''' Saves an object to the database. '''
        d = dict(self)

        self._id = self.collection().save(self.to_mongo(d))


    @classmethod
    def find_or_create(cls, *args, **kwargs):
        ''' Retrieve an element from the database. If it doesn't exist, create it.
        Calliing this method is equivalent to calling find_one and then creating
        an object. Note that this method is not atomic.
        '''
        result = cls.find_one(*args, **kwargs)

        if result == None:
            result = cls(*args, **kwargs)

        return result

    @classmethod
    def find(cls, *args, **kwargs):
        ''' Grabs a set of elements from the DB.
        Note: This returns a generator, so you can't to do an efficient count.
        To get a count, use the count() function which accepts the same arguments
        as find() with the exception of non-query fields like sort, limit, skip.
        Possible kwarg options:
        - sort: field(s) to sort on. Same format as pymongo
        - limit: number of results to return
        - skip: number of results to skip
        '''
        options = {}

        for option in ["sort", "limit", "skip"]:
            if option in kwargs:
                options[option] = kwargs[option]
                del options[option]

        if len(kwargs) > 0 and len(args) == 0:
            # Allow find to accept kwargs format for querying, pass things
            # to pymongo as it expects
            args = (kwargs,) + args
            kwargs = {}

        result = cls.collection().find(*args, **kwargs)

        if "sort" in options:
            result = result.sort(options["sort"])

        if "skip" in options:
            result = result.skip(options["skip"])

        if "limit" in options:
            result = result.limit(options["limit"])

        for obj in result:
            yield cls(**obj)


    @classmethod
    def find_one(cls, *args, **kwargs):
        ''' Finds a single object from this collection. '''
        if len(kwargs) > 0 and len(args) == 0:
            # Allow find_one to accept kwargs format for querying, pass things
            # to pymongo as it expects
            args = (kwargs,) + args
            kwargs = {}

        result = cls.collection().find_one(*args, **kwargs)
        if result != None:
            return cls(**result)
        return None


    @classmethod
    def count(cls, *args, **kwargs):
        ''' Counts the number of items:
            - not the same as pymongo's count, this is the equivalent to:
                collection.find(*args, **kwargs).count()
        '''
        if len(kwargs) > 0 and len(args) == 0:
            # Allow find to accept kwargs format for querying, pass things
            # to pymongo as it expects
            args = (kwargs,) + args
            kwargs = {}

        return cls.collection().find(*args, **kwargs).count()


    @classmethod
    def collection(cls):
        ''' Get the pymongo collection object for this model. Useful for
        features not supported by Warmongo like aggregate queries and map-reduce. '''
        return database.get_collection(collection=cls.collection_name())


    @classmethod
    def collection_name(cls):
        ''' Get the collection associated with this class. The convention is
        to take the lowercase of the class name and pluralize it. '''
        global inflect_engine
        return inflect_engine.plural(cls.__name__.lower())


    def from_mongo(self, d):
        ''' Convert a dict from Mongo format to our format. '''
        return d


    def to_mongo(self, d):
        ''' Convert a dict to Mongo format from our format. '''
        return d


    def validate(self, obj):
        """ Apply a JSON schema to an object - this is an override from
        Warlock's model so that we can add the additional bson types. This
        will allow you to specify "object_id" as a valid type in your JSON
        schema. """
        bson_types = {
            "object_id": ObjectId
        }
        try:
            jsonschema.validate(obj, self.schema, types=bson_types)
        except jsonschema.ValidationError as exc:
            raise ValidationError(str(exc))
