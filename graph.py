class No_vertice(object):
    def __init__(self, dado_vertice, no_anterior=None, proximo_no=None,
                 primeira_aresta_sai_deste_no=None, primeira_aresta_que_chega_noNo=None,
                 ultima_aresta_que_sai=None, ultima_aresta_que_chega=None):
        self.vertice = dado_vertice
        self.no_anterior = no_anterior
        self.proximo_no = proximo_no
        self.primeira_aresta_sai_deste_no = primeira_aresta_sai_deste_no
        self.primeira_aresta_que_chega_noNo = primeira_aresta_que_chega_noNo
        self.ultima_aresta_que_sai = ultima_aresta_que_sai
        self.ultima_aresta_que_chega = ultima_aresta_que_chega

class No_aresta(object):
    def __init__(self, no_inicial, no_final, dado_aresta,
                 aresta_anterior_mesmo_no_inicial=None,
                 aresta_posterior_mesmo_no_inicial=None,
                 aresta_anterior_mesmo_no_final=None,
                 aresta_posterior_mesmo_no_final=None):
        self.aresta = dado_aresta
        self.no_inicial_da_aresta = no_inicial
        self.no_final_da_aresta = no_final
        # lista da arestas que partem do inicial
        self.aresta_anterior_mesmo_no_inicial  = aresta_anterior_mesmo_no_inicial
        self.aresta_posterior_mesmo_no_inicial = aresta_posterior_mesmo_no_inicial
        # lista das arestas que chegam no no final
        self.aresta_anterior_mesmo_no_final  = aresta_anterior_mesmo_no_final
        self.aresta_posterior_mesmo_no_final = aresta_posterior_mesmo_no_final


