from . import *


class Ingredient(metaclass=IngredientMeta):
    macros: Union[Tuple[int, float, float, float], Tuple[float, float, float]] = (0, 0, 0)
    cost = (1, 0.01)
    max_total_g = 1000
    ingredients: List["Ingredient"] = []
    classes: Set[type] = set()
    available = False

    def __init_subclass__(cls):
        Ingredient.classes.add(cls)

    @classmethod
    def get_portion_and_protein_and_carbohydrate_and_fat(cls) -> Tuple[int, float, float, float]:
        return cls.macros if len(cls.macros) == 4 else (100, *cls.macros)

    @classmethod
    def get_cost_per_1g(cls) -> float:
        g, ft = cls.cost
        return ft / g

    @classmethod
    def get_protein_per_1g(cls) -> float:
        portion, protein, _, __ = cls.get_portion_and_protein_and_carbohydrate_and_fat()
        return protein / portion

    @classmethod
    def get_carbohydrate_per_1g(cls) -> float:
        portion, _, carbohydrate, __ = cls.get_portion_and_protein_and_carbohydrate_and_fat()
        return carbohydrate / portion

    @classmethod
    def get_fat_per_1g(cls) -> float:
        portion, _, __, fat = cls.get_portion_and_protein_and_carbohydrate_and_fat()
        return fat / portion

    @classmethod
    def get_protein_kcal_per_1g(cls) -> float:
        return 4 * cls.get_protein_per_1g()

    @classmethod
    def get_carbohydrate_kcal_per_1g(cls) -> float:
        return 4 * cls.get_carbohydrate_per_1g()

    @classmethod
    def get_fat_kcal_per_1g(cls) -> float:
        return 9 * cls.get_fat_per_1g()

    @classmethod
    def get_kcal_per_1g(cls) -> float:
        return cls.get_protein_kcal_per_1g() + cls.get_carbohydrate_kcal_per_1g() + cls.get_fat_kcal_per_1g()

    @classmethod
    def get_protein_kcal_ratio(cls) -> float:
        kcal_per_1g = cls.get_kcal_per_1g()
        return cls.get_protein_kcal_per_1g() / kcal_per_1g if kcal_per_1g else 0

    @classmethod
    def get_carbohydrate_kcal_ratio(cls) -> float:
        kcal_per_1g = cls.get_kcal_per_1g()
        return cls.get_carbohydrate_kcal_per_1g() / kcal_per_1g if kcal_per_1g else 0

    @classmethod
    def get_fat_kcal_ratio(cls) -> float:
        kcal_per_1g = cls.get_kcal_per_1g()
        return cls.get_fat_kcal_per_1g() / kcal_per_1g if kcal_per_1g else 0

    @classmethod
    def get_kcal_ratio_distance(cls, protein_kcal_ratio: float, carbohydrate_kcal_ratio: float, fat_kcal_ratio: float) -> float:
        protein_surplus = cls.get_protein_kcal_ratio() - protein_kcal_ratio
        carbohydrate_surplus = cls.get_carbohydrate_kcal_ratio() - carbohydrate_kcal_ratio
        fat_surplus = cls.get_fat_kcal_ratio() - fat_kcal_ratio
        if protein_surplus >= 0:
            protein_deficit = 0
        else:
            protein_deficit = abs(protein_surplus)
            protein_surplus = 0
        if carbohydrate_surplus >= 0:
            carbohydrate_deficit = 0
        else:
            carbohydrate_deficit = abs(carbohydrate_surplus)
            carbohydrate_surplus = 0
        if fat_surplus >= 0:
            fat_deficit = 0
        else:
            fat_deficit = abs(fat_surplus)
            fat_surplus = 0
        return (protein_surplus * 1) + (carbohydrate_surplus * 1.5) + (fat_surplus * 1.5) + (protein_deficit * 1.7) + (carbohydrate_deficit * 1) + (fat_deficit * 1.5)

    def __add__(self, other):
        return other

    def __lt__(self, other) -> bool:
        return self.weight_in_g < other.weight_in_g

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.weight_in_g} g)"

    @classmethod
    def get_total_ingredient_weight_in_g(cls) -> float:
        return sum([_.weight_in_g for _ in cls.ingredients if isinstance(_, cls)])

    @classmethod
    def get_unused_ingredient_weight_in_g(cls) -> float:
        return max(0, cls.max_total_g - cls.get_total_ingredient_weight_in_g())

    def __init__(self, weight_in_g: float = 0, available: bool = True, free: bool = False) -> None:
        self.weight_in_g = weight_in_g
        type(self).available = available
        if free:
            type(self).cost = (type(self).cost[0], 0)
        self.ingredients.append(self)
        total_weight = self.get_total_ingredient_weight_in_g()
        assert total_weight <= self.max_total_g, f"{total_weight}g {type(self).__name__} is more than max {self.max_total_g}g."

    @staticmethod
    def get_total_protein() -> float:
        return sum([_.get_protein_per_1g() * _.weight_in_g for _ in Ingredient.ingredients])

    @staticmethod
    def get_total_carbohydrate() -> float:
        return sum([_.get_carbohydrate_per_1g() * _.weight_in_g for _ in Ingredient.ingredients])

    @staticmethod
    def get_total_fat() -> float:
        return sum([_.get_fat_per_1g() * _.weight_in_g for _ in Ingredient.ingredients])

    @staticmethod
    def get_total_kcal() -> float:
        return sum([_.get_kcal_per_1g() * _.weight_in_g for _ in Ingredient.ingredients])

    @staticmethod
    def get_available_ingredient_types() -> Set[IngredientMeta]:
        return {_ for _ in Ingredient.classes if _.available}
