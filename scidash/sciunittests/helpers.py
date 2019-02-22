import importlib


def get_observation_schema(import_path):
    splitted = import_path.split('.')

    class_name = splitted[-1:][0]
    module_path = ".".join(splitted[:-1])

    imported_module = importlib.import_module(module_path)
    klass = getattr(imported_module, class_name)

    observation_schema = klass.observation_schema
    result = {}

    for schema in observation_schema:
        result = {**result, **schema}

    return result


def get_test_parameters_schema(import_path):
    splitted = import_path.split('.')

    class_name = splitted[-1:][0]
    module_path = ".".join(splitted[:-1])

    imported_module = importlib.import_module(module_path)
    klass = getattr(imported_module, class_name)

    params_schema = klass.params_schema

    return params_schema
