__author__ = 'Eden Thiago Ferreira'
import cProfile as cp
import pstats as pst
from collections import OrderedDict
from grafos import *
from banco_dados import *
from caminhos_minimos import *

class Coletor:

    def __init__(self,grafo,nome_mapa=None,path_grafos=None):
        """se path_grafo é None ele gera o grafo aleatoriamente"""
        self.nome_mapa = nome_mapa

        if path_grafos is None:
            self.path_grafos = {}
        else:
            self.path_grafos = path_grafos

        self.grafo = grafo
        if nome_mapa is None:
            self.grafo.gerar_grafo(rnd.randint(1200,1600),rnd.randint(1200,1600),
                                   rnd.uniform(800,1200),rnd.uniform(800,1200),rnd.uniform(0.02,0.1))
        else:
            self.grafo.gerar_grafo_mapa(path_grafos[nome_mapa],nome_mapa)

        self.profiler = cp.Profile()
        self.pt_ori, self.pt_dest = rnd.sample(self.grafo.pontos,2)
        self.dij, self.ast = Dijkstra(self.grafo), AStar(self.grafo)
        self.executou = False

    def get_tempo(self):
        with open('status.txt','w') as arq:
            dados = pst.Stats(self.profiler,stream=arq)
            dados.strip_dirs().print_stats('(start)')

        stat = list()

        with open('status.txt','r') as arq:
            for li in arq.readlines():
                if 'start' in li:
                    stat.append((li.split()))
        return stat[1][4]

    def exec_dij(self):
        self.dij.pt_ori, self.dij.pt_dest = self.pt_ori, self.pt_dest
        self.profiler.enable()
        self.dij.start()
        self.profiler.disable()
        self.dij.tempo = self.get_tempo()

    def exec_ast(self):
        self.ast.pt_ori, self.ast.pt_dest = self.pt_ori, self.pt_dest
        self.profiler.enable()
        self.ast.start()
        self.profiler.disable()
        self.ast.tempo = self.get_tempo()

    def start(self):
        self.exec_dij()
        self.exec_ast()
        self.executou = True

    def dump_dados(self,con):
        if self.executou:
            if self.nome_mapa is None:
                con.inserir_grafo(self.grafo)
            else:
                con.inserir_grafo_mapa(self.grafo)

            dados_dij = OrderedDict()
            dados_dij['ponto_origem'] = self.dij.pt_ori
            dados_dij['ponto_destino'] = self.dij.pt_dest
            dados_dij['caminho'] = str(self.dij.caminho)
            dados_dij['num_passos'] = self.dij.num_passos
            dados_dij['distancia_total'] = self.dij.dist_total
            dados_dij['tempo'] = self.dij.tempo

            dados_ast = OrderedDict()
            dados_ast['ponto_origem'] = self.ast.pt_ori
            dados_ast['ponto_destino'] = self.ast.pt_dest
            dados_ast['caminho'] = str(self.ast.caminho)
            dados_ast['num_passos'] = self.ast.num_passos
            dados_ast['distancia_total'] = self.ast.dist_total
            dados_ast['tempo'] = self.ast.tempo

            con.inserir_dijkstra((dados_dij['ponto_origem'],dados_dij['ponto_destino'],
                                  dados_dij['caminho'],dados_dij['num_passos'],
                                  dados_dij['distancia_total'],dados_dij['tempo'],self.grafo.ident))

            con.inserir_astar((dados_ast['ponto_origem'],dados_ast['ponto_destino'],
                               dados_ast['caminho'],dados_ast['num_passos'],
                               dados_ast['distancia_total'],dados_ast['tempo'],self.grafo.ident))