from Grafo import *

#Questão 1 
#enron = Grafo()
#enron = grafo_enron(enron)
#enron.salva_grafo('grafo.txt')
#enron.print_grafo()

enron2 = Grafo()
enron2.carrega_grafo('grafo.txt')

#Questão 2
#a)
enron2.get_ordem()
#b)
enron2.get_tamanho()
#c)
enron2.vertices_isolados()
#d)
#print(enron2.highest_outdegrees(), "\n")
#e)
#print(enron2.highest_indegrees())

print(enron2.dijkstra2("daniel.muschar@enron.com"))
# Questão 3
"""is_euleriano, invalidations = enron2.euleriano()
if is_euleriano:
    print(f"\nO grafo é Euleriano? {is_euleriano}")
else:
    print(f"\nO grafo é Euleriano? {is_euleriano}\nErros: {invalidations}")"""

#Questão 4
"""print(enron2.dijkstra('daniel.muschar@enron.com'))
enron2.lista_distancias(5, "jons@amerexenergy.com")

#Questão 5
print(enron2.diametro())"""

