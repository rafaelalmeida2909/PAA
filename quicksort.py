import random
import time

import matplotlib.pyplot as plt
import numpy as np


class QuickSort:
    def __init__(self):
        self.comparacoes = 0
        self.trocas = 0

    def zerar_contadores(self):
        self.comparacoes = 0
        self.trocas = 0

    def trocar(self, arr, i, j):
        self.trocas += 1
        arr[i], arr[j] = arr[j], arr[i]

    def particionar_primeiro_pivo(self, arr, inicio, fim):
        pivo = arr[inicio]
        i = inicio + 1

        for j in range(inicio + 1, fim + 1):
            self.comparacoes += 1
            if arr[j] < pivo:
                self.trocar(arr, i, j)
                i += 1

        self.trocar(arr, inicio, i - 1)
        return i - 1

    def particionar_pivo_aleatorio(self, arr, inicio, fim):
        indice_pivo = random.randint(inicio, fim)
        self.trocar(arr, inicio, indice_pivo)
        return self.particionar_primeiro_pivo(arr, inicio, fim)

    def particionar_pivo_meio(self, arr, inicio, fim):
        indice_pivo = (inicio + fim) // 2
        self.trocar(arr, inicio, indice_pivo)
        return self.particionar_primeiro_pivo(arr, inicio, fim)

    def quicksort(self, arr, inicio, fim, funcao_particao):
        if inicio < fim:
            indice_pivo = funcao_particao(arr, inicio, fim)
            self.quicksort(arr, inicio, indice_pivo - 1, funcao_particao)
            self.quicksort(arr, indice_pivo + 1, fim, funcao_particao)


def ler_vetores(nome_arquivo):
    vetores = []
    with open(nome_arquivo, "r", encoding="utf-8-sig") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha:
                numeros = [num for num in linha.split() if num]
                vetor = [int(num) for num in numeros]
                vetores.append(vetor)
    return vetores


def medir_desempenho(vetores, ordenador):
    resultados = {
        "Pivô Primeiro": {"tempos": [], "comparacoes": [], "trocas": []},
        "Pivô Aleatório": {"tempos": [], "comparacoes": [], "trocas": []},
        "Pivô Meio": {"tempos": [], "comparacoes": [], "trocas": []},
    }

    estrategias = [
        ("Pivô Primeiro", ordenador.particionar_primeiro_pivo),
        ("Pivô Aleatório", ordenador.particionar_pivo_aleatorio),
        ("Pivô Meio", ordenador.particionar_pivo_meio),
    ]

    for vetor in vetores:
        for nome_estrategia, funcao_particao in estrategias:
            tempos_execucao = []
            for _ in range(5):
                vetor_teste = vetor.copy()
                ordenador.zerar_contadores()

                tempo_inicio = time.perf_counter()
                ordenador.quicksort(
                    vetor_teste, 0, len(vetor_teste) - 1, funcao_particao
                )
                tempo_fim = time.perf_counter()

                tempos_execucao.append(tempo_fim - tempo_inicio)

            resultados[nome_estrategia]["tempos"].append(
                np.mean(tempos_execucao) * 1000
            )
            resultados[nome_estrategia]["comparacoes"].append(ordenador.comparacoes)
            resultados[nome_estrategia]["trocas"].append(ordenador.trocas)

    return resultados


def plotar_resultados(resultados, tamanhos_vetores):
    metricas = ["tempos", "comparacoes", "trocas"]
    titulos = ["Tempo de Execução (ms)", "Número de Comparações", "Número de Trocas"]

    fig, axes = plt.subplots(3, 1, figsize=(12, 18))
    cores = ["#2ecc71", "#3498db", "#e74c3c"]

    for idx, (metrica, titulo) in enumerate(zip(metricas, titulos)):
        for estrategia, cor in zip(resultados.keys(), cores):
            axes[idx].plot(
                tamanhos_vetores,
                resultados[estrategia][metrica],
                label=estrategia,
                marker="o",
                color=cor,
                linewidth=2,
            )

        axes[idx].set_xlabel("Tamanho do Vetor")
        axes[idx].set_ylabel(titulo)
        axes[idx].grid(True, linestyle="--", alpha=0.7)
        axes[idx].legend(loc="upper left")
        axes[idx].set_title(titulo, pad=20)

        for estrategia in resultados.keys():
            media = np.mean(resultados[estrategia][metrica])
            axes[idx].legend_.texts[-1].set_text(f"{estrategia}")

    plt.tight_layout()
    plt.savefig("analise_quicksort.png", dpi=300, bbox_inches="tight")
    plt.close()


def imprimir_estatisticas(resultados, tamanhos_vetores):
    print("\nEstatísticas de Desempenho:")
    print("-" * 50)

    for estrategia in resultados.keys():
        print(f"\n{estrategia}:")
        for metrica in ["tempos", "comparacoes", "trocas"]:
            valores = resultados[estrategia][metrica]
            media = np.mean(valores)
            desvio = np.std(valores)
            minimo = min(valores)
            maximo = max(valores)

            print(f"  {metrica.capitalize()}:")
            print(f"    Média: {media:.2f}")
            print(f"    Desvio Padrão: {desvio:.2f}")
            print(f"    Mínimo: {minimo:.2f}")
            print(f"    Máximo: {maximo:.2f}")


ordenador = QuickSort()
print("Lendo vetores do arquivo...")
vetores = ler_vetores("vetores_quicksort.txt")
tamanhos_vetores = [len(v) for v in vetores]
print(f"Foram lidos {len(vetores)} vetores")
print(f"Variação de tamanho: {min(tamanhos_vetores)} a {max(tamanhos_vetores)}")

print("\nExecutando ordenação...")
resultados = medir_desempenho(vetores, ordenador)

print("\nGerando visualizações...")
plotar_resultados(resultados, tamanhos_vetores)
imprimir_estatisticas(resultados, tamanhos_vetores)
