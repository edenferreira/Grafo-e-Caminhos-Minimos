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
        self.arestas_chegando = defaultdict(list)
        self.pesos = {}
        self.num_arestas = 0
        self.nome_mapa = ''

    def __len__(self):
        return len(self.pontos)

    def add_ponto(self, ponto, pos_x, pos_y):
        self.pontos.add(ponto)
        self.pos_pontos[ponto] = (pos_x, pos_y)

    def add_aresta(self, ponto_origem, ponto_destino, peso, chance_dupla=0, direcionada=True):
        self.arestas[ponto_origem].append(ponto_destino)
        self.arestas_chegando[ponto_destino].append(ponto_origem)
        self.pesos[ponto_origem, ponto_destino] = peso
        self.num_arestas += 1
        if rnd.randint(1, 100) <= chance_dupla or not direcionada:
            self.arestas[ponto_destino].append(ponto_origem)
            self.arestas_chegando[ponto_origem].append(ponto_destino)
            self.pesos[ponto_destino, ponto_origem] = peso
            self.num_arestas += 1

    def calc_distancia(self, ponto_origem, ponto_destino):
        return sqrt(((self.pos_pontos[ponto_destino][0] - self.pos_pontos[ponto_origem][0]) ** 2)
                    + ((self.pos_pontos[ponto_destino][1] - self.pos_pontos[ponto_origem][1]) ** 2))

    def calc_peso(self, ponto_origem, ponto_destino, velocidade=1):
        return self.calc_distancia(ponto_origem, ponto_destino) / velocidade

    def calc_previsao_peso(self, ponto_origem, ponto_destino):
        return self.calc_distancia(ponto_origem, ponto_destino)

    def gerar_grafo_mapa(self,path_arquivo,nome_mapa):
        self.nome_mapa = nome_mapa
        with open(path_arquivo+'.co','r') as arq:
            for li in arq.readlines():
                s = li.strip('v ').split(' ')
                self.add_ponto(int(li[0]),int(li[1]),int(li[2]))

        with open(path_arquivo+'.gr','r') as arq:
            for li in arq.readlines():
                s = li.strip('a ').split(' ')
                self.add_aresta(int(li[0]),int(li[1]),int(li[2]))

    def gerar_grafo_cidade(self, grid_x, grid_y, max_x, max_y, distancia_min):
        fracao_x = max_x / grid_x
        fracao_y = max_y / grid_y

        self.max_x = max_x
        self.max_y = max_y

        tam_min_x = distancia_min / 2
        tam_max_x = fracao_x - tam_min_x
        tam_min_y = distancia_min / 2
        tam_max_y = fracao_y - tam_min_y

        x_1 = tam_min_x
        x_2 = tam_max_x
        y_1 = tam_min_y
        y_2 = tam_max_y
        p_x = {}
        p_y = {}
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
                self.add_ponto((key_x * 1000000) + key_y, rnd.uniform(x[0], x[1]), rnd.uniform(y[0], y[1]))

        for i in range(grid_x - 1):
            for j in range(grid_y - 1):
                ponto_atual = (i * 1000000) + j
                ponto_direita = (i * 1000000) + j + 1
                ponto_abaixo = ((i + 1) * 1000000) + j
                if (i / 1000000) % 2 == 0:
                    self.add_aresta(ponto_atual, ponto_direita, self.calc_distancia(ponto_atual, ponto_direita), 20)
                else:
                    self.add_aresta(ponto_direita, ponto_atual, self.calc_distancia(ponto_direita, ponto_atual), 20)
                if j % 2 == 0:
                    self.add_aresta(ponto_abaixo, ponto_atual, self.calc_distancia(ponto_abaixo, ponto_atual), 20)
                else:
                    self.add_aresta(ponto_atual, ponto_abaixo, self.calc_distancia(ponto_atual, ponto_abaixo), 20)