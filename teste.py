from Grafo import *
import heapq
import numpy as np
ordem = 6

custo = [[np.inf, None] for i in range(self.ordem)]
    custo[0] = [0, None] #add o no de origem
    heapq.heapify(custo) #transforma em heap

    no_atual = no_origem
    while custo:
      no_atual = heapq.heappush(custo[0])
      adjacentes = self.get_adjacente(no_atual)