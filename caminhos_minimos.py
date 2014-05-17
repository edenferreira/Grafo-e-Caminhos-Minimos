__author__ = 'Eden Thiago Ferreira'


class __CaminhosMinimos:
    """Classe base para caminhos minimos ponto a ponto"""

    def __init__(self, grafo):
        self.grafo = grafo
        self.nao_visit = set(self.grafo.pontos)
        self.visit = set()
        self.dist = {}
        self.dist_visit = {}
        self.anterior = {}
        self.num_passos = 0
        self.dist_prev = {}
        self.dist_prev_front = {}
        self.caminho = list()
        self.dist_total = 0
        self.pt_ori = None
        self.pt_dest = None
        self.executou = False

    def get_origem(self):
        self.dist[self.pt_ori] = 0
        self.dist_prev_front[self.pt_ori] = self.grafo.calc_prev_peso(self.pt_ori,
                                                                      self.pt_dest)
        return self.pt_ori

    def up_dist(self, ponto_alvo, ponto_atual):
        self.dist_prev_front[ponto_alvo] = self.dist[ponto_atual] + self.grafo.pesos[ponto_atual, ponto_alvo] \
                                           + self.dist_prev[ponto_alvo]

    def proc_arestas(self, pt_atual):
        for pt_alvo in self.grafo.arestas[pt_atual]:
            self.dist_prev[pt_alvo] = self.grafo.calc_prev_peso(pt_alvo, self.pt_dest)
            if not pt_alvo in self.visit:
                if pt_alvo not in self.dist or self.dist[pt_alvo] > self.dist[pt_atual] \
                        + self.grafo.pesos[pt_atual, pt_alvo]:
                    self.dist[pt_alvo] = self.dist[pt_atual] + self.grafo.pesos[pt_atual, pt_alvo]
                    self.up_dist(pt_alvo, pt_atual)
                    self.anterior[pt_alvo] = pt_atual

    def get_prox(self):
        ponto_min = float("inf")
        val_min = float("inf")
        for key, valor in self.dist_prev_front.items():
            if valor < val_min:
                val_min = valor
                ponto_min = key
        return ponto_min
        #min(self.distancia_prev_fronteira, key=self.distancia_prev_fronteira.get)

    def start(self):
        pt_atual = self.get_origem()
        while self.nao_visit:
            self.dist_prev[pt_atual] = self.grafo.calc_prev_peso(pt_atual, self.pt_dest)
            self.proc_arestas(pt_atual)
            self.dist_visit[pt_atual] = self.dist[pt_atual]
            del self.dist[pt_atual]
            del self.dist_prev_front[pt_atual]
            self.visit.add(pt_atual)
            self.nao_visit.remove(pt_atual)
            if pt_atual == self.pt_dest:
                break
            pt_atual = self.get_prox()
            self.num_passos += 1
        self.get_caminho()
        self.dist_total = self.dist_visit[self.pt_dest]
        self.executou = True

    def get_caminho(self):
        pt_atual = self.pt_dest
        while True:
            self.caminho.insert(0, pt_atual)
            if pt_atual == self.pt_ori:
                break
            pt_atual = self.anterior[pt_atual]


class AStar(__CaminhosMinimos):
    pass


class Dijkstra(__CaminhosMinimos):
    def up_dist(self, pt_alvo, pt_atual):
        self.dist_prev_front[pt_alvo] = self.dist[pt_atual] + self.grafo.pesos[pt_atual, pt_alvo]
