"""Module to hold common useful functions.
"""
# import importlib
# import inspect
# import pkgutil
import pkg_resources

def load_engines(group):
    """Find all the classes that implements `base_class`."""
    engines = {}

    # for _, module_name, _ in pkgutil.walk_packages([path], prefix=prefix):
    #     module = importlib.import_module(module_name)

    #     for klass_name, klass in inspect.getmembers(module, inspect.isclass):
    #         is_engine = (issubclass(klass, base_class) and
    #             klass != base_class and
    #             hasattr(klass, "command"))

    #         if is_engine:
    #             engines[klass.command] = klass

    for entry_point in pkg_resources.iter_entry_points(group=group):
        engines[entry_point.name] = entry_point.load()

    return engines
