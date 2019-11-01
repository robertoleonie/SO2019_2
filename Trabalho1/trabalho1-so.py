import sys

numQuadros = int(sys.argv[1])
arquivo = open(str(sys.argv[2]), 'r')                       # o segundo argumento sera o arquivo a ser lido
paginas = arquivo.readlines()                      # cada linha do arquivo txt sera uma posicao da lista paginas
memoria = []                                                # a memoria inicialmente sera uma lista vazia

##############################

# FIFO - implementacao mais facil.
# Sempre que uma pagina nao esta na memoria, adicione
# Se a memoria nao estiver cheia, apenas adicione paginas
# Se estiver cheia, elimina a pagina mais antiga da memoria, que sera memoria[0]
# depois a seguinte e assim por diante, voltando a 0 apos passar do numero de quadros
def fifo(numQuadros):
    contPageFaultFIFO = 0                                   # inicio o contador de falha de paginas com zero
    numPaginas = len(paginas)                               # pego o numero de paginas
    nextOut = 0                                             # inicialmente ninguem sai da memoria

    for i in range(0, numPaginas):                          # percorro todas as paginas
        if(paginas[i] not in memoria):                      # se a pagina corrente nao esta na memoria
            contPageFaultFIFO += 1                          # incremento o contador, afinal ouve uma falha de pagina
            if(numQuadros <= len(memoria)):                 # se nao ha espaco disponivel na memoria
                memoria[nextOut]= paginas[i]                # retiro a pagina corrente da memoria
            else :                                          # caso contrario
                memoria.append(paginas[i])                  # escrevo a pagina corrente na memoria
            nextOut = (nextOut + 1) % numQuadros            # passo adiante (de 0 a numQuadros-1)

    del memoria[:]                                          # limpo a memoria ao final do algoritmo
    return contPageFaultFIFO                                # retorna quantas falhas de pagina ocorreram

##############################

# LRU - implementacao de media dificuldade.
# Nessa solucao abusamos do fato do enunciado requisitar apenas o numero final de trocas, e nao do mapeamento total da memoria
# Se uma pagina que ja esta na memoria chega, NAO jogamos ela para o fim da lista memoria
# Caso contrario, a posicao ha mais tempo sem ser consultada tera seu elemento removido
# Somente no fim que arrumamos a lista para a primeira posicao sempre ser o elemento mais antigo
def lru(numQuadros):
    contPageFaultLRU = 0                                    # contador de falhas de pagina novamente comeca com zero
    numPaginas = len(paginas)

    for i in range(0, numPaginas):                          # percorro todas as paginas
        if(paginas[i] not in memoria):                      # se a pagina corrente nao esta na memoria
            contPageFaultLRU += 1                           # falha de pagina: incremento o contador
            if(numQuadros <= len(memoria)):                 # se nao ha espaco disponivel na memoria
                memoria.pop(0)                              # como se fosse uma pilha, desempilho o primeiro e jogo para o fim da lista, ja que nao sera
                                                            # uma pagina acessada recentemente
        else :                                              # caso contrario: se a pagina ja estiver na memoria
            memoria.remove(paginas[i])                      # removo a pagina da memoria na posicao atual para escreve-la no fim da lista memoria
        memoria.append(paginas[i])                          # de qualquer maneira, a pagina acessou a memoria, entao merece escrita

    del memoria[:]                                          # limpo a memoria ao final do algoritmo
    return contPageFaultLRU                                 # retorna quantas falhas de pagina ocorreram

##############################

