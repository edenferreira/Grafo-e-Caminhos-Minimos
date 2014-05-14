__author__ = 'Éden Thiago Ferreira'
from banco_dados import *

conexao = Conexao('grafos_db')
conexao.criar_tabela_identificacao()
conexao.criar_tabela_grafos()
conexao.criar_tabela_grafos_mapa()
conexao.criar_tabela_dijkstra()
conexao.criar_tabela_astar()