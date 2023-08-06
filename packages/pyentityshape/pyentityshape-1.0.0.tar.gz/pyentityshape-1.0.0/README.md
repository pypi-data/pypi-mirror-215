# PyEntityshape
Python library to lookup Wikidata items in the entityshape API.

This is the alpha software. Please open an issue if you have any ideas or suggestions or bugs to report.  

# Features
It can be used programmatically to get the results of one validation at a time.

# Installation
Get it from pypi

`$ pip install pyentityshape`

# Usage
```
e = EntityShape(eid="E1", lang="en", qid="Q1")
result = e.get_result()
print(result)
result.is_valid
False|True
result.required_properties_that_are_missing
["P1", "P2"]
```

The result is a Result object with the following properties:
* some_required_properties_are_missing
* properties_with_too_many_statements_found
* incorrect_statements_found
* is_valid
* is_empty
* analyzed
* error
* general
* incorrect_statements
* missing_properties
* name
* optional_properties_that_are_missing
* properties
* properties_with_too_many_statements
* required_properties
* required_properties_that_are_missing
* schema_
* statements
* validity

# License
GPLv3+
