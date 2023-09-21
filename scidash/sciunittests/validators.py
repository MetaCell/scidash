import json
import importlib
from scidash.sciunittests.models import TestClass
import numpy as np
import quantities as pq
import sciunit

import jsonpickle
from copy import deepcopy

# Register the sciunit quantity handlers
jsonpickle.handlers.register(pq.Quantity, handler=sciunit.base.QuantitiesHandler)
jsonpickle.handlers.register(pq.UnitQuantity, handler=sciunit.base.UnitQuantitiesHandler)


def build_destructured_unit(unit_dict):
    unit = pq.UnitQuantity(
        unit_dict.get('name'),
        import_class(unit_dict.get('base').get('quantity')) *
        unit_dict.get('base').get('coefficient'), unit_dict.get('symbol')
    )

    return unit


def import_class(import_path: str) -> object:
    """ Import class from import_path

    :type str:
    :param import_path: path to module similar to path.to.module.ClassName

    :returns: imported class
    """

    splitted = import_path.split('.')

    class_name = splitted[-1:][0]
    module_path = ".".join(splitted[:-1])

    imported_module = importlib.import_module(module_path)
    klass = getattr(imported_module, class_name)

    return klass


class TestInstanceValidator:

    @classmethod
    def validate(cls, data, fallback_observation_schema=None):
        try:
            # old style
            sciunit.settings['PREVALIDATE'] = True
        except:
            # new style
            try:
                sciunit.config_set('PREVALIDATE', True)
            except:
                sciunit.config.set('PREVALIDATE', True)

        class_data = data.get('test_class')
        if not class_data:
            class_data = data.get('test').get('_class')

        if not class_data.get('import_path', False):
            return data

        test_class = import_class(class_data.get('import_path'))

        observation_schema = test_class.observation_schema
        if not observation_schema:
            observation_schema = class_data.get("observation_schema")
            if not observation_schema:
                observation_schema = fallback_observation_schema

        observation = deepcopy(data.get('observation'))  # json of observation

        # Thicken the JSON with metadata required for deserialization
        for key, value in observation.items():
            if isinstance(value, dict) and 'units' in value:
                observation[key] = {'py/object': 'quantities.quantity.Quantity',
                                    'py/state': value}

        # Check observations for values without units
        has_units = False
        for key, value in observation.items():
            if isinstance(value, dict):
                has_units = True

        observation = json.dumps(observation)  # As string for decoding
        observation = jsonpickle.decode(observation)  # decode

        if has_units:
            # some/all observation items have units, use the observation
            obs_with_units = observation
        else:
            # none of the observation items have units, let try to get them from the (class)template
            obs_with_units = cls.add_units_to_observation(class_data, test_class, observation, fallback_observation_schema)

        test_class(obs_with_units)

        return data

    @classmethod
    def add_units_to_observation(cls, class_data, test_class, observation, fallback_observation_schema=None):
        without_units = []
        if class_data.get("units"):
            try:
                destructured = json.loads(class_data.get('units'))
            except json.JSONDecodeError:
                quantity = import_class(class_data.get('units'))
            else:
                if destructured.get('name', False):
                    quantity = build_destructured_unit(destructured)
                else:
                    quantity = destructured
        else:
            quantity = 1


        def filter_units(schema):
            result = []
            for key, rules in schema.items():
                if not rules.get('units', False):
                    result.append(key)

            return result

        observation_schema = test_class.observation_schema
        if not observation_schema:
            observation_schema = class_data.get("observation_schema")
            if not observation_schema:
                observation_schema = fallback_observation_schema

        if isinstance(observation_schema, list):
            for schema in observation_schema:
                if isinstance(schema, tuple) or len(schema)>1:
                    without_units += filter_units(schema[1])
                else:
                    without_units += filter_units(schema)
        elif observation_schema:
            without_units = filter_units(observation_schema)

        def process_obs(obs):
            try:
                obs = int(obs)
            except ValueError:
                obs = np.array(json.loads(obs))

            return obs

        if not isinstance(quantity, dict):
            obs_with_units = {
                x: (
                    process_obs(y) * quantity
                    if x not in without_units else process_obs(y)
                )
                for x, y in observation.items()
            }
        else:
            obs_with_units = {
                x: (
                    process_obs(y) * import_class(quantity[x])
                    if x not in without_units else process_obs(y)
                )
                for x, y in observation.items()
            }
        return obs_with_units
