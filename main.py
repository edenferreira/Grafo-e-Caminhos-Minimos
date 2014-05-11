__author__ = 'Éden Thiago Ferreira'
import cProfile as cp
import pstats as pst
from collections import OrderedDict
from grafos import *
from banco_dados import *
from caminhos_minimos import *

def extrair_tempo(profiler):
    with open('status.txt','w') as arq:
        dados_crus = pst.Stats(profiler,stream=arq)
        dados_crus.strip_dirs().print_stats('(executar)')

    status = list()
    with open('status.txt','r') as arq:
        for linha in arq:
            if 'executar' in linha:
                status.append(linha.split())

    return status[1][4]

dados_grafo = OrderedDict()
dados_dij = OrderedDict()
dados_ast = OrderedDict()

conexao = Conexao('grafos_db')
grafo = Grafo(conexao.get_identificacao())
grafo.gerar_grafo_cidade(rnd.randint(1000,1500),rnd.randint(1000,1500),rnd.randint(800,1200),rnd.randint(800,1200),rnd.uniform(0.04,0.1))
dados_grafo['id'] = grafo.ident
dados_grafo['num_pontos'] = len(grafo)
dados_grafo['num_arestas'] = grafo.num_arestas
dados_grafo['max_pontos'] = sqrt(((grafo.max_x)**2) + ((grafo.max_y)**2))
conexao.inserir_grafo(grafo)

origem, destino = rnd.sample(grafo.pontos,2)
dados_dij['ponto_origem'] = origem
dados_dij['ponto_destino'] = destino
dados_ast['ponto_origem'] = origem
dados_ast['ponto_destino'] = destino

dij = Dijkstra(grafo)
dij.ponto_origem = origem
dij.ponto_destino = destino
ast = A_Star(grafo)
ast.ponto_origem = origem
ast.ponto_destino = destino

prof = cp.Profile(time_unit=.0001)
prof.enable()
dij.executar()
prof.disable()

dados_dij['caminho'] = str(dij.caminho)
dados_dij['num_passos'] = dij.num_passos
dados_dij['distancia_total'] = dij.distancia_total
dados_dij['tempo'] = extrair_tempo(prof)
dados_dij['id'] = dij.grafo.ident
del prof

prof = cp.Profile(time_unit=.0001)
prof.enable()
ast.executar()
prof.disable()

dados_ast['caminho'] = str(ast.caminho)
dados_ast['num_passos'] = ast.num_passos
dados_ast['distancia_total'] = ast.distancia_total
dados_ast['tempo'] = extrair_tempo(prof)
dados_ast['id'] = ast.grafo.ident
del prof

conexao.inserir_dijkstra((dados_dij['ponto_origem'],dados_dij['ponto_destino'],
                                 dados_dij['caminho'],dados_dij['num_passos'],
                                 dados_dij['distancia_total'],dados_dij['tempo'],grafo.ident))
conexao.inserir_astar((dados_ast['ponto_origem'],dados_ast['ponto_destino'],
                              dados_ast['caminho'],dados_ast['num_passos'],
                              dados_ast['distancia_total'],dados_ast['tempo'],grafo.ident))

with open('D:/Dropbox/Trabalho de Conclusão de Curso/Grafos e Caminhos Minimos/resultado_teste.txt','a') as arq:
    print('dados_grafo: ',end=' ',file=arq)
    for elemento,value in dados_grafo.items():
        print(elemento,':',value,file=arq)
    print('dados_dij: ',end=' ',file=arq)
    for elemento,value in dados_dij.items():
        print(elemento,':',value,file=arq)
    print('dados_ast: ',end=' ',file=arq)
    for elemento,value in dados_ast.items():
        print(elemento,':',value,file=arq)
