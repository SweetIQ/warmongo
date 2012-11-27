from model import Model as WarmongoModel
from database import connect

import warlock


def model_factory(schema, base_class=WarmongoModel):
    # All models have an _id field
    if not "_id" in schema["properties"]:
        # TODO: validate object IDs
        schema["properties"]["_id"] = { "type": "any" }

    return warlock.model_factory(schema, base_class)
