

from enum import Enum
from typing import Any, Callable


class HAS(Enum):
    """
    A HoldingAssumptionStands (abbrv. HAS) notes that the object containing HAS follows the corresponding rules
    
    """
    # TODO: How to make this a Callable enum, or a Tuple?
    #       Rationale: want to preserve type check
    Between = 1
    AtLeast = 2
    Exactly = 3


class OPTION:
    """
    An OptionalPartialTieredInsertionOfNotions (abbrv. OPTION, yes these are half satirical) indicates that
      there can be multiple possible validation schemas accepted.
    """
    options = []

    def __init__(self, *args: Any):
        options = list(args)
    
    def __call__(self, obj: Any):
        # For each of the options, run a validator
        ...

PrimitiveTypes = str | bool | float | int
ContainerTypes = list | dict
ValidationTypes = Callable | OPTION | PrimitiveTypes | ContainerTypes[PrimitiveTypes | HAS | OPTION]

# class Optional:
#     ...

class Validator:
    """
    
    The Validator accepts a dict following the ValidationSchema pattern.
    """

    # TODO: define call function, handle all the cases!

class ValidationSchema(dict[str, ValidationTypes]): 
    """
    A JSON-like dict where:
    - Keys are str
    - Values are processable by the Validator
    """

    # TODO: validate this on load, basically what Pydantic does.
    #       ... Maybe just use pydantic?
    ...