from . import *


def get_suggested_ingredients(
    ingredient_types: Set[IngredientMeta], remaining_g_of_protein: float, remaining_g_of_carbohydrate: float, remaining_g_of_fat: float
) -> Union[List[Ingredient], None]:
    solver = Solver.CreateSolver("GLOP")
    variable_and_ingredient_types = [(solver.NumVar(0, _.get_unused_ingredient_weight_in_g(), _.__name__), _) for _ in ingredient_types if _.get_unused_ingredient_weight_in_g()]
    inequality_strs = []
    for constraint_type in (
        ">=",
        "<=",
    ):
        for coefficient_getter_name, remaining_g in [
            (Ingredient.get_protein_per_1g.__name__, remaining_g_of_protein),
            (Ingredient.get_carbohydrate_per_1g.__name__, remaining_g_of_carbohydrate),
            (Ingredient.get_fat_per_1g.__name__, remaining_g_of_fat),
        ]:
            for i, (variable, ingredient_type) in enumerate(variable_and_ingredient_types):
                coefficient = getattr(ingredient_type, coefficient_getter_name)()
                if i == 0:
                    inequality = coefficient * variable
                    inequality_str = f"{coefficient} * {variable}"
                else:
                    inequality = inequality + (coefficient * variable)
                    inequality_str += f" + {coefficient} * {variable}"
            remaining_g = max(0, remaining_g)
            constraint_g = remaining_g if constraint_type == ">=" else remaining_g + 2
            inequality = inequality >= constraint_g if constraint_type == ">=" else inequality <= constraint_g
            inequality_strs.append(f"{inequality_str} {constraint_type} {constraint_g}")
            solver.Add(inequality)
    for i, (variable, ingredient_type) in enumerate(variable_and_ingredient_types):
        coefficient = ingredient_type.get_cost_per_1g()
        if i == 0:
            cost = coefficient * variable
            cost_str = f"Z = {coefficient} * {variable}"
        else:
            cost = cost + (coefficient * variable)
            cost_str += f" + {coefficient} * {variable}"
    solver.Minimize(cost)
    if solver.Solve() == Solver.OPTIMAL:
        return sorted(
            [ingredient_type(int(variable.solution_value())) for variable, ingredient_type in variable_and_ingredient_types if variable.solution_value() >= 1], reverse=True
        )
    else:
        print(f"Can't suggest!")
        for variable, ingredient_type in variable_and_ingredient_types:
            print(f"\t{variable}[{variable.Lb()}, {variable.Ub()}]")
        for inequality_str in inequality_strs:
            print(f"\t{inequality_str}")
        print(f"\t{cost_str}")
