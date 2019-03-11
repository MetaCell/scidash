from scidash.general.helpers import import_class
import inspect


def get_observation_schema(import_path):
    klass = import_class(import_path)
    observation_schema = klass.observation_schema

    return observation_schema


def get_test_parameters_schema(import_path):
    klass = import_class(import_path)

    params_schema = klass.params_schema

    return params_schema


def get_units(import_path):
    klass = import_class(import_path)

    units = \
        f"{inspect.getmodule(klass.units).__package__}.{klass.units.symbol}"

    return units
