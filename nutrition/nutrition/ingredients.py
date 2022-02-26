from . import *


class Water(Ingredient):
    ...


class VeganProteinBU(Ingredient):
    available = True
    macros = (74, 13, 7.8)
    max_total_g = 250
    cost = (2000, 16000)


class CollagenProteinMP(Ingredient):
    macros = (90, 0, 0)
    max_total_g = 50
    cost = (1000, 10000)


class Chia(Ingredient):
    available = True
    macros = (16.54, 42.12, 30.8)
    max_total_g = 20
    cost = (100, 375)


class Linseed(Ingredient):
    available = True
    macros = (22.3, 7.7, 36.5)
    max_total_g = 100
    cost = (500, 600)


class RiceWhite(Ingredient):
    macros = (8, 77, 0.5)
    max_total_g = 350
    cost = (1000, 500)


class CacaoBellaAldi(Ingredient):
    available = True
    macros = (23, 10, 11)
    max_total_g = 20
    cost = (250, 1050)


class GherkinPenny3_6cm(Ingredient):
    macros = (0.8, 2.9, 0.1)
    max_total_g = 200
    cost = (350, 300)


class Cashew(Ingredient):
    available = True
    macros = (18.22, 30.19, 43.85)
    max_total_g = 25
    cost = (500, 3300)


class PecanNut(Ingredient):
    available = True
    macros = (9.17, 13.86, 71.97)
    max_total_g = 25
    cost = (200, 1700)
