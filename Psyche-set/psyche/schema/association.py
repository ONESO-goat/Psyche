from base import SchemaLogic


class AssociationLogic(SchemaLogic):
    """
    Single association between two concepts.
    This is a baseModel for the table 'association' 
    """
    def __init__(self, 
                assoc_id: str
                ):
        if not assoc_id:
            return RuntimeError("Association id can not be empty.")

        super().__init__(schema_id=assoc_id, schema_type="association")