class Graph(object):
    no_first = None #primeiro no do grafo
    no_last = None #ultimo no do grafo
    #variaveis para a funcao busca em profundidade
    valor_profundidade_entrada = 0 # contador da profundidade em que os vertices entram da pilha 
    valor_profundidade_saida = 0 # contador da profundidade em que os vertices saem da pilha
    profundidades_entrada_saida = {}
    pai = {} # dicionario com os pais de cada vertice
    niveis = {} # nivel de cada vertice 
     # é vertice mais proximo da raiz da arvore de busca em profundidade que consigo chegar descendo pelas aresta da arvore quantas vezes eu queira (incluindo 0 vezes) e subindo uma unica vez por uma aresta de retorno
    vertice_mais_prox_da_raiz = {}
    demarcadores = set() # um demarcador eh um vertice que tem como (vertice_mais_prox_da_raiz) seu pai ou ele mesmo
    dic = set()  # articulacao é um vertice que se for removido, torna as aresta desconexa


    #adiciona uma nova aresta no grafo
    def adiciona_vertice(self, dado):
        novo_vertice = No_vertice(dado)  # cria um novo no apontando para None
        # se a no_first e no_last eh None, o grafo nao tem nenhum vertice, grafo vazio
        if (self.no_first is None):
            self.no_first = novo_vertice
            self.no_last = novo_vertice
        else:#se o grafo ja tiver vertice
            novo_vertice.no_anterior = self.no_last
            self.no_last.proximo_no = novo_vertice
            self.no_last = novo_vertice
            # novo_vertice.proximo_no  = None #ja tem none no começo
        return novo_vertice

    #adiciona a aresta, no inicial e fina faz a conexao de um vertice com outro
    def adiciona_aresta(self, no_inicial, no_final, dado):
        nova_aresta = No_aresta(no_inicial, no_final, dado)
        # se ja houver alguma aresta saindo do no inical
        if (no_inicial.ultima_aresta_que_sai is not None):
            nova_aresta.aresta_anterior_mesmo_no_inicial = no_inicial.ultima_aresta_que_sai
            no_inicial.ultima_aresta_que_sai.aresta_posterior_mesmo_no_inicial = nova_aresta
            no_inicial.ultima_aresta_que_sai = nova_aresta
        # se ja houver alguma aresta chegando no no final
        if(no_final.ultima_aresta_que_chega is not None):
            no_final.ultima_aresta_que_chega.aresta_posterior_mesmo_no_final = nova_aresta
            no_final.ultima_aresta_que_chega.aresta_anterior_mesmo_no_final = no_final.ultima_aresta_que_chega
            no_final.ultima_aresta_que_chega = nova_aresta
        # se não tiver nenhuma aresta no no inicial
        if (no_inicial.primeira_aresta_sai_deste_no is None):
            no_inicial.primeira_aresta_sai_deste_no = nova_aresta
            no_inicial.ultima_aresta_que_sai = nova_aresta
        # se nao houver alguma aresta no no final
        if (no_final.primeira_aresta_que_chega_noNo is None):
            no_final.primeira_aresta_que_chega_noNo = nova_aresta
            no_final.ultima_aresta_que_chega = nova_aresta

    #colocando em um dicionario os vertice e as arestas para busca em largura e profudidade
    def dicionario(self):
        no_atual = self.no_first
        myDict = {}#criando o dicionario que ira receber os vertices e arestas 
        # Para cada no valido da lista
        while (no_atual is not None):
            myDict[no_atual.vertice] = [] #inseri os vertices, qe seram as chaves
            aresta_atual  = no_atual.primeira_aresta_sai_deste_no#atualiza a primeira aresta do vertice atual
            aresta_atual2 = no_atual.ultima_aresta_que_sai#atualiza a ultima aresta do vertice atual
            myDict[no_atual.vertice].append(aresta_atual.no_final_da_aresta.vertice)#inseri a primeira aresta
            while (aresta_atual.aresta != aresta_atual2.aresta):#enquanto no chega na ultima aresta
                aresta_atual = aresta_atual.aresta_posterior_mesmo_no_inicial #atualiza a arestas
                myDict[no_atual.vertice].append(aresta_atual.no_final_da_aresta.vertice)#inseri as arestas
            no_atual = no_atual.proximo_no#atualiza o vertice
        return(myDict)

    #funcao que imprimi a matriz   
    def imprimir(self):
        no_atual = self.no_first
        print("\n -------------------------Matriz esparsa---------------------------\n\n")     
        # Para cada no valido da lista
        while (no_atual is not None):
            print("\nVertice ",no_atual.vertice)
            if(no_atual.vertice == self.no_first.vertice):
                print("Vertice Anterior a ",no_atual.vertice,":",None)
            else:
                print("Vertice Anterior a ",no_atual.vertice,":",no_atual.no_anterior.vertice)
            if(no_atual.vertice == self.no_last.vertice):
                print("Vertice posterior a",no_atual.vertice,":",None)
            else:
                print("Vertice posterior a",no_atual.vertice,":",no_atual.proximo_no.vertice)
            aresta_atual = no_atual.primeira_aresta_sai_deste_no
            aresta_atual2 = no_atual.ultima_aresta_que_sai
            print("primeira aresta que sai do vertice",no_atual.vertice,":", aresta_atual.aresta)
            print("ultima aresta que sai  do vertice ",no_atual.vertice,":", aresta_atual2.aresta)
            print("Vertice inicial                  :", aresta_atual.no_inicial_da_aresta.vertice, " Vertice final                   :", aresta_atual.no_final_da_aresta.vertice)
            while(aresta_atual.aresta != aresta_atual2.aresta):
                aresta_atual = aresta_atual.aresta_posterior_mesmo_no_inicial            
                print("aresta_posterior_mesmo_no_inicial:", aresta_atual.aresta, " aresta_anterior_mesmo_no_inicial:",aresta_atual.aresta_anterior_mesmo_no_inicial.aresta)            
                #print("aresta_posterior_mesmo_no_final:", aresta_atual.aresta_anterior_mesmo_no_final.aresta, " aresta_anterior_mesmo_no_final:",aresta_atual.aresta_posterior_mesmo_no_final.aresta_anterior_mesmo_no_inicial.aresta)
                print("Vertice inicial                  :", aresta_atual.no_inicial_da_aresta.vertice ," Vertice final                   :",aresta_atual.no_final_da_aresta.vertice )                                                                                         
            no_atual = no_atual.proximo_no

    def busca_em_largura(self,dicionario, vertice_do_grafo):
        fila = [] # fila da busca 
        #.append(elemento) -> adiciona elemento na fila ; .pop(0) -> proximo na fila
        ordem_de_visita = {}
        l = 1 # contador de ordem_de_visita dos vertices
        pai = {} #  pais de cada vertice
        nivel = {} # nivel de cada vertice
        aresta = {} # classificacao das arestas

        # primeira insercao na fila eh o vertice do grafo (passado como parametro dessa funcao)
        fila.append(vertice_do_grafo)
        ordem_de_visita[vertice_do_grafo] = l # a ordem_de_visita  busca em largura comeca por 1
        pai[vertice_do_grafo] = None # o primeiro vertice a entrar na fila 
        nivel[vertice_do_grafo] = 1 # o nivel do primeiro vertice a entrar na fila a (raiz da arvore de busca em largura) eh 1

        # enquanto tivermos algum na fila vamos continuar a busca. 
        while len(fila):
            vertice = fila.pop(0) # pega o proximo vertice da fila
            # colocando os vizinhos que ainda  estavam na fila
            for vizinho in dicionario.get(vertice):
                # testando se o vizinho jah foi visitado (se o get retornar None, significa que este vertice nunca entrou na fila)
                if not ordem_de_visita.get(vizinho): # se o vizinho ainda naum foi visitado...
                    fila.append(vizinho) # ... colocamos na fila para visita-lo no seu devido momento
                    l += 1 # atualizando o contador de ordem_de_visita
                    ordem_de_visita[vizinho] = l
                    pai[vizinho] = vertice
                    nivel[vizinho] = nivel[vertice] + 1 # um vizinho esta sempre um nivel abaixo do pai            
        return ordem_de_visita, pai, aresta, nivel

    def busca_em_profundidade(self, dicionario, vertice_do_grafo):
        # todos os vertices do grafo comecam achando que eles mesmos sao seus vertice_mais_prox_da_raizs
        for vertice in dicionario:
            self.vertice_mais_prox_da_raiz[vertice] = vertice
        self.pai[vertice_do_grafo] = None  # a raiz naum tem pai
        qtd_filhos_da_raiz = self.chamada_para_busca_em_profundidade(dicionario, vertice_do_grafo, 1)
        if qtd_filhos_da_raiz <= 1:  # concerta a raiz
            # se a raiz soh tem um filho, significa que esse vertice, no grafo original, soh estah ligado a vertices que jah possuem um outro caminho entre eles que naum passa pela raiz, e portanto ela naum se trata de uma articulacao, pois remove-la naum desconectarah o grafo
            self.dic.remove(vertice_do_grafo)

    # funcao recursiva
    def chamada_para_busca_em_profundidade(self,dicionario, vertice_do_grafo, nivel):
        self.valor_profundidade_entrada += 1 # atualizando o contador de profundidade de entrada
        self.profundidades_entrada_saida[vertice_do_grafo] = [self.valor_profundidade_entrada, None] # anotando profundidade de entrada de vertice_do_grafo
        self.niveis[vertice_do_grafo] = nivel # anotando o nivel desse vertice_do_grafo na arvore de busca em profundidade
        count_filhos = 0 # contador de filhos do vertice por arestas 
        for vizinho in dicionario.get(vertice_do_grafo): # percorrendo os vizinhos de vertice_do_grafo
            if not self.profundidades_entrada_saida.get(vizinho): # testa se esse vizinho jah foi empilhado (chamado pela recursao)
                self.pai[vizinho] = vertice_do_grafo # se ainda não foi empilhado,atualizar quem é o pai 
                count_filhos += 1 # contando a quantidade de filhos do vertice por aresta da arvore
                self.chamada_para_busca_em_profundidade(dicionario, vizinho, nivel + 1) # o proximo vertice estará um nivel abaixo
                if self.niveis[self.vertice_mais_prox_da_raiz[vizinho]] < self.niveis[self.vertice_mais_prox_da_raiz[vertice_do_grafo]]: # caso meu filho tenha um vertice_mais_prox_da_raiz melhor 
                    self.vertice_mais_prox_da_raiz[vertice_do_grafo] = self.vertice_mais_prox_da_raiz[vizinho] # atualizo o meu vertice_mais_prox_da_raiz, para o vertice_mais_prox_da_raiz filho 
                if vizinho in self.demarcadores:
                    # se esse vertice_do_grafo é pai de um demarcador na arvore de busca em profundidade, entao ele é um verticemais proximo da raiz
                    self.dic.add(vertice_do_grafo)
            else: # caso o vizinho ja esteja na pilha 
                # testa se esse vizinho ja foi desipilhado
                if not self.profundidades_entrada_saida[vizinho][1]:
                    if self.pai[vertice_do_grafo] != vizinho: # testando se o vizinho é o pai do vertice tratado nessa chamada de chamada_para_busca_em_profundidade
                        # caso o vizinho não seja o pai do vertice dessa chamada de chamada_para_busca_em_profundidade
                        # por se tratar de uma aresta de retorno, pode ser que meu vizinho esteja mais proximo da raiz que o meu vertice_mais_prox_da_raiz...
                        if self.niveis[vizinho] < self.niveis[self.vertice_mais_prox_da_raiz[vertice_do_grafo]]:
                            self.vertice_mais_prox_da_raiz[vertice_do_grafo] = vizinho # atualizandoo meu vertice_mais_prox_da_raiz

        self.valor_profundidade_saida += 1 # atualizando o contador de profundidade de saida
        self.profundidades_entrada_saida[vertice_do_grafo][1] = self.valor_profundidade_saida
        # nesse momento sei se (vertic_do_grafo) é um desmarcador  ou não
        if self.vertice_mais_prox_da_raiz[vertice_do_grafo] in (vertice_do_grafo, self.pai[vertice_do_grafo]):
            self.demarcadores.add(vertice_do_grafo) 

        return count_filhos
  


