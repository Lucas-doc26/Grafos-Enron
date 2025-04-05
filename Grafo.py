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
      print("Ordem do grafo:", self.ordem)
      print("Tamanho do grafo:", self.tamanho)


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
      with open(caminho, 'r') as f:
          for linha in f:
              remetente, conteudo = linha.split(":", 1)
              destinatarios = re.findall(r"'(.*?)', (\d+)", conteudo)
              emails = {remetente: [(email, int(numero)) for email, numero in destinatarios]}
              
              if emails[remetente]:
                  for destinatario in emails[remetente]:
                      pessoa, peso = destinatario
                      self.add_aresta(remetente, pessoa, peso)
      self.print_grafo()

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
      adjs = []
      for v in self.corpo[no]:
        adjs.append(v)   
      return adjs

  def get_prox_no(self, adjs, visitados):
    menor = [None, np.inf]
    for adj in adjs:
      if adj[0] not in visitados:
        if adj[1] < menor[1]:
          menor = adj
    if menor[0] != None: 
      return menor[0]
    else:
      return None

  def adj(self, no_origem):
    no = self.get_adjacente(no_origem)
    print(self.get_prox_no(no, [])) 

  def dijkstra(self, no_origem):
    controle = [] #estrutura para controle
    custo = {vertice: [-1, None] for vertice in self.corpo} #dic de cada custo
    visitados = []
    custo[no_origem][0] = 0
    no_atual = no_origem

    while len(visitados) != len(self.corpo):
        try:
            adjacentes = self.get_adjacente(no_atual)
            for adj in adjacentes:
                if adj[0] not in visitados:
                    peso_aresta = self.get_peso(no_atual, adj[0])
                    peso_acumulado = custo[no_atual][0]
                    peso = peso_acumulado + peso_aresta
                    if custo[adj[0]][0] == -1 or custo[adj[0]][0] > peso:
                        custo[adj[0]][0] = peso
                        custo[adj[0]][1] = no_atual

            visitados.append(no_atual)
            controle.append(no_atual)

            no_anterior = no_atual
            no_atual = self.get_prox_no(adjacentes, visitados)

            #caso seja None, tenho que voltar para o meu anterior 
            if no_atual is None:
                controle.remove(no_anterior)
                no_selecionado = None
                #percorrer ao contrário
                for no in reversed(controle):
                    adjs = self.get_adjacente(no)
                    for adj in adjs:
                        
                        #caso os adjs do meu anterior não tenham sido visitados,
                        #vou selecionar eles 
                        if adj[0] not in visitados:
                            no_selecionado = no
                            break #quebrando pq achei oq não foi visitado
                            
                    if no_selecionado is not None:
                        break #quebrando o laço pq achei oq não foi visitado ainda 

                if no_selecionado is not None:
                    no_atual = self.get_prox_no(self.get_adjacente(no_selecionado), visitados)
                    #pego meu adj ao no selecionado
                else:
                    break  # se ele for None até aqui, não tenho mais conexões 
                            # ou seja, não posso ir, ele é desconexo

        except Exception as e:
            print("Erro:", e)
            break

    custo = {chave: valor for chave, valor in custo.items() if valor != [-1, None]}
    #print(custo)
    return custo

  def lista_distancias(self, distancia, no):
    lista = self.dijkstra(no)
    lista = [chave for chave, valor in lista.items() if valor[0] <= distancia]
    print(f'\nOs respectivos vértices estão com uma distância a baixo de {distancia}: {lista}')

  def dfs_iterative(self, source_node):
    visited = []
    stack = []

    stack.append(source_node)

    while len(stack) > 0:
      element = stack.pop()

      if element not in visited:
        print(element)
        visited.append(element)

        for (adj,_) in self.corpo[element]:
          print(adj)
          if adj not in visited:
            stack.append(adj)
    return visited

  def euleriano(self): 
    """
    Valida se o grafo é euleriano. Primeiro valida a se o grau total é par; depois se o grau de entrada e o de saída
      do vertice sao iguais; e por fim, se o grafo eh conexo.

    Returns:
        bool|str: Retora True se o grafo for euleriano, ou retorna as strings de erro,
          informando quais os problemas do grafo.:
          - "O grau total de um vertice nao é par"
          - "Há um ou mais vertices com grau de entrada diferente do de saída"
          - "O grafo nao é conexo"
    """

    invalidations = []
    # mensagem de erro
    degree_is_not_even = "O grau total de um vertice nao é par"
    degree_in_diff_out = "Há um ou mais vertices com grau de entrada diferente do de saída"
    graph_is_weak = "O grafo nao é conexo"

    eulerian_validation = True
    for vertice in self.corpo:
      if not((self.grau(vertice) % 2 == 0)): # grau nao ser par
        eulerian_validation = False
        invalidations.append(degree_is_not_even) if degree_is_not_even not in invalidations else None # texto de erro grau nao ser par
        if not(self.grau_entrada(vertice) == self.grau_saida(vertice)): # grau in != out
          invalidations.append(degree_in_diff_out) if degree_in_diff_out not in invalidations else None #  texto erro in != out


    dfs = self.dfs_iterative(self.vertices[len(self.vertices) -1]) # verifica se o grafo é conexo
    eulerian_validation = sorted(dfs) == sorted(self.vertices)

    invalidations.append(graph_is_weak) if not(eulerian_validation) else None # texto erro de nao convexo

    error_message = ""
    for i, invalidation in enumerate(invalidations):
        error_message += (invalidation + ", " if i < len(invalidations) - 1 else invalidation)

    return eulerian_validation, error_message

    
        
    

  


  