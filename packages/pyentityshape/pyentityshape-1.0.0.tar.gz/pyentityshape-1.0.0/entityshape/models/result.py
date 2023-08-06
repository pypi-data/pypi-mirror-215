from typing import Any, Dict, List, Set

from pydantic import BaseModel, Field

from entityshape.enums import Necessity, PropertyResponse, StatementResponse
from entityshape.models.property_value import PropertyValue
from entityshape.models.statement_value import StatementValue


class Result(BaseModel):
    error: str = ""  # always empty?
    general: Dict[Any, Any] = {}
    name: str = ""
    properties: Dict[str, PropertyValue] = {}
    schema_: str = Field("", alias="schema")
    statements: Dict[Any, StatementValue] = {}
    validity: Dict[Any, Any] = {}  # always empty
    missing_properties: List[str] = []
    required_properties: List[str] = []
    incorrect_statements: List[str] = []
    properties_with_too_many_statements: List[str] = []
    analyzed: bool = False
    required_properties_that_are_missing: Set[str] = set()
    optional_properties_that_are_missing: Set[str] = set()

    @property
    def some_required_properties_are_missing(self):
        return bool(self.required_properties_that_are_missing)

    @property
    def properties_with_too_many_statements_found(self):
        return bool(self.properties_with_too_many_statements)

    @property
    def incorrect_statements_found(self):
        return bool(self.incorrect_statements)

    @property
    def is_valid(self) -> bool:
        """check if the properties are all allowed,
        all required properties are present,
        not too many statements,
        and none of the statements are incorrect"""
        self.analyze()
        return bool(
            not self.properties_with_too_many_statements_found
            and not self.incorrect_statements_found
            and not self.some_required_properties_are_missing
        )

    @property
    def is_empty(self):
        return bool(len(self.properties) == 0 and len(self.statements) == 0)

    def analyze(self):
        if not self.analyzed:
            self.__find_missing_properties__()
            self.__find_required_properties__()
            self.__find_incorrect_statements__()
            self.__find_properties_with_too_many_statements__()
            self.__find_required_properties_that_are_missing__()
            self.__find_optional_properties_that_are_missing__()
            self.analyzed = True

    def __find_properties_with_too_many_statements__(self):
        for property_ in self.properties:
            value: PropertyValue = self.properties[property_]
            if value.response == PropertyResponse.TOO_MANY_STATEMENTS:
                self.properties_with_too_many_statements.append(property_)

    def __find_incorrect_statements__(self):
        for statement in self.statements:
            value: StatementValue = self.statements[statement]
            if value.response == StatementResponse.INCORRECT:
                self.incorrect_statements.append(statement)

    def __find_required_properties__(self):
        for property_ in self.properties:
            value: PropertyValue = self.properties[property_]
            if value.necessity == Necessity.REQUIRED:
                self.required_properties.append(property_)

    def __find_missing_properties__(self):
        for property_ in self.properties:
            value: PropertyValue = self.properties[property_]
            if value.response == PropertyResponse.MISSING:
                self.missing_properties.append(property_)

    def __find_required_properties_that_are_missing__(self):
        a = set(self.missing_properties)
        b = set(self.required_properties)
        # the intersection between these two should be empty
        # if all required properties are present
        self.required_properties_that_are_missing = a.intersection(b)

    def __find_optional_properties_that_are_missing__(self):
        """We calculate using set difference"""
        a = set(self.missing_properties)
        b = set(self.required_properties)
        self.optional_properties_that_are_missing = a.difference(b)
