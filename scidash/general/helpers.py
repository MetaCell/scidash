import importlib


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
