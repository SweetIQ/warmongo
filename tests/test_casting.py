import unittest

import warmongo


class TestValidation(unittest.TestCase):
    def testCastWithObject(self):
        schema = {
            "name": "Model",
            "properties": {
                "field": {
                    "type": "object",
                    "properties": {
                        "subfield": {"type": "integer"}
                    }
                }
            }
        }
        Model = warmongo.model_factory(schema)

        m = Model()

        old_fields = {
            "field": {
                "subfield": 5.2
            }
        }

        fields = m.cast(old_fields)

        self.assertEqual(5, fields["field"]["subfield"])

    def testCastWithArray(self):
        schema = {
            "name": "Model",
            "properties": {
                "field": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    }
                }
            }
        }
        Model = warmongo.model_factory(schema)

        m = Model()

        old_fields = {
            "field": [5.2, 7]
        }

        fields = m.cast(old_fields)

        self.assertEqual(5, fields["field"][0])
        self.assertEqual(7, fields["field"][1])

    def testBasicCast(self):
        schema = {
            "name": "Model",
            "properties": {
                "field": {"type": "integer"},
                "other_field": {"type": "string"},
            }
        }
        Model = warmongo.model_factory(schema)

        m = Model()

        old_fields = {
            "field": 5.2,
            "other_field": "5"
        }

        fields = m.cast(old_fields)

        self.assertEqual(5, fields["field"])
        self.assertEqual("5", fields["other_field"])
