import re
import numpy as np
from collections import defaultdict
import os
from email.parser import Parser
from email.policy import default
import heapq

class Grafo:
  def __init__(self):
      self.ordem = 0
      self.tamanho = 0
      self.vertices = []  # Mantém a ordem de inserção
      self.corpo = defaultdict(list)  # Adjacências com defaultdict

  def __str__(self):
    return self.imprime_lista()
    
  def get_ordem(self):
    print(f"\nA ordem do grafo é: {self.ordem}")
    return self.ordem

  def get_tamanho(self):
    print(f"\nO tamanho do grafo é: {self.tamanho}")
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
      #print("Ordem do grafo:", self.ordem)
      #print("Tamanho do grafo:", self.tamanho)

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
      else:
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
                  #formata os dados, e escreve no arquivo
                  dados_formatados = [f"{aresta} ->" for aresta in adjacentes]
                  f.write(f"{vertice}:{dados_formatados}\n")
              else:
                  f.write(f"{vertice}:\n")
          print("Grafo salvo com sucesso!")

  def carrega_grafo(self, caminho):
      with open(caminho, 'r') as f:
          for linha in f:
              #lendo cada linha do arquivo e pegando o remetente e os destinatarios
              remetente, conteudo = linha.split(":", 1)#spli assim por conta de joao: [[''],['']]
              destinatarios = re.findall(r"'(.*?)', (\d+)", conteudo) #separando por qualquer coisa entre '' e um decimal
              emails = {remetente: [(email, int(numero)) for email, numero in destinatarios]} #formatando em dic 
              
              if emails[remetente]:
                  for destinatario in emails[remetente]:
                      pessoa, peso = destinatario
                      self.add_aresta(remetente, pessoa, peso)
      self.print_grafo()

  def vertices_isolados(self):
    isolados = [v for v in self.vertices if self.grau(v) == 0]
    print(f"\n{len(isolados)} vértices isolados: {isolados}")

  def highest_outdegrees(self):
    """
    Pega os 20 maiores graus de saída 
    """
    rank = []
    for node in self.vertices:
        grau = self.grau_saida(node)
        rank.append([grau, node])

    rank.sort(reverse=True)
    return rank[:20]

  def highest_indegrees(self):
    """
    Pega os 20 maiores graus de entrada
    """
    rank = []
    for node in self.vertices:
        grau = self.grau_entrada(node)
        rank.append([grau, node])

    rank.sort(reverse=True)
    return rank[:20]

  def return_no(self, nome):
    return self.corpo[nome]

  def get_adjacente(self, no):
    """
    Retorna uma lista de adjacentes 
    """
    if no not in self.corpo:
      raise ValueError("Esse nó não existe!")
    else:
      adjs = []
      for v in self.corpo[no]:
        adjs.append(v)   
      return adjs

  def dijkstra(self, no_origem):
    #crio um dic com a estrutura: Vertice - Peso Acumulado, Antecessor
    distancia = {vertice: [np.inf, None] for vertice in self.corpo}
    distancia[no_origem][0] = 0 
    custo = [(0, no_origem)] #add o nó de origem ao custo
    
    #enquanto minha lista de custos não for 0, continua 
    while custo:
      peso_acumulado, no_atual = heapq.heappop(custo)
      #pego os vertíces adjs ao no atual
      adjacentes = self.get_adjacente(no_atual)
      for vertice, peso_aresta in adjacentes:
          peso = peso_acumulado + peso_aresta
          if peso < distancia[vertice][0]:
            distancia[vertice] = peso, no_atual
            heapq.heappush(custo, (peso, vertice)) #add tds os vertice adjs e seu peso a lista de custos
    
    #retiro da lista de distancias os vértices valores são inf
    nos_nao_alcancados = [v for v in distancia if distancia[v][0] == np.inf]
    for v in nos_nao_alcancados:
      distancia.pop(v)

    return distancia
  
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
        visited.append(element)

        for (adj,_) in self.corpo[element]:
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
    degree_in_diff_out = "Há um ou mais vertices com grau de entrada diferente do de saída"
    graph_is_weak = "O grafo nao é conexo"

    eulerian_validation = True
    for vertice in self.corpo:
      if not(self.grau_entrada(vertice) == self.grau_saida(vertice)): # grau in != out
        invalidations.append(degree_in_diff_out) if degree_in_diff_out not in invalidations else None #  texto erro in != out


    dfs = self.dfs_iterative(self.vertices[len(self.vertices) -1]) # verifica se o grafo é conexo
    eulerian_validation = sorted(dfs) == sorted(self.vertices)

    invalidations.append(graph_is_weak) if not(eulerian_validation) else None # texto erro de nao convexo

    error_message = ""
    for i, invalidation in enumerate(invalidations): # enumerate para pegar index no i
        error_message += (invalidation + ", " if i < len(invalidations) - 1 else invalidation)

    return eulerian_validation, error_message
  
  def diametro(self):
        maiores_custos = []
        for node in self.vertices:
            lista = self.dijkstra(node)
            chave_maxima, valor_maximo = max(lista.items(), key=lambda item: item[1][0])

            caminho_maximo = [chave_maxima]
            no_atual = chave_maxima
            while no_atual != node:
                predecessor = lista[no_atual][1]
                if predecessor is None:
                    break
                caminho_maximo.append(predecessor)
                no_atual = predecessor

            caminho_maximo.reverse()
            maiores_custos.append([valor_maximo[0], caminho_maximo])

        return max(maiores_custos, key=lambda item: item[0])

