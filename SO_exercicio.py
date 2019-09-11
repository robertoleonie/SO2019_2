### CLASSE TAREFA

class Tarefa:
    sorter = 0
    tempoRestante = 0
    pd = 0
    def __init__(self, idTarefa, instanteIngresso, duracaoTarefa, prioridadeTarefa):
        self.idTarefa = idTarefa
        self.instanteIngresso = instanteIngresso
        self.duracaoTarefa = duracaoTarefa
        self.prioridadeTarefa = prioridadeTarefa

def programa():
    arquivo = open('entrada_so.txt', 'r')

    tarefas = arquivo.readlines()
    num_tarefas = int(tarefas[0])
    instanteIngresso = tarefas[1].split()
    duracaoTarefa = tarefas[2].split()
    prioridadeTarefa = tarefas[3].split()
    arquivo.close()
    array_tarefas = []
    for i in range(0,num_tarefas):
        array_tarefas.append(Tarefa(i, int(instanteIngresso[i]), int(duracaoTarefa[i]), int(prioridadeTarefa[i])))   # instanciei a classe

    execucao(num_tarefas, array_tarefas)

### POLITICAS DE ESCALONAMENTO
def execucao(num_tarefas, tarefas):

    def fcfs():
        tempoTotal = 0
        tempoEspera = 0
        tempoAcumulado = 0
        tarefas.sort(key = lambda x: x.instanteIngresso)
        for i in range(0,num_tarefas):
            tempoTotal += tarefas[i].duracaoTarefa + tempoAcumulado - tarefas[i].instanteIngresso
            if(i > 0):
                tempoEspera += tempoAcumulado - tarefas[i].instanteIngresso
            tempoAcumulado += tarefas[i].duracaoTarefa
        tempoTotal = tempoTotal/num_tarefas
        tempoEspera = tempoEspera/num_tarefas
        trocaDeContexto = num_tarefas - 1

        print('Politica FCFS:\nTempo total: {}\nTempo espera: {}\nTrocas de Contexto: {}'.format(tempoTotal, tempoEspera,trocaDeContexto))

    def round_robin():
        tempoTotal = 0
        tempoEspera = 0
        tempoAcumulado = 0
        trocaDeContexto = 0
        quantum = 2
        num_tarefas_restantes = num_tarefas
        valor = 0

        for i in tarefas:
            i.sorter = i.instanteIngresso

        while(num_tarefas_restantes > 0):
            if(quantum > tarefas[0].duracaoTarefa):
                valor = tarefas[0].duracaoTarefa
            else:
                valor = quantum

            tempoAcumulado += valor
            for i in range(1,num_tarefas_restantes):
                tarefas[i].tw += valor
            tarefas[0].sorter += 2
            tarefas[0].duracaoTarefa -= quantum

            if(tarefas[0].duracaoTarefa <= 0):
                tempoTotal += tempoAcumulado - tarefas[0].instanteIngresso
                tempoEspera += tarefas[0].tw - tarefas[0].instanteIngresso
                tarefas.pop(0)
                num_tarefas_restantes -= 1

            tarefas.sort(key = lambda x: x.sorter)
            trocaDeContexto += 1

        tempoTotal = tempoTotal / num_tarefas
        tempoEspera = tempoEspera / num_tarefas
        print('Politica RR:\nTempo total: {}\nTempo espera: {}\nTrocas de Contexto: {}\n'.format(tempoTotal, tempoEspera,trocaDeContexto - 1))

    def sjf(tarefas):
        tempoTotal = 0
        tempoEspera = 0
        tempoAcumulado = 0
        trocaDeContexto = 0
        cp_tarefas = []
        num_tarefas_restantes = num_tarefas

        for trf in tarefas:
            trf.sorter = trf.duracaoTarefa

        while(num_tarefas_restantes > 0):
            for trf in tarefas:
                if(trf.instanteIngresso <= tempoAcumulado):
                    cp_tarefas.append(trf)

            cp_tarefas.sort(key = lambda x : x.sorter)
            tempoAcumulado += cp_tarefas[0].duracaoTarefa
            tempoTotal += tempoAcumulado - cp_tarefas[0].instanteIngresso
            tempoEspera += tempoAcumulado - cp_tarefas[0].duracaoTarefa - cp_tarefas[0].instanteIngresso
            num_tarefas_restantes -= 1
            cp_tarefas[0].sorter += 90000

        tempoTotal = tempoTotal / num_tarefas
        tempoEspera = tempoEspera / num_tarefas
        trocaDeContexto = num_tarefas - 1
        print('Politica SJF:\nTempo total: {}\nTempo espera: {}\nTrocas de Contexto: {}\n'.format(tempoTotal, tempoEspera,trocaDeContexto))

    def srtf(tarefas):
        tempoTotal = 0
        tempoEspera = 0
        tempoAcumulado = 0
        trocaDeContexto = 0
        cp_tarefas = []
        num_tarefas_restantes = num_tarefas
        id_atual = -1
        for trf in tarefas:
            trf.tempoRestante = trf.duracaoTarefa

        while(num_tarefas_restantes > 0):
            for trf in tarefas:
                trf.sorter = trf.tempoRestante
                if(trf.instanteIngresso <= tempoAcumulado):
                    cp_tarefas.append(trf)
            cp_tarefas.sort(key = lambda x : x.sorter)
            tempoAcumulado += 1
            cp_tarefas[0].tempoRestante -= 1

            if(cp_tarefas[0].tempoRestante <= 0):
                tempoTotal += tempoAcumulado - cp_tarefas[0].instanteIngresso
                tempoEspera += tempoAcumulado - cp_tarefas[0].duracaoTarefa - cp_tarefas[0].instanteIngresso
                num_tarefas_restantes -= 1
                cp_tarefas[0].tempoRestante = 10000000

            if(cp_tarefas[0].idTarefa != id_atual):
                trocaDeContexto += 1

            id_atual = cp_tarefas[0].idTarefa
            cp_tarefas = []

        tempoTotal = tempoTotal / num_tarefas
        tempoEspera = tempoEspera / num_tarefas
        print('Politica SRTF:\nTempo total: {}\nTempo espera: {}\nTrocas de Contexto: {}\n'.format(tempoTotal, tempoEspera,trocaDeContexto - 1))

    def prioC(tarefas):
        tempoTotal = 0
        tempoEspera = 0
        tempoAcumulado = 0
        trocaDeContexto = 0
        cp_tarefas = []
        num_tarefas_restantes = num_tarefas

        for trf in tarefas:
            trf.sorter = trf.prioridadeTarefa

        while(num_tarefas_restantes > 0):
            for trf in tarefas:
                if(trf.instanteIngresso <= tempoAcumulado):
                    cp_tarefas.append(trf)
            cp_tarefas.sort(key = lambda x : x.sorter, reverse = True)
            tempoAcumulado += cp_tarefas[0].duracaoTarefa
            tempoTotal += tempoAcumulado - cp_tarefas[0].instanteIngresso
            tempoEspera += tempoAcumulado - cp_tarefas[0].duracaoTarefa - cp_tarefas[0].instanteIngresso
            num_tarefas_restantes -= 1
            cp_tarefas[0].sorter -= 90000
            cp_tarefas = []
        tempoTotal = tempoTotal / num_tarefas
        tempoEspera = tempoEspera / num_tarefas
        trocaDeContexto = num_tarefas - 1
        print('Politica PRIOC:\nTempo total: {}\nTempo espera: {}\nTrocas de Contexto: {}\n'.format(tempoTotal, tempoEspera,trocaDeContexto))

    def prioP(tarefas):
        tempoTotal = 0
        tempoEspera = 0
        tempoAcumulado = 0
        trocaDeContexto = 0
        cp_tarefas = []
        num_tarefas_restantes = num_tarefas
        id_atual = -1
        for trf in tarefas:
            trf.tempoRestante = trf.duracaoTarefa

        while(num_tarefas_restantes > 0):
            for trf in tarefas:
                trf.sorter = trf.prioridadeTarefa
                if(trf.instanteIngresso <= tempoAcumulado):
                    cp_tarefas.append(trf)
            cp_tarefas.sort(key = lambda x : x.sorter, reverse = True)
            tempoAcumulado += 1
            cp_tarefas[0].tempoRestante -= 1

            if(cp_tarefas[0].tempoRestante <= 0):
                tempoTotal += tempoAcumulado - cp_tarefas[0].instanteIngresso
                tempoEspera += tempoAcumulado - cp_tarefas[0].duracaoTarefa - cp_tarefas[0].instanteIngresso
                num_tarefas_restantes -= 1
                cp_tarefas[0].prioridadeTarefa = -1

            if(cp_tarefas[0].idTarefa != id_atual):
                trocaDeContexto += 1

            id_atual = cp_tarefas[0].idTarefa
            cp_tarefas = []

        tempoTotal = tempoTotal / num_tarefas
        tempoEspera = tempoEspera / num_tarefas
        print('Politica PRIOP:\nTempo total: {}\nTempo espera: {}\nTrocas de Contexto: {}\n'.format(tempoTotal, tempoEspera,trocaDeContexto - 1))

    def prioD(tarefas, alfa):
        tempoTotal = 0
        tempoEspera = 0
        tempoAcumulado = 0
        trocaDeContexto = 0
        cp_tarefas = []
        num_tarefas_restantes = num_tarefas
        id_atual = -1
        for trf in tarefas:
            trf.pd = trf.prioridadeTarefa
            trf.tempoRestante = trf.duracaoTarefa

        while(num_tarefas_restantes > 0):
            for trf in tarefas:
                trf.sorter = trf.pd
                if(trf.instanteIngresso <= tempoAcumulado):
                    cp_tarefas.append(trf)

            cp_tarefas.sort(key = lambda x : x.sorter, reverse = True)
            if(num_tarefas_restantes > 1 and cp_tarefas[0].pd == cp_tarefas[1].pd ):
                cp_tarefas[0] = cp_tarefas[1]
            tempoAcumulado += 1
            cp_tarefas[0].tempoRestante -= 1
            print(cp_tarefas[0].pd, cp_tarefas[0].idTarefa)
            if(cp_tarefas[0].tempoRestante <= 0):
                tempoTotal += tempoAcumulado - cp_tarefas[0].instanteIngresso
                tempoEspera += tempoAcumulado - cp_tarefas[0].duracaoTarefa - cp_tarefas[0].instanteIngresso
                num_tarefas_restantes -= 1
                for i in range(num_tarefas):
                    if(cp_tarefas[0].idTarefa == tarefas[i].idTarefa):
                        tarefas.pop(i)
                        break


            if(cp_tarefas[0].idTarefa != id_atual):
                trocaDeContexto += 1

            id_atual = cp_tarefas[0].idTarefa
            #print(id_atual)

            for trf in tarefas:
                if(trf.instanteIngresso <= tempoAcumulado and trf.idTarefa != id_atual):
                    trf.pd += alfa
                elif(trf.idTarefa == id_atual):
                    trf.pd = trf.prioridadeTarefa

            cp_tarefas = []
            #cp_tarefas[0].sorter

        tempoTotal = tempoTotal / num_tarefas
        tempoEspera = tempoEspera / num_tarefas
        #falta troca de contexto
        print('Politica PRIOD:\nTempo total: {}\nTempo espera: {}\nTrocas de Contexto: {}\n'.format(tempoTotal, tempoEspera,trocaDeContexto - 1))


    # fcfs(n)
    #round_robin(n)
    #sjf(n)
    #srtf(n)
    #prioC(n)
    #prioP(n)
    prioD(tarefas, 1)

### MAIN
programa()
