from . import *


@typechecked
class IngredientMeta(type):
    def __str__(self) -> str:
        return f"{self.__name__}{dict(sorted([(k,v) for k,v in self.__dict__.items() if not k.startswith('__')]))}"

    def __neg__(self) -> "IngredientMeta":
        self.available = False
        return self

    def __pos__(self) -> "IngredientMeta":
        if self.available:
            self.set_free()
        else:
            self.available = True
        return self
