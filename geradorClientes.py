import numpy as np
import random

probClientes = [20, 50, 30]
arrayProb = np.concatenate([np.full(20, 1), np.full(50, 2), np.full(30, 3)])
listaPlanos = ["top10", "top20", "top50"]
listaNomes = ["Maria", "João", "Bruna", "Gabriel", "Alice", "Mario", "Cristina", "Fernando"]
listaSobrenome = ["Oliveira", "Silva", "Arraes", "Pereira", "Assis", "Correia"]
listaClientes = []


def definirTipoCliente(arrayProb):
    indexValor = random.randint(0,99)
    return arrayProb[indexValor]

# Probabilidade de um cliente ter um certo tipo de plano
def probabilidadePlano(tipoCliente):
    arrayProbPlano = []

    if(tipoCliente==1):
        arrayProbPlano = np.concatenate([np.full(50, "top10"), np.full(40, "top20"), np.full(10, "top50")])
    elif(tipoCliente==2):
        arrayProbPlano = np.concatenate([np.full(10, "top10"), np.full(40, "top20"), np.full(60, "top50")])
    else:
        arrayProbPlano = np.concatenate([np.full(30, "top10"), np.full(60, "top20"), np.full(10, "top50")])

    return arrayProbPlano[random.randint(0,99)]

def criarChamadas():
    numeroChamdas = random.randint(1,15)
    listaChamadas = []
    for i in range(numeroChamdas):
        numero = str(random.randint(1111,9999))+"-"+str(random.randint(1111,9999))
        listaChamadas.append(numero)
     
    return listaChamadas

def getDataNascimento(anoInicial, anoFinal):
    return  str(random.randint(1,31))+"/"+str(random.randint(1,12))+"/"+ str(random.randint(anoInicial,anoFinal))

def getCpf():
    return str(random.randint(111111111,999999999))+"-"+str(random.randint(11,99))

def getNome():
    nome = listaNomes[random.randint(0, len(listaNomes)-1)]
    sobrenome = listaSobrenome[random.randint(0, len(listaSobrenome)-1)]
    return nome + " " + sobrenome

def getNumero():
    return str(random.randint(111111111,999999999))

def getCliente(cpf, nome, numero, dataNascimento, plano, saldo, minutoDisponivel, internetDisponivel, chamadas): ### pega os inputs para usar em inserirCliente
    ### recebe input com as informações do cliente e devolve um cliente
    cliente = {
    "cpf": cpf,
    "nome": nome,
    "numero": numero,
    "nascimento": dataNascimento,
    "plano": plano,
    "saldo": saldo,
    "minutoDisponivel": minutoDisponivel, 
    "internetDisponivel": internetDisponivel,
    "chamadas" : chamadas  
    }
    return cliente


def gerarCliente(arrayProb):
    tipoCliente = definirTipoCliente(arrayProb)
    
    if(tipoCliente==1):
        dataNascimento = getDataNascimento(1990, 2010)
        plano = probabilidadePlano(1)
        saldo = random.normalvariate(10, 5)
        minutoDisponivel = random.normalvariate(50, 30)
        internetDisponivel = random.normalvariate(1, .5)
        chamadas = criarChamadas() 
        return getCliente(getCpf(),getNome(), getNumero(), dataNascimento, plano, saldo, minutoDisponivel, internetDisponivel, chamadas )

    elif(tipoCliente==2):
        dataNascimento = getDataNascimento(1960, 1989)
        plano = probabilidadePlano(2)
        saldo = random.normalvariate(30, 10)
        minutoDisponivel = random.normalvariate(20, 5)
        internetDisponivel = random.normalvariate(4, 1)
        chamadas = criarChamadas() 
        return getCliente(getCpf(),getNome(), getNumero(), dataNascimento, plano, saldo, minutoDisponivel, internetDisponivel, chamadas )
    else:
        dataNascimento = getDataNascimento(1922, 1959)
        plano = probabilidadePlano(3)
        saldo = random.normalvariate(50, 20)
        minutoDisponivel = random.normalvariate(40, 10)
        internetDisponivel = random.normalvariate(10, 1)
        chamadas = criarChamadas() 
        return getCliente(getCpf(),getNome(), getNumero(), dataNascimento, plano, saldo, minutoDisponivel, internetDisponivel, chamadas )


def gerarListaClientes(numeroClientes, arrayProb):
    listaClientes=[]
    for i in range(numeroClientes):
        listaClientes.append(gerarCliente(arrayProb))

    return listaClientes


def salvarArquivo(listaClientes):
    arquivo = open("listaClientes2.txt", "w")
    
    for cliente in listaClientes:
        stringArquivo = ""
        stringArquivo += cliente["nome"]+"\n"
        stringArquivo += cliente["cpf"]+"\n"
        stringArquivo += cliente["numero"]+"\n"
        stringArquivo += cliente["nascimento"]+"\n"
        stringArquivo += cliente["plano"]+"\n"
        stringArquivo += str(round(cliente["saldo"],2))+"\n"
        stringArquivo += str(int(cliente["minutoDisponivel"]))+"\n"
        stringArquivo += str(int(cliente["internetDisponivel"]))+"\n"
        stringArquivo += "[\n"
        for chamada in cliente["chamadas"]:
            stringArquivo+= chamada + "\n"
        stringArquivo+="]\n"

        arquivo.write(stringArquivo)
    
    arquivo.close()

listaClientes = gerarListaClientes(100, arrayProb)
salvarArquivo(listaClientes)
