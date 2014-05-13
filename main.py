__author__ = 'Eden Thiago Ferreira'
from coletar_dados import *
from random import uniform, randint

for i in range(10):
    executar_coleta(randint(1200,1600),randint(1200,1600),uniform(800,1200),uniform(800,1200),uniform(0.04,0.1))