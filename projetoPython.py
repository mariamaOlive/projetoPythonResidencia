from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

### Projeto Residencia Python - Operadoras Telefonicas
### Lucas e Mariama

# chamada1 = {
#     "dataHora": "23/12/2013",
#     "numero": "1341234",
#     "duracao":34
# }

# chamada2 = {
#     "dataHora": "23/12/2013",
#     "numero": "1341234",
#     "duracao":34
# }

plano1 = {
    "nome": "top10",
    "minutosChamada": 10,
    "gigaInternet":5
}
plano2 = {
    "nome": "top20",
    "minutosChamada": 20,
    "gigaInternet":10
}
plano3 = {
    "nome": "top50",
    "minutosChamada": 50,
    "gigaInternet":25
}

dicPlanos = {"top10": plano1, "top20": plano1, "top50": plano1}

cliente1 = {
    "cpf": "135134",
    "nome": "Maria Silva",
    "numero": "41341234",
    "nascimento": "23/10/1950",
    "plano": "top50",
    "saldo": 20,
    "minutoDisponivel":100, 
    "internetDisponivel":4000,
    "chamadas" : ["94313-414"] 
}

cliente2 = {
    "cpf": "111111",
    "nome": "Gabriel Silva",
    "numero": "91234134",
    "nascimento": "23/10/1950",
    "plano": "top50",
    "saldo": 20,
    "minutoDisponivel":100, 
    "internetDisponivel":4000,
    "chamadas" : ["4313-414", "4123-4143"]  
}


def listarClientes(dicionarioClientes):
    lista = []
    for info in dicionarioClientes.values():
        lista.append(info)

    print(lista)
    return lista


def inserirCliente(dicionarioClientes, cliente):
    chave = cliente["cpf"]
    dicionarioClientes[chave] = cliente
    salvarArquivo(dicionarioClientes)
    #return Bool
    
def receberInfoCliente(cpf, nome, numero, dataNascimento, plano, planosDisponiveis): ### pega os inputs para usar em inserirCliente
    ### recebe input com as informações do cliente e devolve um cliente
    cliente = {
    "cpf": cpf,
    "nome": nome,
    "numero": numero,
    "nascimento": dataNascimento,
    "plano": plano,
    "saldo": 0,
    "minutoDisponivel": planosDisponiveis[plano]["minutosChamada"], 
    "internetDisponivel": planosDisponiveis[plano]["gigaInternet"],
    "chamadas" : []  
    }
    return cliente

def lerCliente(cpf, nome, numero, dataNascimento, plano, saldo, minutoDisponivel, internetDisponivel, chamadas): ### pega os inputs para usar em inserirCliente
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

def buscarCliente(dicionarioClientes, cpf):
    ###Busca cliente de acordo com o cpf
    cliente = dicionarioClientes[cpf]
    print(cliente)
    return cliente

def atualizaSaldo(dicionarioClientes, cpf, novoSaldo):
    dicionarioClientes[cpf]["saldo"] = novoSaldo
    salvarArquivo(dicionarioClientes)
    #return Bool

def adicionarChamada(dicionarioClientes, cpf, chamada):
    #Adiciona uma nova chamada ao cliente
    dicionarioClientes[cpf]["chamadas"].append(chamada)
    salvarArquivo(dicionarioClientes)
    #return Bool

def deletarCliente(dicionarioClientes, cpf):
    dicionarioClientes.pop(cpf)
    salvarArquivo(dicionarioClientes)
    ###

def imprimeMenu():
    print("Menu - Escolha uma opção:")
    print("1 - Listar clientes")
    print("2 - Inserir clientes")
    print("3 - Buscar clientes")
    print("4 - Atualizar o saldo")
    print("5 - Adicionar chamada")
    print("6 - Deletar cliente")
    #print("7 - Salvar arquivo")
    print("0 - Fim da execução")


