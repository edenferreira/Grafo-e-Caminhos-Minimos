__author__ = 'Eden Thiago Ferreira'
from collections import defaultdict
import random as rnd
from math import sqrt


class Grafo:
    """Mantem colecoes de pontos, arestas, e seus atributos, como posicoes, pesos, direcao"""

    def __init__(self, ident=0):
        self.ident = ident
        self.pontos = set()
        self.pos_pontos = defaultdict()
        self.arestas = defaultdict(list)
        self.pesos = {}
        self.nome_mapa = ''
        self.max_x = self.max_y = self.num_arestas = 0

    def __len__(self):
        return len(self.pontos)

    def add_ponto(self, ponto, pos_x, pos_y):
        self.pontos.add(ponto)
        self.pos_pontos[ponto] = (pos_x, pos_y)

    def add_aresta(self, ponto_origem, ponto_destino, peso, chance_dupla=0):
        self.arestas[ponto_origem].append(ponto_destino)
        self.pesos[ponto_origem, ponto_destino] = peso
        self.num_arestas += 1
        if rnd.randint(1, 100) <= chance_dupla:
            self.arestas[ponto_destino].append(ponto_origem)
            self.pesos[ponto_destino, ponto_origem] = peso
            self.num_arestas += 1

    def calc_dist(self, ponto_origem, ponto_destino):
        return sqrt(((self.pos_pontos[ponto_destino][0] - self.pos_pontos[ponto_origem][0]) ** 2)
                    + ((self.pos_pontos[ponto_destino][1] - self.pos_pontos[ponto_origem][1]) ** 2))

    def calc_peso(self, ponto_origem, ponto_destino):
        return self.calc_dist(ponto_origem, ponto_destino) * rnd.uniform(1, 2.0)

    def calc_prev_peso(self, ponto_origem, ponto_destino):
        return self.calc_dist(ponto_origem, ponto_destino)

    def gerar_grafo_mapa(self, path_arquivo, nome_mapa):
        self.nome_mapa = nome_mapa
        with open(path_arquivo + '.co', 'r') as arq:
            [self.add_ponto(int(li.strip('v ').split(' ')[0]),
                            int(li.strip('v ').split(' ')[1]),
                            int(li.strip('v ').split(' ')[2]))
             for li in arq.readlines()]

        with open(path_arquivo + '.gr', 'r') as arq:
            [self.add_aresta(int(li.strip('a ').split(' ')[0]),
                             int(li.strip('a ').split(' ')[1]),
                             int(li.strip('a ').split(' ')[2]))
             for li in arq.readlines()]

    def gerar_grafo(self, grid_x, grid_y, max_x, max_y, distancia_min):
        mult_ponto = 10000000

        fracao_x = max_x / grid_x
        fracao_y = max_y / grid_y

        self.max_x, self.max_y = max_x, max_y

        tam_min_x = distancia_min / 2
        tam_max_x = fracao_x - tam_min_x
        tam_min_y = distancia_min / 2
        tam_max_y = fracao_y - tam_min_y

        x_1, x_2 = tam_min_x, tam_max_x
        y_1, y_2 = tam_min_y, tam_max_y
        p_x = p_y = {}
        for i in range(grid_x):
            p_x[i] = (x_1, x_2)
            x_1 += fracao_x
            x_2 += fracao_x
        for i in range(grid_y):
            p_y[i] = (y_1, y_2)
            y_1 += fracao_y
            y_2 += fracao_y

        for key_x, x in p_x.items():
            for key_y, y in p_y.items():
                self.add_ponto((key_x * mult_ponto) + key_y, rnd.uniform(x[0], x[1]), rnd.uniform(y[0], y[1]))

        for i in range(grid_x - 1):
            for j in range(grid_y - 1):
                ponto_atual = (i * mult_ponto) + j
                ponto_direita = (i * mult_ponto) + j + 1
                ponto_abaixo = ((i + 1) * mult_ponto) + j
                if (i / mult_ponto) % 2 == 0:
                    self.add_aresta(ponto_atual, ponto_direita, self.calc_peso(ponto_atual, ponto_direita), 20)
                else:
                    self.add_aresta(ponto_direita, ponto_atual, self.calc_peso(ponto_direita, ponto_atual), 20)
                if j % 2 == 0:
                    self.add_aresta(ponto_abaixo, ponto_atual, self.calc_peso(ponto_abaixo, ponto_atual), 20)
                else:
                    self.add_aresta(ponto_atual, ponto_abaixo, self.calc_peso(ponto_atual, ponto_abaixo), 20)