import unittest

import warmongo

class TestFinding(unittest.TestCase):
    def setUp(self):
        self.schema = {
            'name': 'Country',
            'properties': {
                'name': {'type': 'string'},
                'abbreviation': {'type': 'string'},
                'languages' : {
                    'type' : 'array',
                    'items' : {
                        'type' : 'string'
                    }
                }
            },
            'additionalProperties': False,
        }

        # Connect to warmongo_test - hopefully it doesn't exist
        warmongo.connect("warmongo_test")
        self.Country = warmongo.model_factory(self.schema)

        # Drop all the data in it
        self.Country.collection().remove({})

        # Create some defaults
        sweden = self.Country(name="Sweden", abbreviation="SE",
                languages=["swedish"])
        sweden.save()
        usa = self.Country(name="United States of America", abbreviation="US",
                languages=["english"])
        usa.save()

    def testFindOneWithArgs(self):
        ''' Test grabbing a single value the Mongo way '''

        usa = self.Country.find_one({"abbreviation":"US"})

        self.assertIsNotNone(usa)
        self.assertEqual("United States of America", usa.name)

    def testFindOneWithKwargs(self):
        ''' Test grabbing a single value the Mongo way '''

        sweden = self.Country.find_one(abbreviation="SE")

        self.assertIsNotNone(sweden)
        self.assertEqual("Sweden", sweden.name)

    def testFindAll(self):
        ''' Just grab a bunch of stuff '''

        countries = self.Country.find()

        # Since find() returns a generator, need to convert to list
        countries = [c for c in countries]

        self.assertEqual(2, len(countries))

    def testCount(self):
        ''' See if everything is there '''
        self.assertEqual(2, self.Country.count())
        self.assertEqual(1, self.Country.count(abbreviation="SE"))
        self.assertEqual(0, self.Country.count(abbreviation="CA"))

    def testFindAllWithArgs(self):
        ''' Test fetching everything the mongo way '''

        countries = self.Country.find({"abbreviation":"SE"})

        # Since find() returns a generator, need to convert to list
        countries = [c for c in countries]

        self.assertEqual(1, len(countries))
        self.assertEqual("Sweden", countries[0].name)

    def testFindAllWithKwargs(self):
        ''' Test fetching everything the Python way '''

        countries = self.Country.find(abbreviation="US")

        # Since find() returns a generator, need to convert to list
        countries = [c for c in countries]

        self.assertEqual(1, len(countries))
        self.assertEqual("United States of America", countries[0].name)
