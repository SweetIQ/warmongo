import unittest
from datetime import datetime
from bson import ObjectId

import warmongo
from warmongo.exceptions import ValidationError


class TestValidation(unittest.TestCase):
    def testValidateArray(self):
        schema = {
            "name": "Model",
            "properties": {
                "field": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        }

        Model = warmongo.model_factory(schema)

        m = Model({
            "field": ["asdf", "hello"]
        })

        self.assertEqual(2, len(m.field))
        self.assertEqual("asdf", m.field[0])
        self.assertRaises(ValidationError, Model, {
            "field": "hi"
        })

    def testValidateString(self):
        schema = {
            "name": "Model",
            "properties": {
                "field": {
                    "type": "string"
                }
            }
        }

        Model = warmongo.model_factory(schema)

        m = Model({
            "field": "asdf"
        })

        self.assertEqual("asdf", m.field)
        self.assertRaises(ValidationError, Model, {
            "field": 5
        })

    def testValidateObject(self):
        schema = {
            "name": "Model",
            "properties": {
                "field": {
                    "type": "object",
                    "properties": {
                        "subfield": {"type": "string"}
                    }
                }
            }
        }

        Model = warmongo.model_factory(schema)

        m = Model({
            "field": {"subfield": "asdf"}
        })

        self.assertEqual("asdf", m.field["subfield"])
        self.assertRaises(ValidationError, Model, {
            "field": "hi"
        })

    def testValidateAny(self):
        schema = {
            "name": "Model",
            "properties": {
                "field": {
                    "type": "any"
                }
            }
        }

        Model = warmongo.model_factory(schema)

        Model({"field": ["asdf", "hello"]})
        Model({"field": "asdf"})
        Model({"field": 5})
        Model({"field": True})
        Model({"field": None})
        Model({"field": {"subfield": "asdf"}})

    def testValidateNumber(self):
        schema = {
            "name": "Model",
            "properties": {
                "field": {
                    "type": "number"
                }
            }
        }

        Model = warmongo.model_factory(schema)

        m = Model({
            "field": 5.5
        })

        self.assertEqual(5.5, m.field)
        self.assertRaises(ValidationError, Model, {
            "field": "hi"
        })

        # using an int should still work
        m = Model({
            "field": 5
        })

        self.assertEqual(5, m.field)

    def testValidateMany(self):
        schema = {
            "name": "Model",
            "properties": {
                "field": {
                    "type": ["string", "null"]
                }
            }
        }

        Model = warmongo.model_factory(schema)

        m = Model({
            "field": "asdf"
        })

        self.assertEqual("asdf", m.field)
        self.assertRaises(ValidationError, Model, {
            "field": 5
        })

        m.field = None

        self.assertIsNone(m.field)

    def testValidateDate(self):
        schema = {
            "name": "Model",
            "properties": {
                "field": {
                    "type": "date"
                }
            }
        }

        Model = warmongo.model_factory(schema)

        m = Model({
            "field": datetime(2010, 5, 12)
        })

        self.assertEqual(2010, m.field.year)
        self.assertEqual(5, m.field.month)
        self.assertEqual(12, m.field.day)
        self.assertRaises(ValidationError, Model, {
            "field": "hi"
        })

    def testValidateObjectId(self):
        schema = {
            "name": "Model",
            "properties": {
                "field": {
                    "type": "object_id"
                }
            }
        }

        Model = warmongo.model_factory(schema)

        m = Model({
            "field": ObjectId("123412341234123412341234")
        })

        self.assertEqual(ObjectId("123412341234123412341234"), m.field)
        self.assertRaises(ValidationError, Model, {
            "field": "hi"
        })

    def testValidateInteger(self):
        schema = {
            "name": "Model",
            "properties": {
                "field": {
                    "type": "integer"
                }
            }
        }

        Model = warmongo.model_factory(schema)

        # floats should not cause validation errors, but they do get truncated
        m = Model({
            "field": 7.8
        })

        self.assertEqual(7, m.field)
        self.assertRaises(ValidationError, Model, {
            "field": "hi"
        })

    def testValidateBool(self):
        schema = {
            "name": "Model",
            "properties": {
                "field": {
                    "type": "boolean"
                }
            }
        }

        Model = warmongo.model_factory(schema)

        m = Model({
            "field": False
        })

        self.assertEqual(False, m.field)
        self.assertRaises(ValidationError, Model, {
            "field": "hi"
        })
