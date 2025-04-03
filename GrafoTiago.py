from collections import defaultdict

class Grafo:
    def __init__(self):
        self.ordem = 0  # Número de vértices
        self.tamanho = 0  # Número de arestas
        self.master_list = []  # Lista de vértices
        self.lista_adjacente = defaultdict(list)

    def __str__(self):
        return self.imprime_lista_adjacencias()

    def adiciona_vertice(self, u): # adiciona um vértice u (rotulado) ao grafo G.
        if u not in self.master_list:
            self.master_list.append(u)
            self.ordem += 1
        else:
          print(f"Vertice {u} ja foi inserido")

    def adiciona_aresta(self, u, v, peso):# cria uma aresta com peso positivo entre os vértices u e v do grafo G.
        if peso < 0:
            print("Peso não pode ser negativo")
            return

        # Adiciona os vértices u e v, se ainda não existirem
        if u not in self.master_list:
            self.adiciona_vertice(u)
        if v not in self.master_list:
            self.adiciona_vertice(v)

        # Verifica se a aresta já existe, para atualizar
        aresta_existe = False
        for vizinho, p in self.lista_adjacente[u]:
            if vizinho == v:
                self.lista_adjacente[u].remove((v, p))
                aresta_existe = True

        # Adiciona a nova aresta
        self.lista_adjacente[u].append((v, peso))

        if not aresta_existe:
          self.tamanho += 1

    def remove_aresta(self, u, v): # remove a aresta entre os vértices u e v do grafo G.
        if u not in self.master_list or v not in self.master_list:
            print(f"Vértice {u} ou {v} não está no grafo.")
            return

        removido = False
        for vizinho, _ in self.lista_adjacente[u]:
            if vizinho == v:
                self.lista_adjacente[u].remove((v, _))
                self.tamanho -= 1
                removido = True
                return

        if not removido:
            print(f"Aresta ({u}, {v}) não existe no grafo.")

    def remove_vertice(self, u):
        if u not in self.master_list:
            print(f"Vértice {u} não existe no grafo.")
            return

        # Remove todas as arestas que apontam para u
        for vertice in self.master_list:
            self.lista_adjacente[vertice] = [(v, peso) for v, peso in self.lista_adjacente[vertice] if v != u]

        # Remove o vértice u e suas arestas
        del self.lista_adjacente[u]
        self.master_list.remove(u)
        self.ordem -= 1

        # Atualiza o tamanho do grafo
        self.tamanho = sum(len(arestas) for arestas in self.lista_adjacente.values())

    def tem_aresta(self,u, v): # verifica se existe uma aresta entre os vértices u e v do grafo
      aresta_u_v = [vizinho for vizinho,_ in self.lista_adjacente[u] if vizinho == v ]
      return aresta_u_v != []

    def grau_entrada(self, u): # retorna a quantidade total de arestas que chegam até o vértice u do grafo G.
      grau_entrada = 0
      for vertice in self.master_list:
        grau_entrada += len([vizinho for vizinho,_ in self.lista_adjacente[vertice] if vizinho == u])
      return grau_entrada

    def grau_saida(self, u): # retorna a quantidade total de arestas que saem do vértice u do grafo G.
      grau_saida = len(self.lista_adjacente[u])
      return grau_saida

    def grau(self, u): # retorna a quantidade total de arestas conectadas (indegree + outdegree) ao vértice u do grafo G.
      grau = self.grau_entrada(u) + self.grau_saida(u)
      return grau

    def get_peso(self, u, v): # retorna qual é o peso da aresta entre os vértices u e v do grafo G, caso exista uma aresta entre eles.
      for vizinho, peso in self.lista_adjacente[u]:
        if vizinho == v:
          return peso
      return f"Não há arestas entre os vértices {u} e {v}"



    def imprime_lista_adjacencias(self):
      lista = ""
      for vertice in self.master_list:
          arestas = self.lista_adjacente[vertice]
          lista += f"{vertice}: "
          for i, (vizinho, peso) in enumerate(arestas):
              seta = "-> " if i != len(arestas) - 1 else ""
              lista += f"({vizinho}, {peso}) {seta}"
          lista += "\n"
      return lista