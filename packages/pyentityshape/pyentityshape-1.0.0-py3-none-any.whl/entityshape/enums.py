from enum import Enum


class Necessity(Enum):
    ABSENT = "absent"
    OPTIONAL = "optional"
    REQUIRED = "required"


class PropertyResponse(Enum):
    MISSING = "missing"
    PRESENT = "present"
    INCORRECT = "incorrect"
    TOO_MANY_STATEMENTS = "too many statements"
    CORRECT = "correct"


class StatementResponse(Enum):
    NOT_IN_SCHEMA = "not in schema"
    ALLOWED = "allowed"
    INCORRECT = "incorrect"
    CORRECT = "correct"
