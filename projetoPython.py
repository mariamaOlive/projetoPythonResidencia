from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import matplotlib
import matplotlib.pyplot as plt
import numpy
import numpy as np

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

dicPlanos = {"top10": plano1, "top20": plano2, "top50": plano3}

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
    try: 
        cliente = dicionarioClientes[cpf]
        return cliente
    except:
        return []

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
    print("8 - Gráficos")
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

### Graficos

def graficoPlanos(dicionarioClientes):
    cont10=0
    cont20=0
    cont50=0
    for info in dicionarioClientes.values():
        if (info["plano"]=="top10"):
            cont10+=1
        elif (info["plano"]=="top20"):
            cont20+=1
        elif (info["plano"]=="top50"):
            cont50+=1

    x = ["Top 10", "Top 20", "Top 50"]
    y = [cont10, cont20, cont50]

    plt.bar(x, y, color='red', label='Grafico de barras dos planos telefônicos')
    plt.xlabel("Planos telefônicos")
    plt.ylabel("Quantidade")
    #plt.title("Grafico de barras dos planos telefônicos")
    plt.legend()
    plt.show()

def graficoPlanosPie(dicionarioClientes):
    cont10=0
    cont20=0
    cont50=0
    for info in dicionarioClientes.values():
        if (info["plano"]=="top10"):
            cont10+=1
        elif (info["plano"]=="top20"):
            cont20+=1
        elif (info["plano"]=="top50"):
            cont50+=1

    planos = ["Top 10", "Top 20", "Top 50"]
    count = [cont10, cont20, cont50]

    cores = ["paleturquoise", "darkred", "khaki"]
    # Criando um gráfico
    plt.pie(count, labels = planos, colors = cores, startangle = 90, shadow = True)
    plt.show()

def graficoIdadeSaldo(dicionarioClientes):
    idades = []
    saldos = []
    for info in dicionarioClientes.values():
        idades.append(int(info["nascimento"])) #implementar calculo da idade
        saldos.append(float(info["saldo"])) ### tirar o float() pra testar
    #idades.sort()
    plt.scatter(idades, saldos, color='red', label='Grafico de dispersão da idade e saldo')
    plt.xlabel("Idade")
    plt.ylabel("Saldo")
    plt.legend()
    plt.show()

def graficoPlanosIdade(dicionarioClientes):
  planos = ["Top 10", "Top 20", "Top 50"] #X = ['Group A','Group B','Group C','Group D']
  

  cont10a = cont20a = cont50a = cont10b = cont20b = cont50b = cont10c = cont20c = cont50c = 0

  for info in dicionarioClientes.values():
       if (info["plano"]=="top10"):
           if (int(info["nascimento"])<=30):
             cont10a+=1
           elif (int(info["nascimento"])<=60 and int(info["nascimento"])>30):
             cont10b+=1
           elif (int(info["nascimento"])>60):
             cont10c+=1
       elif (info["plano"]=="top20"):
           if (int(info["nascimento"])<=30):
             cont20a+=1
           elif (int(info["nascimento"])<=60 and int(info["nascimento"])>30):
             cont20b+=1
           elif (int(info["nascimento"])>60):
             cont20c+=1
       elif (info["plano"]=="top50"):
           if (int(info["nascimento"])<=30):
             cont50a+=1
           elif (int(info["nascimento"])<=60 and int(info["nascimento"])>30):
             cont50b+=1
           elif (int(info["nascimento"])>60):
             cont50c+=1

  conta = [cont10a, cont20a, cont50a]
  contb = [cont10b, cont20b, cont50b]
  contc = [cont10c, cont50c, cont50c]


  X_axis = np.arange(len(planos))
  
  #plt.bar(X_axis - 0.8, conta, 0.4, label = "Até 30")
  #plt.bar(X_axis + 0.8 , contb, 0.4, label = "30-60")
  #plt.bar(X_axis + 0.8, contc, 0.4, label = "60+")
  #plt.xticks(X_axis, planos)
  #plt.xlabel("Planos")
  #plt.ylabel("Quantidade")
  #plt.title("Gráfico...")
  #plt.legend()
  #plt.show()

  width = 0.25

  plt.bar(X_axis, conta, #color = 'b',
        width = width, edgecolor = 'black',
        label='Até 30 anos')
  plt.bar(X_axis + width, contb, #color = 'g',
        width = width, edgecolor = 'black',
        label='De 31 a 60 anos')
  plt.bar(X_axis + 2*width, contc, #color = 'y',
        width = width, edgecolor = 'black',
        label='61 anos ou mais')

  plt.xlabel("Planos")
  plt.ylabel("Quantidade de pessoas")
  plt.title("Quantidade de pessoas por plano e idade")
  # plt.grid(linestyle='--')
  plt.xticks(X_axis + width, planos)
  plt.legend()
  plt.show()



