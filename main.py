from Grafo import *

#Questão 1 
#enron = Grafo()
#enron = grafo_enron(enron)
#enron.salva_grafo('grafo.txt')
#enron.print_grafo()

enron2 = Grafo()
enron2 = grafo_enron(enron2)
enron2.salva_grafo('grafo.txt')
enron2.carrega_grafo('grafo.txt')

#Questão 2
#a)
enron2.get_ordem()
#b)
enron2.get_tamanho()
#c)
enron2.vertices_isolados()
#d)
print(f"\nOs seguintes vértices possuem os maiores graus de saída: {enron2.highest_outdegrees()}")
#e)
print(f"\nOs seguintes vértices possuem os maiores graus de entrada: {enron2.highest_indegrees()}")

# Questão 3
is_euleriano, invalidations = enron2.euleriano()
if is_euleriano:
    print(f"\nO grafo é Euleriano? {is_euleriano}")
else:
    print(f"\nO grafo é Euleriano? {is_euleriano}\nErros: {invalidations}")

#Questão 4
enron2.lista_distancias(5, "jared.kaiser@enron.com")

#Questão 5
print(f"\nO diametro do grafo é: {enron2.diametro()}")

