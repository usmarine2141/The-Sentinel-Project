import importlib.util, sys, os


__doc__ = "Module to perform relative imports and general module importation ..."

def load(path):
    for current, subdir, files in os.walk(os.path.dirname(path)):
        for file in files:
            if not file.endswith(".py"):
                continue
            if file == "__init__.py":
                continue
            module_name = os.path.basename(path).replace(".py", "")
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[spec.name] = module
    module_name = os.path.basename(path).replace(".py", "")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
