import warmongo

schema = {
    'name': 'Country',
    'properties': {
        'name': {'type': 'string'},
        'abbreviation': {'type': 'string'},
        'languages': {
            'type': 'array',
            'items': {
                'type': 'string'
            }
        }
    },
    'additionalProperties': False,
}

# Connect to test database
warmongo.connect("test")

Country = warmongo.model_factory(schema)

sweden = Country(name="Sweden", abbreviation="SE", languages=["swedish", "english"])
sweden.save()

canada = Country(name="Canada", abbreviation="CA", languages=["english", "french"])
canada.save()

sweden2 = Country.find_one(_id=sweden._id)

countries = [c for c in Country.find({"name":"Sweden"})]

print countries
