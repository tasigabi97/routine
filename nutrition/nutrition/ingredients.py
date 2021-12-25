from . import *


class Water(Ingredient):
    ...


class VeganProteinBU(Ingredient):
    data = (74, 13, 7.8)
    max_total_g = 250


class CollagenProteinMP(Ingredient):
    data = (90, 0, 0)
    max_total_g = 50


class Chia(Ingredient):
    data = (16.54, 42.12, 30.8)
    max_total_g = 20


class Linseed(Ingredient):
    data = (22.3, 7.7, 36.5)
    max_total_g = 100


class RiceWhite(Ingredient):
    data = (8, 77, 0.5)
    max_total_g = 350


class CacaoBellaAldi(Ingredient):
    data = (23, 10, 11)
    max_total_g = 30


class GherkinPenny3_6cm(Ingredient):
    data = (0.8, 2.9, 0.1)
    max_total_g = 200


class CoconutOil(Ingredient):
    data = (0, 0, 98)
    max_total_g = 20


class Honey(Ingredient):
    data = (0.4, 76.4, 0)
    max_total_g = 30