def salvarArquivo(dicionarioClientes):
    arquivo = open("listaClientes.txt", "w")
    
    for info in dicionarioClientes.values():
        stringArquivo = ""
        stringArquivo += info["nome"]+"\n"
        stringArquivo += info["cpf"]+"\n"
        stringArquivo += info["numero"]+"\n"
        stringArquivo += info["nascimento"]+"\n"
        stringArquivo += info["plano"]+"\n"
        stringArquivo += str(info["saldo"])+"\n"
        stringArquivo += str(info["minutoDisponivel"])+"\n"
        stringArquivo += str(info["internetDisponivel"])+"\n"
        stringArquivo += "[\n"
        for chamada in info["chamadas"]:
            stringArquivo+= chamada + "\n"
        stringArquivo+="]\n"

        arquivo.write(stringArquivo)
    
    arquivo.close()



def lerArquivo(dicClientes):
    arquivo = open("listaClientes.txt", "r")
    linhas = arquivo.readlines()
    cont = 0

    while cont<=(len(linhas)-1):
        nome = linhas[cont].strip()
        cpf = linhas[cont+1].strip()
        numero = linhas[cont+2].strip()
        dataNascimento = linhas[cont+3].strip()
        plano = linhas[cont+4].strip()
        saldo = linhas[cont+5].strip()
        minutoDisponivel = linhas[cont+6].strip()
        internetDisponivel = linhas[cont+7].strip()
        cont+=9
        chamadas = []
        while linhas[cont]!="]\n":
            chamadas.append(linhas[cont].strip())
            cont+=1
        cont+=1
        
        cliente = lerCliente(cpf, nome, numero, dataNascimento, plano, saldo, minutoDisponivel, internetDisponivel, chamadas)
        dicClientes[cpf] = cliente

    return dicClientes

    
dici = {}
# dici={cliente1["cpf"]: cliente1}
lerArquivo(dici)
opcao = 99
# while(opcao !=0):
#     imprimeMenu()
#     opcao = int(input())
#     if(opcao==1):
#         listarClientes(dici)
#     elif(opcao==2): 
#         cpf = input("Digite o CPF do cliente:")
#         nome = input("Digite oo nome do cliente:")
#         numero = input("Digite oo numero do cliente:")
#         data = input("Digite a data de nascimento do cliente dd/mm/aaaa: ")
#         plano = input("Digite o plano do cliente:")
#         cliente = receberInfoCliente(cpf, nome, numero, data, plano, dicPlanos)
#         inserirCliente(dici, cliente)
#     elif(opcao==3):
#         cpf = input("Digite o CPF do cliente para buscar:")
#         buscarCliente(dici, cpf)
#     elif(opcao==4):
#         cpf = input("Digite o CPF do cliente para atualizar:")
#         novoSaldo = float(input("Digite o novo saldo:"))
#         atualizaSaldo(dici, cpf, novoSaldo)
#     elif(opcao==5):
#         cpf = input("Digite o CPF do cliente para adicionar a chamada:")
#         chamada = input("Digite a chamada a ser adicionada:")
#         adicionarChamada(dici, cpf, chamada)
#     elif(opcao==6):
#         cpf = input("Digite o CPF do cliente para deletar:")
#         deletarCliente(dici, cpf)
#     #elif(opcao==7):
#     #    salvarArquivo(dici)
#     elif(opcao==0):
#         print("Fim da execução.")

def buscarPlanos():
    planos = []
    for plano in dicPlanos.keys():
        planos.append(plano)
    return planos
    

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cpf = request.form["cpf"]
        if cpf=="":
            return render_template('index.html',clientes=listarClientes(dici), planos = buscarPlanos())
        else:
            clienteUnico = [buscarCliente(dici, cpf)]
            return render_template('index.html', clientes=clienteUnico, planos = buscarPlanos())

    return render_template('index.html',clientes=listarClientes(dici), planos = buscarPlanos())

@app.route('/inserir', methods=['POST'])
def inserir():
    cliente = receberInfoCliente(
                request.form["novoCpf"],
                request.form["novoNome"], 
                request.form["novoNumero"], 
                request.form["novoData"], 
                request.form["radioPlano"], 
                dicPlanos)
    inserirCliente(dici, cliente)
    return redirect(url_for('index'))