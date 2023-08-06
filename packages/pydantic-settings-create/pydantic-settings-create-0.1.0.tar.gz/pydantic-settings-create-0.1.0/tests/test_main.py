import pytest
from pydantic.v1.schema import field_class_to_schema

from src import create_settings


def get_schema(type_):
    if type_ is None:
        return
    for type, schema in field_class_to_schema:
        if type_ is type:
            return schema['type']
    raise ValueError
    return 'object'


def f1(a: list):
    ...


def f2(a: int, b):
    ...


def f3(a: int, /, b):
    ...


# ! WIP
@pytest.mark.parametrize(
    ['function', 'schema_properties_keys', 'schema_required', 'schema_properties_type'],
    [
        # [function_1],
        [lambda: None, set(), set(), {}],
        [lambda a: None, {'a'}, {'a'}, {}],
        [lambda a, b: None, {'a', 'b'}, {'a', 'b'}, {}],
        [lambda a, b=b'': None, {'a', 'b'}, {'a'}, {}],
        [f1, {'a'}, {'a'}, {'a': list}],
        [f2, {'a', 'b'}, {'a', 'b'}, {'a': int}],
        [f3, {'a', 'b'}, {'a', 'b'}, {'a': int}],
    ],
)
def test_create_settings(
    function,
    schema_properties_keys: set,
    schema_required: set,
    schema_properties_type: dict,
):
    # print(f'\n{function = }')

    settings_cls = create_settings(function)
    # print(f'\n{settings_cls = }')

    schema = settings_cls.model_json_schema()
    # print(f'\n{schema = }')

    schema_keys = schema.keys()
    # print(f'\n{schema_keys = }')
    assert 'additionalProperties' in schema_keys
    assert 'properties' in schema_keys
    # assert 'required' in  schema_keys
    assert 'title' in schema_keys
    assert 'type' in schema_keys

    properties: dict = schema['properties']
    # print(f'\n{properties = }')

    properties_keys = properties.keys()
    # print(f'\n{properties_keys = }')
    assert set(properties_keys) == schema_properties_keys

    required = schema.get('required', [])
    # print(f'\n{required = }')
    assert set(required) == schema_required

    for var, var_schema in properties.items():
        print(f'\n{var, var_schema = }')
        assert var_schema.get('type') == get_schema(schema_properties_type.get(var))