def main():

    print("imprimir aqui")
    G = Graph()
    dado1 = "x1"
    dado2 = "x2"
    dado3 = "x3"
    dado4 = "x4"

    no1 = G.adiciona_vertice(dado1)
    no2 = G.adiciona_vertice(dado2)
    no3 = G.adiciona_vertice(dado3)
    no4 = G.adiciona_vertice(dado4)

    G.adiciona_aresta(no1, no1, "a1")
    G.adiciona_aresta(no1, no2, "a2")
    G.adiciona_aresta(no1, no3, "a3")
    G.adiciona_aresta(no2, no2, "a4")
    G.adiciona_aresta(no2, no4, "a5")
    G.adiciona_aresta(no3, no3, "a6")
    G.adiciona_aresta(no3, no3, "a7")
    G.adiciona_aresta(no4, no1, "a8")
    G.adiciona_aresta(no4, no3, "a9")



    

    dicionario =G.dicionario()
    #pegando as chaves do dicionario
    chaves = list(dicionario.keys())
    #print(dicionario.keys())

  
   

    

   
    print(G.imprimir())
    print("\n")

    print(dicionario)
   
    ordem_de_visita, pai, aresta, nivel = G.busca_em_largura(dicionario, chaves[0])
    print("------------Busca em Largura------------------------------------\n")
    print ("Ordem_de_visita : ",ordem_de_visita)
    print("\npai :",pai)

    print("\n------------Busca em Profundidade-----------------------------\n")
    G.busca_em_profundidade(dicionario, chaves[0])

    print("profundidade de entrada e saída",(G.profundidades_entrada_saida))
    print("\n pai ->",G.pai)
    print("\n niveis", G.niveis)



if __name__ == "__main__":
     main()



    
 













