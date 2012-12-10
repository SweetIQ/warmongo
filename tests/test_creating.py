import unittest

import warmongo

class TestCreating(unittest.TestCase):
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
        usa = self.Country(name="United States of America", abbreviation="US",
                languages=["english"])

    def testCreateWithKwargs(self):
        ''' Test with doing things the Python way '''
        canada = self.Country(name="Canada", abbreviation="CA",
                languages=["english", "french"])

        canada.save()

        self.assertEqual("Canada", canada.name)
        self.assertEqual("CA", canada.abbreviation)
        self.assertEqual(2, len(canada.languages))
        self.assertTrue("english" in canada.languages)
        self.assertTrue("french" in canada.languages)

    def testCreateWithArgs(self):
        ''' Test with doing things the Mongo way '''

        canada = self.Country({
            "name" : "Canada",
            "abbreviation" : "CA",
            "languages" : ["english", "french"]
        })

        canada.save()

        self.assertEqual("Canada", canada.name)
        self.assertEqual("CA", canada.abbreviation)
        self.assertEqual(2, len(canada.languages))
        self.assertTrue("english" in canada.languages)
        self.assertTrue("french" in canada.languages)
