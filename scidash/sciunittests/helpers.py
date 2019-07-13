import inspect
import json

import quantities as pq

from scidash.general.helpers import import_class


def build_destructured_unit(unit_dict):
    unit = pq.UnitQuantity(
        unit_dict.get('name'),
        import_class(unit_dict.get('base').get('quantity')) *
        unit_dict.get('base').get('coefficient'), unit_dict.get('symbol')
    )

    return unit


def get_observation_schema(import_path):
    klass = import_class(import_path)
    observation_schema = klass.observation_schema

    if observation_schema is None:
        observation_schema = {}

    return observation_schema


def get_test_parameters_schema(import_path):
    klass = import_class(import_path)

    params_schema = klass.params_schema

    if params_schema is None:
        params_schema = {}

    return params_schema


def get_units(import_path):
    klass = import_class(import_path)

    if isinstance(klass.units, dict):
        str_units = {}

        for param in klass.units.keys():
            str_units.update(
                {
                    param: f"{inspect.getmodule(klass.units[param]).__package__}.{klass.units[param].symbol}"  # noqa: E501
                }
            )

        return json.dumps(str_units)

    units = \
        f"{inspect.getmodule(klass.units).__package__}.{klass.units.symbol}"

    def importable(unit):
        try:
            import_class(unit)
        except AttributeError:
            return False

        return True

    def destructure_custom_unit(unit):
        base_unit = list(unit.definition.dimensionality).pop()

        base_quantity = \
            f"{inspect.getmodule(unit).__package__}.{base_unit.symbol}"

        if not importable(base_quantity):
            base_quantity = "N/A"

        destructured = {
            'name': unit.name,
            'base': {
                'quantity': base_quantity,
                'coefficient': float(unit.definition.base)
            },
            'symbol': unit.symbol
        }

        return json.dumps(destructured)

    try:
        import_class(units)
    except AttributeError:
        units = destructure_custom_unit(klass.units)

    return units
