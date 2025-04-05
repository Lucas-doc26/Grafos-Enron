import os
from Grafo import *
from email.parser import Parser
from email.policy import default

def grafo_enron(graph):
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
            remetente = remetente.strip() #remove os espaços em branco: "  lucas@pucpr.edu.br " -> "lucas@pucpr.edu.br"
            destinarios = headers["To"] or headers["to"]
            if destinarios != None:
                # caso o email seja para mais de uma pessoa, ele vai me retornar a lista
                pessoas = destinarios.split(',')
                if remetente != None:
                    for destinario in pessoas:
                        destinario = destinario.strip()
                        #caso já possua uma aresta, ele vai mudar o peso, pegando o peso antigo e add mais um
                        #try/except pq gera uma exceção caso naõ exista as duas arestas 
                        try:
                            if graph.tem_aresta(remetente, destinario):
                                graph.add_aresta(remetente, destinario, (graph.get_peso(remetente, destinario) + 1 ))
                        except:
                            graph.add_aresta(remetente, destinario, 1 )
        
        del email_dir, f 

    return graph

#Questão 1 
enron = Grafo()
enron.carrega_grafo('grafo-euleriano.txt')
enron.print_grafo()

print(enron.ordem, 
enron.tamanho)

# print("------------------------------")
# print(enron)
# print(enron.euleriano())


# print(enron.get_adjacente('carlos.giron@psiusa.com'))
# print(enron.get_prox_no('carlos.giron@psiusa.com'))
# enron.dijkstra('carlos.giron@psiusa.com', 'mike.kotar@psiusa.com')