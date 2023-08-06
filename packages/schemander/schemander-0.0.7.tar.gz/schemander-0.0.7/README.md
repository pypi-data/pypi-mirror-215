# Schemander

> As in Schema + Commander... 
>
> ... it took me a while to connect the name with the "Fantastic Beasts and Where to Find Them" (2016) film, main character.

This module aims to simplify the way we handle JSON Schemas in Python, leveraging type annotations.

## Install

```
pip install schemander
```

When working with JSON is common to have situations in which string values are "blest" with extra meaning or behaviour such as dates, datetimes, email, phone numbers, amoung others. This module solves this by defining a class that we can extend called `InternalObjectTypeString`, which attempt to convert the value of the string in to an object while preserving the string version as a main display value, exposing the converted object via an attribute named `value`.

Moreover when converting a JSON in to a data structure, we usually have to pass through a dictionary, and then "cast" in to the desired representation we desire. For this we define a `Schema` from which we need to extend in order to define a schema where you will define attributes with a type-hint, `int`, `float`, `str`, `bool`, `typing.List` with a given type to have a homogeneous array (heterogeneous, are not supported) or a _class_ that will take the field value as only argument for construction, such as `UUID`, or some of the `InternalObjectTypeString` or `RegexValidatedString`.

An example on how to write for a _user_ could be found at `./example.py`.
