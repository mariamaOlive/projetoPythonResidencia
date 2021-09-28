import numpy as np
import random

probClientes = [20, 50, 30]
arrayProb = np.concatenate([np.full(20, 1), np.full(50, 2), np.full(30, 3)])
listaPlanos = ["top10", "top20", "top50"]
listaNomes = ["Maria", "João", "Bruna", "Gabriel", "Alice", "Mario", "Cristina", "Fernando"]
listaSobrenome = ["Oliveira", "Silva", "Arraes", "Pereira", "Assis", "Correia"]
listaClientes = []
carCliente = {
    1:{'infData': 1990,
    'supData': 2010,
        'mediaSaldo': 10,
        'vSaldo': 5,
        'mediaMinuto':50,
        'vMinuto':30,
        'mediaInternet':1,
        'vInternet': .5,
    },
    2:{'infData': 1960,
    'supData': 1989,
        'mediaSaldo': 30,
        'vSaldo': 10,
        'mediaMinuto':20,
        'vMinuto':5,
        'mediaInternet':4,
        'vInternet': 1,
    },
    3:{'infData': 1990,
    'supData': 2010,
        'mediaSaldo': 10,
        'vSaldo': 5,
        'mediaMinuto':50,
        'vMinuto':30,
        'mediaInternet':1,
        'vInternet': .5,
    }
}  


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


def gerarCliente(arrayProb, caracClientes):
    clienteType = definirTipoCliente(arrayProb)
    c = caracClientes[clienteType]
    
    dataNascimento = getDataNascimento(c["infData"], c["supData"])
    plano = probabilidadePlano(clienteType)
    saldo = random.normalvariate(c["mediaSaldo"], c["vSaldo"])
    minutoDisponivel = random.normalvariate(c["mediaMinuto"], c["vMinuto"])
    internetDisponivel = random.normalvariate(c["mediaInternet"], c["vInternet"])
    chamadas = criarChamadas() 
    return getCliente(getCpf(),getNome(), getNumero(), dataNascimento, plano, saldo, minutoDisponivel, internetDisponivel, chamadas )

    
def gerarListaClientes(numeroClientes, arrayProb, carCliente):
    listaClientes=[]
    for i in range(numeroClientes):
        listaClientes.append(gerarCliente(arrayProb, carCliente))

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

listaClientes = gerarListaClientes(100, arrayProb, carCliente)
salvarArquivo(listaClientes)