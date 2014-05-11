__author__ = 'Éden Thiago Ferreira'
from coletar_dados import *
from random import uniform, randint

for i in range(10):
    executar_coleta(randint(800,1500),randint(800,1500),uniform(800,1200),uniform(800,1200),uniform(0.04,0.1))