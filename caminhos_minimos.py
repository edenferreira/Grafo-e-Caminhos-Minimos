__author__ = 'Eden Thiago Ferreira'


class _Caminhos_Minimos:
    def __init__(self, grafo):
        self.grafo = grafo
        self.nao_visitados = set(self.grafo.pontos)
        self.visitados = set()
        self.distancia = {}
        self.distancia_visitados = {}
        self.anterior = {}
        self.num_passos = 0
        self.distancia_prev = {}
        self.distancia_prev_fronteira = {}
        self.ponto_origem = None
        self.ponto_destino = None
        self.executou = False

    def buscar_origem(self):
        self.distancia[self.ponto_origem] = 0
        self.distancia_prev_fronteira[self.ponto_origem] = self.grafo.calc_previsao_peso(self.ponto_origem,
                                                                                         self.ponto_destino)
        return self.ponto_origem

    def atualizar_distancias(self, ponto_alvo, ponto_atual):
        self.distancia_prev_fronteira[ponto_alvo] = self.distancia[ponto_atual] + self.grafo.pesos[
            ponto_atual, ponto_alvo] + self.distancia_prev[ponto_alvo]

    def processar_arestas(self, ponto_atual):
        for ponto_alvo in self.grafo.arestas[ponto_atual]:
            self.distancia_prev[ponto_alvo] = self.grafo.calc_previsao_peso(ponto_alvo, self.ponto_destino)
            if not ponto_alvo in self.visitados:
                if ponto_alvo not in self.distancia or self.distancia[ponto_alvo] > self.distancia[ponto_atual] \
                        + self.grafo.pesos[ponto_atual, ponto_alvo]:
                    self.distancia[ponto_alvo] = self.distancia[ponto_atual] + self.grafo.pesos[ponto_atual, ponto_alvo]
                    self.atualizar_distancias(ponto_alvo, ponto_atual)
                    self.anterior[ponto_alvo] = ponto_atual

    def buscar_proximo_ponto(self):
        ponto_min = float("inf")
        val_min = float("inf")
        for elemento, valor in self.distancia_prev_fronteira.items():
            if valor < val_min:
                val_min = valor
                ponto_min = elemento
        return ponto_min
        #min(self.distancia_prev_fronteira, key=self.distancia_prev_fronteira.get)

    def executar(self):
        ponto_atual = self.buscar_origem()
        while self.nao_visitados:
            self.distancia_prev[ponto_atual] = self.grafo.calc_previsao_peso(ponto_atual, self.ponto_destino)
            self.processar_arestas(ponto_atual)
            self.distancia_visitados[ponto_atual] = self.distancia[ponto_atual]
            del self.distancia[ponto_atual]
            del self.distancia_prev_fronteira[ponto_atual]
            self.visitados.add(ponto_atual)
            self.nao_visitados.remove(ponto_atual)
            if ponto_atual == self.ponto_destino: break
            ponto_atual = self.buscar_proximo_ponto()
            self.num_passos += 1
        self.formatar_caminho()
        self.distancia_total = self.distancia_visitados[self.ponto_destino]
        self.executou = True

    def formatar_caminho(self):
        self.caminho = list()
        ponto_atual = self.ponto_destino
        while True:
            self.caminho.insert(0, ponto_atual)
            if ponto_atual == self.ponto_origem: break
            ponto_atual = self.anterior[ponto_atual]


class A_Star(_Caminhos_Minimos):
    pass


class Dijkstra(_Caminhos_Minimos):
    def atualizar_distancias(self, ponto_alvo, ponto_atual):
        self.distancia_prev_fronteira[ponto_alvo] = self.distancia[ponto_atual] + self.grafo.pesos[
            ponto_atual, ponto_alvo]
