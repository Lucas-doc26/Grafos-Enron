import os
from Grafo import *
from email.parser import Parser
from email.policy import default

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

def grafo_enron(grafo):
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

                        destinario = formata(destinario)
                        remetente = formata(remetente)
                        #caso já possua uma aresta, ele vai mudar o peso, pegando o peso antigo e add mais um
                        #try/except pq gera uma exceção caso naõ exista as duas arestas 
                        try:
                            if grafo.tem_aresta(remetente, destinario):
                                grafo.add_aresta(remetente, destinario, (grafo.get_peso(remetente, destinario) + 1 ))
                        except:
                            grafo.add_aresta(remetente, destinario, 1 )
        
        del email_dir, f 

    return grafo

#Questão 1 
enron = Grafo()
enron = grafo_enron(enron)
enron.salva_grafo('grafo.txt')
enron.print_grafo()

enron2 = Grafo()
enron2.carrega_grafo('grafo.txt')

#Questão 2
#a)
enron2.get_ordem()
#b)
enron2.get_tamanho()


#Questão 3


#Questão 4
enron2.lista_distancias(5, "jons@amerexenergy.com")
