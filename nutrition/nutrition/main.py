from . import *


@typechecked
def main(body_weight_in_kg: int, expected_g_of_protein_per_kg: float, expected_g_of_carbohydrate_per_kg: float, expected_g_of_fat_per_kg: float, mode: str) -> None:
    expected_total_g_of_protein, expected_total_g_of_carbohydrate, expected_total_g_of_fat = (
        body_weight_in_kg * expected_g_of_protein_per_kg,
        body_weight_in_kg * expected_g_of_carbohydrate_per_kg,
        body_weight_in_kg * expected_g_of_fat_per_kg,
    )
    expected_kcal_from_protein, expected_kcal_from_carbohydrate, expected_kcal_from_fat = (
        expected_total_g_of_protein * 4,
        expected_total_g_of_carbohydrate * 4,
        expected_total_g_of_fat * 9,
    )
    expected_total_kcal = expected_kcal_from_protein + expected_kcal_from_carbohydrate + expected_kcal_from_fat
    expected_protein_kcal_ratio, expected_carbohydrate_kcal_ratio, expected_fat_kcal_ratio = (
        expected_kcal_from_protein / expected_total_kcal,
        expected_kcal_from_carbohydrate / expected_total_kcal,
        expected_kcal_from_fat / expected_total_kcal,
    )
    remaining_g_of_protein, remaining_g_of_carbohydrate, remaining_g_of_fat = (
        expected_total_g_of_protein - Ingredient.get_total_protein(),
        expected_total_g_of_carbohydrate - Ingredient.get_total_carbohydrate(),
        expected_total_g_of_fat - Ingredient.get_total_fat(),
    )
    remaining_kcal_from_protein, remaining_kcal_from_carbohydrate, remaining_kcal_from_fat = (
        max(remaining_g_of_protein, 0) * 4,
        max(remaining_g_of_carbohydrate, 0) * 4,
        max(remaining_g_of_fat, 0) * 9,
    )
    remaining_kcal = remaining_kcal_from_protein + remaining_kcal_from_carbohydrate + remaining_kcal_from_fat
    remaining_protein_kcal_ratio, remaining_carbohydrate_kcal_ratio, remaining_fat_kcal_ratio = (
        remaining_kcal_from_protein / remaining_kcal,
        remaining_kcal_from_carbohydrate / remaining_kcal,
        remaining_kcal_from_fat / remaining_kcal,
    )
    if mode == FAT_LOSS:
        assert 2 <= expected_g_of_protein_per_kg <= 2.5, expected_g_of_protein_per_kg
        assert 0.4 <= expected_protein_kcal_ratio <= 0.5, expected_protein_kcal_ratio
        assert 0.1 <= expected_carbohydrate_kcal_ratio <= 0.3, expected_carbohydrate_kcal_ratio
        assert 0.3 <= expected_fat_kcal_ratio <= 0.4, expected_fat_kcal_ratio
    elif mode == BULKING:
        assert 1.43 <= expected_g_of_protein_per_kg <= 1.8, expected_g_of_protein_per_kg
        assert 0.25 <= expected_protein_kcal_ratio <= 0.35, expected_protein_kcal_ratio
        assert 0.45 <= expected_carbohydrate_kcal_ratio <= 0.65, expected_carbohydrate_kcal_ratio
        assert 0.15 <= expected_fat_kcal_ratio <= 0.25, expected_fat_kcal_ratio
    else:
        raise UserWarning
    ingredients = sorted(Ingredient.classes, key=lambda _: _.get_kcal_ratio_distance(remaining_protein_kcal_ratio, remaining_carbohydrate_kcal_ratio, remaining_fat_kcal_ratio))[:5]
    print("\n" * 30)
    print(f"You should eat {int(expected_total_g_of_protein)}/{int(expected_total_g_of_carbohydrate)}/{int(expected_total_g_of_fat)} g protein/carbohydrate/fat today.")
    print(f"Your recommended calories intake is {int(expected_total_kcal)} kcal.")
    print(f"Your recommended calorie ratio is {int(100*expected_protein_kcal_ratio)}/{int(100*expected_carbohydrate_kcal_ratio)}/{int(100*expected_fat_kcal_ratio)} %.")
    print(f"Your should eat more {int(remaining_g_of_protein)}/{int(remaining_g_of_carbohydrate)}/{int(remaining_g_of_fat)} g protein/carbohydrate/fat today.")
    print(f"Your remaining calorie ratio is {int(100*remaining_protein_kcal_ratio)}/{int(100*remaining_carbohydrate_kcal_ratio)}/{int(100*remaining_fat_kcal_ratio)} %.")
    print(f"Ingredients with smallest calorie ratio distance:")
    for ingredient in ingredients:
        print(f"\t{ingredient}")
    suggested_ingredients = get_suggested_ingredients(Ingredient.get_available_ingredient_types(), remaining_g_of_protein, remaining_g_of_carbohydrate, remaining_g_of_fat)
    if suggested_ingredients:
        print(f"Suggestions:")
        for _ in suggested_ingredients:
            print(f"\t{_}")
