import inspect


class IDGenerator:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.id = 0
        return cls.__instance

    def generate_id(self):
        id_value = self.id
        self.id += 1
        return id_value


def memoize(func):
    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]
        else:
            result = func(*args)
            cache[args] = result
            return result

    return wrapper


@memoize
def type_to_params(_class: type) -> list[str]:
    init_params = inspect.signature(_class.__init__).parameters
    param_names = [param_name for param_name in init_params if param_name != "self"]
    return param_names
