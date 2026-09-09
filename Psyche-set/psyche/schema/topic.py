from pydanic import pydanic  



# The flow here will be that C++ sends the id to python, the python gets the data. Better than sending 
# data over.

from helpers.python_.helpers import Brain, Logger, BrainCreationError
from helpers.python_.debugging_utils import debug
from typing import (
    Awaitable,
    Final,
    final
)
from base import SchemaLogic
from datetime import datetime

class TopicLogic(SchemaLogic):
    def __init__(self, schema_id):
        super().__init__(schema_id)

if __name__ == "__main__":
    t = TopicLogic()