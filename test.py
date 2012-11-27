import warmongo

schema = {
    'name': 'Country',
    'properties': {
        'name': {'type': 'string'},
        'abbreviation': {'type': 'string'},
    },
    'additionalProperties': False,
}

# Connect to test database
warmongo.connect("test")

Country = warmongo.model_factory(schema)

sweden = Country(name="Sweden", abbreviation="SE")
sweden.save()

sweden = Country.find_one({"name" : "Sweden"})
sweden.overlord = "Bears"
