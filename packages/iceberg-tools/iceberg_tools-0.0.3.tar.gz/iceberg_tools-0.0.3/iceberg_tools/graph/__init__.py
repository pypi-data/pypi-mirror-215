import fastjsonschema

class AssociationSchema:

    def __init__(self, schema: dict):
        self.schema = schema
        self.compiled_schema = fastjsonschema.compile(schema)

class AssociationSchema:
    pass