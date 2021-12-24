from . import *


class IngredientMeta(type):
    def __str__(self) -> str:
        return f"{self.__name__}{dict(sorted([(k,v) for k,v in self.__dict__.items() if not k.startswith('__')]))}"
