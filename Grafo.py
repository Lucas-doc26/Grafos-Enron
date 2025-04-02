import re
import numpy as np

class Grafo:
  def __init__(self):
      self.ordem = 0
      self.tamanho = 0
      self.corpo = {}

  def get_ordem(self):
    print(f"A ordem do grafo é: {self.ordem}")
    return self.ordem
  
  def get_tamanho(self):
    print(f"O tamanho do grafo é: {self.tamanho}")
    return self.tamanho

  def add_vertice(self, nome):
      if nome not in self.corpo:
          self.corpo[nome] = []
          self.ordem += 1
      else:
          raise ValueError("Vértice já existe!")

  def imprime_lista(self):
    for vertice in self.corpo:
      dados = []
      if len(self.corpo[vertice]) > 0:
        for i in range(len(self.corpo[vertice])):
            dados.append(self.corpo[vertice][i])
            dados_formatados = [f'{d} ->' for d in dados]
        print(f'{vertice}:{dados_formatados}')
      else:
        print(vertice, ':')

  def add_aresta(self,vertice1, vertice2, peso):
    if peso < 0:
      raise ValueError("Peso inválido!")
    else:
      if vertice1 not in self.corpo:
            self.add_vertice(vertice1)
      if vertice2 not in self.corpo:
        self.add_vertice(vertice2)

      if self.tem_aresta(vertice1, vertice2):
        #print("Aresta já existe! Peso será mudado")
        for i in range(len(self.corpo[vertice1])):
          if self.corpo[vertice1][i][0] == vertice2:
            self.corpo[vertice1][i][1] = peso
            return

      if not self.tem_aresta(vertice1, vertice2):
        self.corpo[vertice1].append([vertice2, peso])
        self.tamanho += 1

  def print_grafo(self):
      for vertice in self.corpo:
          print(vertice, ":", self.corpo[vertice])
      print("Tamanho do grafo:", self.tamanho)
      print("Ordem do grafo:", self.ordem)

  def remove_aresta(self, vertice1, vertice2):
    if vertice1 in self.corpo:
      for i in range(len(self.corpo[vertice1])):
        if self.corpo[vertice1][i][0] == vertice2:
          self.corpo[vertice1].pop(i)
          self.tamanho -= 1
          break

  def remove_vertice(self, vertice):
    if vertice in self.corpo:
      for v in self.corpo:
        if self.tem_aresta(vertice, v):
          self.remove_aresta(vertice, v)
        self.remove_aresta(v, vertice)
      self.corpo.pop(vertice)
      self.ordem -= 1
    else:
      raise ValueError("Vértice não existe!")

  def tem_aresta(self, vertice1, vertice2):
    if vertice1 in self.corpo and vertice2 in self.corpo:
        for vizinho, _ in self.corpo[vertice1]:
            if vizinho == vertice2:
                return True
        for vizinho, _ in self.corpo[vertice2]:
            if vizinho == vertice1:
                return True
        return False  
    else:
        raise ValueError("Pelo menos um desses vértices não existe!")

  def grau_entrada(self, vertice):
    grau_entrada = 0
    if vertice in self.corpo:
      for v in self.corpo:
        if len(self.corpo[v]) > 0:
          for i in range(len(self.corpo[v])):
            if self.corpo[v][i][0] == vertice:
              grau_entrada += 1
      return grau_entrada
    else:
      raise ValueError("Vértice não existe")

  def grau_saida(self, vertice):
    if vertice in self.corpo:
      return len(self.corpo[vertice])
    else:
      raise ValueError("Vértice não existe")

  def grau(self, vertice):
    return self.grau_entrada(vertice) + self.grau_saida(vertice)

  def get_peso(self, vertice1, vertice2):
    if vertice1 in self.corpo:
     for i in range(len(self.corpo[vertice1])):
        if len(self.corpo[vertice1]) > 0:
           if self.corpo[vertice1][i][0] == vertice2:
            return self.corpo[vertice1][i][1]
    else:
      raise ValueError("Vértice não existe")
           
  def salva_grafo(self, caminho):
    with open(caminho,'w') as f:
      for vertice in self.corpo:
        dados = []
        if len(self.corpo[vertice]) > 0:
          for i in range(len(self.corpo[vertice])):
              dados.append(self.corpo[vertice][i])
              dados_formatados = [f'{d} ->' for d in dados]
          f.write(f'{vertice}:{dados_formatados}\n')
        else:
          f.write(f'{vertice}:\n')
      print("Grafo salvo com sucesso!")

  def carrega_grafo(self, caminho):
     with open(caminho, 'r') as f:
        for linha in f:
          remetente, conteudo = linha.split(":", 1)  

          # '(.*?)' -> pega qualquer coisa entre '' 
          # (\d+) -> pega qualquer número decimal
          destinatarios = re.findall(r"'(.*?)', (\d+)", conteudo)

          #faço um list comprehension para criar um dic com a estrutura: Remetente: [pessoa, peso], [pessoa, peso] , ...
          emails = {remetente: [(email, int(numero)) for email, numero in destinatarios]}

          #caso o remetente não esteja vazio, vou percorer a lista de pessoas e ir add
          if emails[remetente]:
            for destinatario in emails[remetente]:
              pessoa, peso = destinatario
              self.add_aresta(remetente, pessoa, peso)
          else:
            try:
              #add os vertíces que não tinham conexões saindo dele
              self.add_vertice(remetente)
            except:
               pass
            
  def vertices_isolados(self):
    isolados = []
    for vertice in self.corpo:
      if self.grau(vertice) == 0:
        isolados.append(vertice)
    
    print(f"Os grafos isolados são: {isolados}")

  #Implemente um método que retorne uma lista com todos os vértices que
  #estão localizados até uma distância D de um vértice N, em que D é a soma dos
  #pesos ao longo do caminho mais curto entre dois vértices. A implementação deve
  #ser eficiente o suficiente para lidar com grafos com milhares de vértices e arestas
  #sem exceder limites razoáveis de tempo e memória.

  def return_no(self, nome):
    return self.corpo[nome]

  def get_adjacente(self, no):
    if no not in self.corpo:
      raise ValueError("Esse nó não existe!")
    else:
      return self.corpo[no]

  def get_prox_no(self, no):
    adjacentes = self.get_adjacente(no)
    menor = [None, 0]
    for adj in adjacentes:
      if adj[1] > menor[1]:
        menor = adj
    return menor

  def dijkstra(self, no_origem, no_destino):
    visitados = []
    custo = [([np.inf, None], [np.inf, None]) for i in range(self.ordem)] #crio uma lista de custos, 
    custo[0] = no_origem, 0
    custo.index(no_origem)
    no_atual = no_origem
    while no_destino not in visitados:
      adjcentes = self.get_adjacente(no_atual)
      for adj in adjcentes:
        if adj not in visitados:
          custo[adj]
      visitados.append(no_atual)
      no_atual = self.get_prox_no(no_atual)
    print(custo)

  def teste(self, distancia, vertice):
    pass


  