# OPT - a implementacao mais dificil.
# Definitivamente nao foi a solucao mais simples, mas foi a que conseguimos rodar com entradas grandes.
# A ideia: quando uma pagina nova chega, olha entre todas as futuras paginas qual tem o maior indice na primeira vez que eh encontrada.
# Caso um ou mais itens da memoria nao estejam entre essas futuras, entao a ESCOLHIDA para remocao sera uma dessas, e veremos o historico de acesso de cada pagina.
def opt(numQuadros):
    contPageFaultOPT = 0                                    # contador de page fault sempre comeca com zero
    numPaginas = len(paginas)
    escolhida = -1                                          # inicialmente nenhuma pagina foi escolhida ainda

    for i in range(0, numPaginas):                          # percorro todas as paginas
        if(paginas[i] not in memoria):                      # se a pagina corrente nao esta na memoria
            contPageFaultOPT += 1                           # falha de pagina: incremento o contador
            if(numQuadros > len(memoria)):                  # se ha mais quadros disponiveis
                memoria.append(paginas[i])                  # apenas adiciono na memoria, pois ha espaco disponivel
            else:                                           # caso contrario
                lidos = []                                  # inicialmente nao foi verificado se alguma pagina aparecera futuramente
                anterior = 0
                # checa se todos os itens da memoria futuramente aparecerao, e se confirmado, qual pagina possui o maior indice
                for k in range(numQuadros):                 # percorre so os quadros da memoria
                    resto = paginas[i:]                     # cria uma lista com paginas que ainda nao foram validadas
                    if(memoria[k] in resto and memoria[k] not in lidos):
                    # se a memoria ainda sera testada e nao foi lida
                        if(resto.index(memoria[k])> anterior):  # se a posicao de memoria em teste eh corrente ou futura
                            escolhida = memoria[k]          # escolho ela
                            anterior = resto.index(memoria[k]) # testo a partir da pagina escolhida agora
                            lidos.append(memoria[k])        # li e testei a posicao atual
                                                            # se alguma pagina tenha sido pulada, entao percorremos o historico de tras para a frente, removendo novamente quem tem maior indice.
                if(len(lidos) != len(memoria)):         # se eu nao li todas as posicoes de memoria
                       resto = paginas[0:i]             # percorro tudo de novo
                       resto = resto[::-1]              # so que agora decrementando indice, ou seja, de tras para frente
                       anterior = 0                     # desligo o anterior
                       for k in range(numQuadros):      # percorro os quadros da memoria novamente
                           if(memoria[k] not in lidos and resto.index(memoria[k]) > anterior):
                            # se o quadro de memoria atual nao foi lido e o indice ainda eh mais alto do que as paginas, ja que estou decrementando, entao:
                              escolhida = memoria[k]    # escolho a pagina do quadro atual
                              anterior = resto.index(memoria[k])    # verifico agora a partir da pagina atual, mas de tras para frente ainda
                if(escolhida != 1):                     # se alguma pagina foi de fato escolhida
                    indice = memoria.index(escolhida)   # pego o indice da pagina escolhida na memoria
                    memoria[indice] = paginas[i]        # e adiciono a pagina no quadro de memoria

                else:
                    memoria.pop(0)                      # caso contrario, pego a pagina no primeiro quadro e jogo pro final para test
    # obs: olha quanta verificacao e quanta etapa de laÃ§o sera feita! deve ser por isso que o algoritmo aumenta a complexidade quando possui entradas muito grandes

    del memoria[:]                                          # limpo a memoria ao final do algoritmo
    return contPageFaultOPT                                 # retorno o numero de falhas de pagina

##############################

def gcc(numeroQuadrosVSIMGCC):                             # vou construir minha tabela.
    if(sys.argv[2] == 'vsim-gcc'):                          # se esse eh o arquivo que estamos abrindo entao
        print('FIFO | LRU | OPT')
        while(numeroQuadrosVSIMGCC <= 4096):
            print("%d | %d | %d" %                          # imprimo a tabela
                  (fifo(numeroQuadrosVSIMGCC),
                   lru(numeroQuadrosVSIMGCC),
                   opt(numeroQuadrosVSIMGCC)))
            numeroQuadrosVSIMGCC *= 4                   # a proxima linha eh o valor anterior multiplicado por 4

    else :
        return

### ATRIBUICOES FINAIS
totalDePaginas = len(paginas)
FIFO_final = fifo(numQuadros)
LRU_final = lru(numQuadros)
OPT_final = opt(numQuadros)

print("%5d quadros, %7d refs: FIFO: %5d PFs, LRU: %5d PFs, OPT: %5d PFs\n" %
         (numQuadros,
         totalDePaginas, FIFO_final, LRU_final, OPT_final))



gcc(64)                                                     # inicialmente este terceiro exemplo possui 64 quadros de entrada
arquivo.close()
