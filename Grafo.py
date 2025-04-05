import re
import numpy as np
from collections import defaultdict

class Grafo:
  def __init__(self):
      self.ordem = 0
      self.tamanho = 0
      self.vertices = []  # Mantém a ordem de inserção
      self.corpo = defaultdict(list)  # Adjacências com defaultdict

  def __str__(self):
    return self.imprime_lista()
    
  def get_ordem(self):
    print(f"A ordem do grafo é: {self.ordem}")
    return self.ordem

  def get_tamanho(self):
    print(f"O tamanho do grafo é: {self.tamanho}")
    return self.tamanho

  def add_vertice(self, nome):
      if nome not in self.vertices:
          self.vertices.append(nome)
          self.ordem += 1
      else:
          raise ValueError("Vértice já existe!")

  def imprime_lista(self):
      lista = ""
      for vertice in self.vertices:
          arestas = self.corpo[vertice]
          lista += f"{vertice}: "
          for i, (vizinho, peso) in enumerate(arestas):
              seta = "-> " if i != len(arestas) - 1 else ""
              lista += f"({vizinho}, {peso}) {seta}"
          lista += "\n"
      return lista

  def add_aresta(self, vertice1, vertice2, peso):
      if peso < 0:
          raise ValueError("Peso inválido!")
      
      # Adiciona vértices se não existirem
      if vertice1 not in self.vertices:
          self.add_vertice(vertice1)
      if vertice2 not in self.vertices:
          self.add_vertice(vertice2)

      # Verifica se aresta existe em qualquer direção
      if self.tem_aresta(vertice1, vertice2):
          # Atualiza peso se existir na direção vertice1->vertice2
          for i in range(len(self.corpo[vertice1])):
              if self.corpo[vertice1][i][0] == vertice2:
                  self.corpo[vertice1][i][1] = peso
                  return
      else:
          self.corpo[vertice1].append([vertice2, peso])
          self.tamanho += 1

  def print_grafo(self):
      for vertice in self.vertices:
          print(vertice, ":", self.corpo[vertice])
      print("Tamanho do grafo:", self.tamanho)
      print("Ordem do grafo:", self.ordem)

  def remove_aresta(self, vertice1, vertice2):
      if vertice1 in self.vertices:
          for i in range(len(self.corpo[vertice1])):
              if self.corpo[vertice1][i][0] == vertice2:
                  self.corpo[vertice1].pop(i)
                  self.tamanho -= 1
                  return

  def remove_vertice(self, vertice):
      if vertice in self.vertices:
          # Remove todas as arestas conectadas
          for v in self.vertices:  # Cópia para iterar com segurança
            if self.tem_aresta(vertice, v):
              self.remove_aresta(vertice, v)
            self.remove_aresta(v, vertice)
          self.vertices.remove(vertice)
          del self.corpo[vertice]
          self.ordem -= 1
      else:
          raise ValueError("Vértice não existe!")

  def tem_aresta(self, vertice1, vertice2):
      if vertice1 in self.vertices and vertice2 in self.vertices:
        for vizinho, _ in self.corpo[vertice1]:
          if vizinho == vertice2:
              return True
        for vizinho, _ in self.corpo[vertice2]:
            if vizinho == vertice1:
                return True
        return False  
      raise ValueError("Vértice não existe!")

  def grau_entrada(self, vertice):
    grau_entrada = 0
    if vertice in self.vertices:
      for v in self.vertices:
        grau_entrada += len([vizinho for vizinho,_ in self.corpo[v] if vizinho == vertice])
      return grau_entrada
    else:
      raise ValueError("Vértice não existe")
    
  def grau_saida(self, vertice):
      if vertice not in self.vertices:
          raise ValueError("Vértice não existe")
      return len(self.corpo[vertice])

  def grau(self, vertice):
      return self.grau_entrada(vertice) + self.grau_saida(vertice)

  def get_peso(self, vertice1, vertice2):      
      if vertice1 not in self.vertices:
          raise ValueError("Vértice não existe")
      for vizinho, peso in self.corpo[vertice1]:
          if vizinho == vertice2:
              return peso
      return None

  def salva_grafo(self, caminho):
      with open(caminho,'w') as f:
          for vertice in self.vertices:
              adjacentes = self.corpo[vertice]
              if adjacentes:
                  dados_formatados = [f"{aresta} ->" for aresta in adjacentes]
                  f.write(f"{vertice}:{dados_formatados}\n")
              else:
                  f.write(f"{vertice}:\n")
          print("Grafo salvo com sucesso!")

  def carrega_grafo(self, caminho):
      i = 0
      with open(caminho, 'r') as f:
          for linha in f:
            remetente, conteudo = linha.split(":", 1) 
            destinatarios = re.findall(r"'(.*?)', (\d+)", conteudo)

            emails = {remetente: [(email, int(numero)) for email, numero in destinatarios]}
            if emails[remetente]:
                for destinatario in emails[remetente]:
                  pessoa, peso = destinatario
                  self.add_aresta(remetente, pessoa, peso)
            else:
                #se só tiver grau de entrada, eu tenho que add o vertice 
                try:
                  if remetente not in self.corpo.keys:
                    self.add_vertice(remetente)
                except:
                  pass
            i += 1
      print(i)

  def vertices_isolados(self):
      isolados = [v for v in self.vertices if self.grau(v) == 0]
      print(f"Os vértices isolados são: {isolados}")

  # Demais métodos mantidos com lógica similar...

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

    # def euleriano(self): 
    #   vertices_eulerianos = []
    #   for vertice in self.corpo:
    #     if (self.grau(vertice) % 2 == 0) and (self.grau_entrada(vertice) == self.grau_saida(vertice)):
    #       if vertice not in vertices_eulerianos:
    #         vertices_eulerianos.append(vertice)
    #     else: 
    #       return False
    #   for vertice in vertices_eulerianos:
    #     for i in range(self.grau_saida(vertice)):
    #       last_vertice = vertice
    #       current_vertice = 0 
    #       while current_vertice != vertice:
    #         for i in range(self.gra)
    #         current_vertice = self.corpo[last_vertice][current_vertice][]
    #   print(f"Os grafos eulerianos são: {vertices_eulerianos}")

  


  