def grafo_enron(grafo):
    """
    Retorna o grafo do Enron
    """
    base_path = 'Amostra Enron - 2016'

    emails_dir = []
    for dir in os.listdir(base_path):
        sub_dir = os.path.join(base_path, dir) #'Amostra Enron - 2016/cuilla-m'

        if os.path.isdir(sub_dir):
            for dir_emails in os.listdir(sub_dir):
                emails = os.path.join(sub_dir, dir_emails) #'Amostra Enron - 2016/cuilla-m/10-fantasay'

                for email in os.listdir(emails):
                    email_path = os.path.join(emails, email)  # caminho do email
                    
                    if os.path.isdir(email_path):  # pode ter outras pastas dentro
                        for m in os.listdir(email_path):
                            dir_email = os.path.join(email_path, m)  
                            emails_dir.append(dir_email)
                    else:
                        emails_dir.append(email_path)

    for email_dir in emails_dir:
        with open(email_dir, "r", encoding="cp1252") as f:
            conteudo_email = f.read()
            headers = Parser(policy=default).parsestr(conteudo_email)
            remetente = headers["From"] or headers["from"]
            destinarios = headers["To"] or headers["to"]
            if destinarios != None:
                # caso o email seja para mais de uma pessoa, ele vai me retornar a lista
                if ',' in destinarios:
                  pessoas = destinarios.split(',')
                else:
                  pessoas = [destinarios] #coloca somente uma pessoa na lista
                if remetente != None:
                    remetente = remetente.strip() #remove os espaços em branco: "  joao@pucpr.edu.br " -> "joao@pucpr.edu.br"

                    for destinario in pessoas:
                        destinario = destinario.strip()

                        destinario = formata(destinario)
                        remetente = formata(remetente)
                        #caso já possua uma aresta, ele vai mudar o peso, pegando o peso antigo e add mais um
                        #try/except pq gera uma exceção caso naõ exista as duas arestas 
                        try:
                            if grafo.tem_aresta(remetente, destinario):
                                grafo.add_aresta(remetente, destinario, (grafo.get_peso(remetente, destinario) + 1 ))
                            else:
                                # pode ser que o r/d existam mas não tenham aresta
                                grafo.add_aresta(remetente, destinario, 1 )
                        except:
                            grafo.add_aresta(remetente, destinario, 1 )
            

        
        del email_dir, f 
    return grafo

def formata(string):
    """
    Está formatando os emails que estavam com caracteres inválidos
    """
    string = string.replace(" ", "")
    if 'e-mail' or 'email' in string:
        string = string.replace("e-mail", '')
    if '<' or '>':
        string = string.replace(">", '')
        string = string.replace("<", '')
    if string.startswith("."):
        string = string[1:]
        #tirando o . 
    if "'" in string:
        string = string.replace("'", '')
    return string

  