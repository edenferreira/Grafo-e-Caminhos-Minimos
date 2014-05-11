__author__ = 'Éden Thiago Ferreira'
import sqlite3 as sql


class Conexao:
    def __init__(self, nome_banco):
        self.banco = nome_banco

    def __str__(self):
        return self.banco

    def criar_tabela_identificacao(self):
        print("Criando tabela de identificação")
        comando_sql = """create table ident_grafo
                         (id   integer primary key autoincrement,
                          dump integer);"""
        con = sql.connect(self.banco)
        con.execute(comando_sql)
        con.close()
        print("Tabela de identificação criada")

    def criar_tabela_grafos(self):
        print("Criando tabela informacao_grafo")
        comando_sql = """create table informacao_grafo
                         (id          integer   primary key not null,
                          num_pontos  integer   not null,
                          num_arestas integer   not null,
                          max_ponto   float not null);"""
        con = sql.connect(self.banco)
        con.execute(comando_sql)
        con.close()
        print("Tabela informacao_grafo criada")

    def criar_tabela_dijkstra(self):
        print("Criando tabela informacao_dijkstra")
        comando_sql = """create table informacao_dijkstra
                         (ponto_origem  integer          not null,
                          ponto_destino integer          not null,
                          caminho       text             not null,
                          num_passos    integer          not null,
                          distancia_total float          not null,
                          tempo         float            not null,
                          id            integer          not null,
                          primary key(ponto_origem, ponto_destino),
                          foreign key(id) references informacao_grafo(id));"""
        con = sql.connect(self.banco)
        con.execute(comando_sql)
        con.close()
        print("Tabela informacao_dijkstra criada")

    def criar_tabela_astar(self):
        print("Criando tabela informacao_astar")
        comando_sql = """create table informacao_astar
                     (ponto_origem  integer          not null,
                      ponto_destino integer          not null,
                      caminho       text not null,
                      num_passos    integer          not null,
                      distancia_total float   not null,
                      tempo         float        not null,
                      id            integer          not null,
                      primary key(ponto_origem, ponto_destino),
                      foreign key(id) references informacao_grafo(id));"""
        con = sql.connect(self.banco)
        con.execute(comando_sql)
        con.close()
        print("Tabela informacao_astar criada")

    def iniciar_identificacao(self):
        comando_sql = """delete from ident_grafo"""
        con = sql.connect(self.banco)
        con.execute(comando_sql)
        con.commit()
        print("Iniciada tabela de identificação de grafos")
        con.close()

    def inserir_grafo(self, grafo):
        print("Inserindo grafo")
        comando_sql = """insert into informacao_grafo(id,num_pontos,num_arestas,max_ponto)
                     values(?,?,?,?)"""
        con = sql.connect(self.banco)
        con.execute(comando_sql, (grafo.ident, len(grafo), grafo.num_arestas, grafo.max_x))
        con.commit()
        con.close()
        print("Grafo inserido corretamente")

    def inserir_dijkstra(self, dados):
        print("Inserindo dados de dijkstra")
        comando_sql = """insert into informacao_dijkstra(ponto_origem,ponto_destino,caminho,num_passos,distancia_total,tempo,id)
                     values(?,?,?,?,?,?,?)"""
        con = sql.connect(self.banco)
        con.execute(comando_sql, dados)
        con.commit()
        con.close()
        print("Dados de dijkstra inseridos corretamente")

    def inserir_astar(self, dados):
        print("Inserindo dados de astar")
        comando_sql = """insert into informacao_astar(ponto_origem,ponto_destino,caminho,num_passos,distancia_total,tempo,id)
                     values(?,?,?,?,?,?,?)"""
        con = sql.connect(self.banco)
        con.execute(comando_sql, dados)
        con.commit()
        con.close()
        print("Dados de astar inseridos corretamente")

    def get_lista_de_cursor(self, cursor):
        lista = list()
        for elemento in cursor:
            lista.append(elemento)
        return lista

    def get_identificacao(self):
        comando_sql = """insert into ident_grafo(dump) values(0);"""
        con = sql.connect(self.banco)
        con.execute(comando_sql)
        con.commit()
        con.close()

        comando_sql = """select max(id) from ident_grafo;"""
        con = sql.connect(self.banco)
        lista = self.get_lista_de_cursor(con.execute(comando_sql))
        con.close()
        return lista[0][0]

    def get_grafos(self):
        comando_sql = """select *
                           from informacao_grafo;"""
        con = sql.connect(self.banco)
        lista = self.get_lista_de_cursor(con.execute(comando_sql))
        con.close()
        return lista

    def get_dijkstra(self):
        comando_sql = """select *
                           from informacao_dijkstra;"""
        con = sql.connect(self.banco)
        lista = self.get_lista_de_cursor(con.execute(comando_sql))
        con.close()
        return lista

    def get_astar(self):
        comando_sql = """select *
                           from informacao_astar;"""
        con = sql.connect(self.banco)
        lista = self.get_lista_de_cursor(con.execute(comando_sql))
        con.close()
        return lista

    def get_tempos_dijkstra(self):
        comando_sql = """select g.id, g.num_pontos, g.num_arestas, d.ponto_origem, d.ponto_destino, d.num_passos, d.distancia_total, d.tempo
                       from informacao_grafo g,
                            informacao_dijkstra d
                      where g.id = d.id;"""
        dicionario_dados = {}
        dicionario_dados['id'] = list()
        dicionario_dados['num_pontos'] = list()
        dicionario_dados['num_arestas'] = list()
        dicionario_dados['ponto_origem'] = list()
        dicionario_dados['ponto_destino'] = list()
        dicionario_dados['num_passos'] = list()
        dicionario_dados['distancia_total'] = list()
        dicionario_dados['tempo'] = list()
        con = sql.connect(self.banco)
        lista = self.get_lista_de_cursor(con.execute(comando_sql))
        for linha in lista:
            dicionario_dados['id'].append(linha[0])
            dicionario_dados['num_pontos'].append(linha[1])
            dicionario_dados['num_arestas'].append(linha[2])
            dicionario_dados['ponto_origem'].append(linha[3])
            dicionario_dados['ponto_destino'].append(linha[4])
            dicionario_dados['num_passos'].append(linha[5])
            dicionario_dados['distancia_total'].append(linha[6])
            dicionario_dados['tempo'].append(linha[7])
        con.close()
        return dicionario_dados

    def get_tempos_astar(self):
        comando_sql = """select g.id, g.num_pontos, g.num_arestas, a.ponto_origem, a.ponto_destino, a.num_passos, a.distancia_total, a.tempo
                           from informacao_grafo g,
                                informacao_astar a
                          where g.id = a.id;"""
        dicionario_dados = {}
        dicionario_dados['id'] = list()
        dicionario_dados['num_pontos'] = list()
        dicionario_dados['num_arestas'] = list()
        dicionario_dados['ponto_origem'] = list()
        dicionario_dados['ponto_destino'] = list()
        dicionario_dados['num_passos'] = list()
        dicionario_dados['distancia_total'] = list()
        dicionario_dados['tempo'] = list()

        con = sql.connect(self.banco)
        lista = self.get_lista_de_cursor(con.execute(comando_sql))
        for linha in lista:
            dicionario_dados['id'].append(linha[0])
            dicionario_dados['num_pontos'].append(linha[1])
            dicionario_dados['num_arestas'].append(linha[2])
            dicionario_dados['ponto_origem'].append(linha[3])
            dicionario_dados['ponto_destino'].append(linha[4])
            dicionario_dados['num_passos'].append(linha[5])
            dicionario_dados['distancia_total'].append(linha[6])
            dicionario_dados['tempo'].append(linha[7])
        con.close()
        return dicionario_dados

    def get_caminhos_dijkstra(self):
        comando_sql = """select g.id, d.caminho
                           from informacao_grafo g,
                                informacao_dijkstra d
                          where g.id = d.id;"""
        con = sql.connect(self.banco)
        lista = self.get_lista_de_cursor(con.execute(comando_sql))
        con.close()
        return lista

    def get_caminhos_astar(self):
        comando_sql = """select g.id, a.caminho
                           from informacao_grafo g,
                                informacao_astar a
                          where g.id = a.id;"""
        con = sql.connect(self.banco)
        lista = self.get_lista_de_cursor(con.execute(comando_sql))
        con.close()
        return lista