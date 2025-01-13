import math
from collections import defaultdict
from itertools import combinations


class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, outro):
        return self.x == outro.x and self.y == outro.y

    def __hash__(self):
        return hash((self.x, self.y))


def sao_colineares(pontos):
    if len(pontos) <= 2:
        return True

    for i in range(len(pontos) - 2):
        x1, y1 = pontos[i].x, pontos[i].y
        x2, y2 = pontos[i + 1].x, pontos[i + 1].y
        x3, y3 = pontos[i + 2].x, pontos[i + 2].y

        area = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
        if area != 0:
            return False
    return True


def encontrar_grupos_colineares(pontos):
    grupos = []
    n = len(pontos)

    for tamanho in range(2, n + 1):
        for combo in combinations(pontos, tamanho):
            if sao_colineares(combo):
                grupos.append(list(combo))

    return grupos


def resolver_passos_minimos(pontos):
    if not pontos:
        return 0, 1

    n = len(pontos)
    pontos = [Ponto(x, y) for x, y in pontos]
    grupos_colineares = encontrar_grupos_colineares(pontos)

    memoria = {}

    def obter_chave_estado(pontos_restantes):
        return tuple(sorted((p.x, p.y) for p in pontos_restantes))

    def resolver_recursivo(pontos_restantes):
        if not pontos_restantes:
            return 0, 1

        chave_estado = obter_chave_estado(pontos_restantes)
        if chave_estado in memoria:
            return memoria[chave_estado]

        passos_minimos = float("inf")
        total_maneiras = 0

        for grupo in grupos_colineares:
            if all(p in pontos_restantes for p in grupo):
                novos_restantes = [p for p in pontos_restantes if p not in grupo]
                sub_passos, sub_maneiras = resolver_recursivo(novos_restantes)

                if sub_passos + 1 < passos_minimos:
                    passos_minimos = sub_passos + 1
                    total_maneiras = sub_maneiras
                elif sub_passos + 1 == passos_minimos:
                    total_maneiras += sub_maneiras

        memoria[chave_estado] = (passos_minimos, total_maneiras)
        return passos_minimos, total_maneiras

    return resolver_recursivo(pontos)


exemplo1 = [(0, 0), (0, 1), (1, 0)]
print(resolver_passos_minimos(exemplo1))

exemplo2 = [(3, 4), (3, 5), (3, 6), (5, 5)]
print(resolver_passos_minimos(exemplo2))
