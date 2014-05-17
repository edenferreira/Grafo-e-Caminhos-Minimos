__author__ = 'Eden Thiago Ferreira'
from coletar_dados import *
from banco_dados import *

for i in range(10000):
    grafo = Grafo(Conexao('grafos_db').get_identificacao())
    col = Coletor(grafo)
    col.start()
    col.dump_dados(Conexao('grafos_db'))