dici = {}
# dici={cliente1["cpf"]: cliente1}
lerArquivo(dici)
opcao = 99
while(opcao !=0):
     imprimeMenu()
     opcao = int(input())
     if(opcao==1):
         listarClientes(dici)
     elif(opcao==2): 
         cpf = input("Digite o CPF do cliente:")
         nome = input("Digite oo nome do cliente:")
         numero = input("Digite oo numero do cliente:")
         data = input("Digite a data de nascimento do cliente dd/mm/aaaa: ")
         plano = input("Digite o plano do cliente:")
         cliente = receberInfoCliente(cpf, nome, numero, data, plano, dicPlanos)
         inserirCliente(dici, cliente)
     elif(opcao==3):
         cpf = input("Digite o CPF do cliente para buscar:")
         buscarCliente(dici, cpf)
     elif(opcao==4):
         cpf = input("Digite o CPF do cliente para atualizar:")
         novoSaldo = float(input("Digite o novo saldo:"))
         atualizaSaldo(dici, cpf, novoSaldo)
     elif(opcao==5):
         cpf = input("Digite o CPF do cliente para adicionar a chamada:")
         chamada = input("Digite a chamada a ser adicionada:")
         adicionarChamada(dici, cpf, chamada)
     elif(opcao==6):
         cpf = input("Digite o CPF do cliente para deletar:")
         deletarCliente(dici, cpf)
     #elif(opcao==7):
     #    salvarArquivo(dici)
     elif(opcao==8):
         graficoPlanos(dici)
         graficoPlanosPie(dici)
         graficoIdadeSaldo(dici)
         graficoPlanosIdade(dici)
     elif(opcao==0):
         print("Fim da execução.")



""" ##Variáveis de interface
infoUsuarioLabels = ["CPF", "Nome", "Plano", "Data de Nascimento", ""]

##Funções auxiliares para interface
def buscarPlanos():
    planos = []
    for plano in dicPlanos.keys():
        planos.append(plano)
    return planos


##Carregamento da interface
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>(1)")
        print(request.form)

        opcao = list(request.form.keys())
        if('deletar' in opcao or 'adicionarSaldo' in opcao or 'adicionarChamada' in opcao):
            if(opcao[0]=='deletar'):
                deletarCliente(dici, request.form['deletar'])

        else:
            cpf = request.form["cpf"]
            if cpf!="":
                clienteUnico = [buscarCliente(dici, cpf)]
                return render_template('index.html', clientes=clienteUnico, planos = buscarPlanos(), usuarioLabel = infoUsuarioLabels)

    return render_template('index.html',clientes=listarClientes(dici), planos = buscarPlanos(), usuarioLabel = infoUsuarioLabels)

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

@app.route('/alterarCliente', methods=['POST'])
def alterar():
    print(request.form["cpf"])
    return redirect(url_for('index'))

@app.route('/alterarSaldo', methods=['POST'])
def alterarSaldo():
    print(">>>>>>>>>>>", request.form)
    cpf = request.form["cpf"]
    novoSaldo = request.form["novoSaldo"]
    atualizaSaldo(dici, cpf,novoSaldo)

    return redirect(url_for('index'))

@app.route('/adicionarChamada', methods=['POST'])
def inserirChamada():
    print(">>>>>>>>>>>", request.form)
    cpf = request.form["cpf"]
    novoNumero = request.form["novoNumero"]
    adicionarChamada(dici, cpf, novoNumero)

    return redirect(url_for('index'))


@app.route("/ajaxfile",methods=["POST","GET"])
def ajaxfile():
    if request.method == 'POST':
        print(">>>>>>>>>>>", request.form)
        cpf = request.form['cpf']
        tipoAcao = request.form['tipoAcao']
        print(cpf)
    return jsonify({'htmlresponse': render_template('modal.html',cpf=cpf, tipoAcao=tipoAcao)})
 """



