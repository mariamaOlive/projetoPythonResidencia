import numpy as np
import matplotlib.pyplot as plt
import os.path
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, Response
from flask_bootstrap import Bootstrap
import matplotlib
matplotlib.use('Agg')


# Tipos de planos telefonicos (a principio podemos tirar essas informacoes)
plano1 = {
    "nome": "top10",
    "minutosChamada": 100,
    "gigaInternet": 10
}
plano2 = {
    "nome": "top20",
    "minutosChamada": 200,
    "gigaInternet": 20
}
plano3 = {
    "nome": "top50",
    "minutosChamada": 500,
    "gigaInternet": 50
}

###
dicPlanos = {"top10": plano1, "top20": plano2, "top50": plano3}

# Função para salvar o dicionario no arquivo (função utilizada em todas as operações que alterem o dicionario)
def salvarArquivo(dicionarioClientes, nomeArq):
    arquivo = open(nomeArq, "w")

    for info in dicionarioClientes.values():
        stringArquivo = ""
        stringArquivo += info["nome"]+"\n"
        stringArquivo += info["cpf"]+"\n"
        stringArquivo += info["numero"]+"\n"
        stringArquivo += info["nascimento"]+"\n"
        stringArquivo += info["plano"]+"\n"
        stringArquivo += str(info["saldo"])+"\n"
        stringArquivo += str(info["minutoConsumido"])+"\n"
        stringArquivo += str(info["internetConsumida"])+"\n"
        stringArquivo += "[\n"
        for chamada in info["chamadas"]:
            stringArquivo += chamada + "\n"
        stringArquivo += "]\n"

        arquivo.write(stringArquivo)

    arquivo.close()

# Função para listar todos os clientes do dicionario
def listarClientes(dicionarioClientes):
    lista = []
    for info in dicionarioClientes.values():
        lista.append(info)
    return lista

# Função para inserir clientes no dicionario (como em toda operação que altera, ele salva no arquivo também)
def inserirCliente(dicionarioClientes, cliente):
    chave = cliente["cpf"]
    dicionarioClientes[chave] = cliente
    salvarArquivo(dicionarioClientes, nomeArquivo)


# Função para pegar os inputs para usar em inserirCliente
def receberInfoCliente(cpf, nome, numero, dataNascimento, plano, planosDisponiveis):
    # recebe input com as informações do cliente e devolve um cliente
    cliente = {
        "cpf": cpf,
        "nome": nome,
        "numero": numero,
        "nascimento": dataNascimento,
        "plano": plano,
        "saldo": 0,
        "minutoConsumido": 0,
        "internetConsumida": 0,
        "chamadas": []
    }
    return cliente


# Função para buscar cliente de acordo com o cpf
def buscarCliente(dicionarioClientes, cpf):
    try:
        cliente = dicionarioClientes[cpf]
        return cliente
    except:
        return None

# Função para atualizar o saldo disponível de um cliente de acordo com o cpf
def atualizaSaldo(dicionarioClientes, cpf, novoSaldo):
    dicionarioClientes[cpf]["saldo"] = round(float(dicionarioClientes[cpf]["saldo"]) + float(novoSaldo), 2)
    salvarArquivo(dicionarioClientes, nomeArquivo)


# Função para adicionar chamadas realizadas para um cliente de acordo com o cpf
def adicionarChamada(dicionarioClientes, cpf, chamada):
    # Adiciona uma nova chamada ao cliente
    dicionarioClientes[cpf]["chamadas"].append(chamada)
    salvarArquivo(dicionarioClientes, nomeArquivo)

# Função para deletar um cliente do dicionario e do arquivo de acordo com o cpf
def deletarCliente(dicionarioClientes, cpf):
    dicionarioClientes.pop(cpf)
    salvarArquivo(dicionarioClientes, nomeArquivo)


# Função para pegar os inputs para usar em lerArquivo
def lerCliente(cpf, nome, numero, dataNascimento, plano, saldo, minutoConsumido, internetConsumida, chamadas):
    # recebe input com as informações do cliente e devolve um cliente
    cliente = {
        "cpf": cpf,
        "nome": nome,
        "numero": numero,
        "nascimento": dataNascimento,
        "plano": plano,
        "saldo": saldo,
        "minutoConsumido": minutoConsumido,
        "internetConsumida": internetConsumida,
        "chamadas": chamadas
    }
    return cliente

# Função para ler o arquivo com as informações dos clientes
def lerArquivo(dicClientes, nomeArq):

    if os.path.isfile(nomeArq):
        arquivo = open(nomeArq, "r")
        linhas = arquivo.readlines()
        cont = 0

        while cont <= (len(linhas)-1):
            nome = linhas[cont].strip()
            cpf = linhas[cont+1].strip()
            numero = linhas[cont+2].strip()
            dataNascimento = linhas[cont+3].strip()
            plano = linhas[cont+4].strip()
            saldo = linhas[cont+5].strip()
            minutoConsumido = linhas[cont+6].strip()
            internetConsumida = linhas[cont+7].strip()
            cont += 9
            chamadas = []
            while linhas[cont] != "]\n":
                chamadas.append(linhas[cont].strip())
                cont += 1
            cont += 1

            cliente = lerCliente(cpf, nome, numero, dataNascimento, plano, saldo, minutoConsumido, internetConsumida, chamadas)
            dicClientes[cpf] = cliente

    return dicClientes

    

# Graficos

# Grafico 1: Grafico de setores dos planos telefonicos
def graficoPlanosPie(dicionarioClientes, modo):
    plt.clf()
    path = "static/plot1.png"
    cont10 = 0
    cont20 = 0
    cont50 = 0
    for info in dicionarioClientes.values():
        if (info["plano"] == "top10"):
            cont10 += 1
        elif (info["plano"] == "top20"):
            cont20 += 1
        elif (info["plano"] == "top50"):
            cont50 += 1

    planos = ["Top 10", "Top 20", "Top 50"]
    count = [cont10, cont20, cont50]

    cores = ["paleturquoise", "darkred", "khaki"]
    plt.pie(count, labels=planos, colors=cores, startangle=90, shadow=True)
    plt.title("Gráfico de setores dos planos telefônicos")
    plt.legend(planos)
    if modo == "exibir":
        plt.show()
    elif modo == "salvar":
        plt.savefig(path)
    return path

# Função básica para calcular idade baseada apenas no ano de nascimento (poderiamos utilizar biblioteca datetime para fazer isso de forma simples e melhor)
def calculaIdade(nascimento):
    tam = len(nascimento)
    idade = 2021-int(nascimento[tam-4:tam])
    return idade

# Gráfico 2: Grafico de dispersao da idade e saldo disponivel
def graficoIdadeSaldo(dicionarioClientes, modo):
    plt.clf()
    path = "static/plot2.png"
    idades = []
    saldos = []
    for info in dicionarioClientes.values():
        idade = calculaIdade(info["nascimento"])
        idades.append(idade)
        saldos.append(float(info["saldo"]))
    plt.scatter(idades, saldos, color="red")
    plt.xlabel("Idade")
    plt.ylabel("Saldo disponível")
    plt.title("Gráfico de dispersão da idade e saldo disponível")
    if modo == "exibir":
        plt.show()
    elif modo == "salvar":
        plt.savefig(path)
    return path

# Grafico 3: Gráfico de barras da quantidade de pessoas por plano e idade
def graficoPlanosIdade(dicionarioClientes, modo):
    plt.clf()
    path = "static/plot3.png"
    planos = ["Top 10", "Top 20", "Top 50"]

    cont10a = cont20a = cont50a = cont10b = cont20b = cont50b = cont10c = cont20c = cont50c = 0

    # Faixa de idade a = ate 30 anos ; faixa de idade b = 31 a 60 anos ; faixa de idade c = 61+
    # for para contar quantos clientes tem em cada plano (top10,top20,top50) para cada faixa de idade(a,b,c)
    for info in dicionarioClientes.values():
        if (info["plano"] == "top10"):
            if (calculaIdade(info["nascimento"]) <= 30):
                cont10a += 1
            elif (calculaIdade(info["nascimento"]) <= 60 and calculaIdade(info["nascimento"]) > 30):
                cont10b += 1
            elif (calculaIdade(info["nascimento"]) > 60):
                cont10c += 1
        elif (info["plano"] == "top20"):
            if (calculaIdade(info["nascimento"]) <= 30):
                cont20a += 1
            elif (calculaIdade(info["nascimento"]) <= 60 and calculaIdade(info["nascimento"]) > 30):
                cont20b += 1
            elif (calculaIdade(info["nascimento"]) > 60):
                cont20c += 1
        elif (info["plano"] == "top50"):
            if (calculaIdade(info["nascimento"]) <= 30):
                cont50a += 1
            elif (calculaIdade(info["nascimento"]) <= 60 and calculaIdade(info["nascimento"]) > 30):
                cont50b += 1
            elif (calculaIdade(info["nascimento"]) > 60):
                cont50c += 1

    conta = [cont10a, cont20a, cont50a]
    contb = [cont10b, cont20b, cont50b]
    contc = [cont10c, cont50c, cont50c]

    X_axis = np.arange(len(planos))
    width = 0.25

    plt.bar(X_axis, conta, width=width, edgecolor='black', label='Até 30 anos') #Grafico de barras dos planos de pessoas da faixa A
    plt.bar(X_axis + width, contb, width=width, edgecolor='black', label='De 31 a 60 anos') # Grafico de barras dos planos das pessoas da faixa B
    plt.bar(X_axis + 2*width, contc, width=width, edgecolor='black', label='61 anos ou mais') # Grafico de barras dos planos das pessoas da faixa C

    plt.xlabel("Planos telefônicos")
    plt.ylabel("Quantidade de pessoas")
    plt.title("Gráfico de barras da quantidade de pessoas por plano e idade")
    plt.xticks(X_axis + width, planos)
    plt.legend()
    if modo == "exibir":
        plt.show()
    elif modo == "salvar":
        plt.savefig(path)
    return path

# Grafico 4: Grafico de dispersão de minutos por quantidade de chamadas e saldo
def graficoMinutosChamadas(dicionarioClientes, modo):
    plt.clf()
    minutos = []
    qtdChamadas = []
    saldos = []
    size = 5 #tamanho dos caracteres
    path = "static/plot4.png"

    for info in dicionarioClientes.values():
        minutos.append(int(info["minutoConsumido"]))
        qtdChamadas.append(len(info["chamadas"]))
        saldos.append(float(info["saldo"])*size) # size referente ao tamanho do caracter (no caso estrela)
    plt.scatter(qtdChamadas, minutos, marker="*", s=saldos,
                color='red', label="Saldo disponível")
    plt.xlabel("Quantidade de chamadas realizadas")
    plt.ylabel("Minutos gastos")
    plt.title('Grafico de dispersão de minutos por quantidade de chamadas e saldo')
    plt.legend()
    if modo == "exibir":
        plt.show()
    elif modo == "salvar":
        plt.savefig(path)

    return path


# Inicializa o dicionario e leitura do arquivo
dici = {}
nomeArquivo = "listaClientes.txt"
lerArquivo(dici, nomeArquivo)


######
# INTERFACE GRAFICA A PARTIR DAQUI
######

# Variáveis de interface
infoUsuarioLabels = ["CPF", "Nome", "Plano", "Data de Nascimento", ""]

# Funções auxiliares para interface
def buscarPlanos():
    planos = []
    for plano in dicPlanos.keys():
        planos.append(plano)
    return planos


# Carregamento da interface
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        opcao = list(request.form.keys())
        if('deletar' in opcao):
            if(opcao[0] == 'deletar'):
                deletarCliente(dici, request.form['deletar'])

        else:
            cpf = request.form["cpf"]
            if cpf != "":
                clienteUnico = [buscarCliente(dici, cpf)] if buscarCliente(
                    dici, cpf) != None else None
                return render_template('index.html', clientes=clienteUnico, planos=buscarPlanos(), usuarioLabel=infoUsuarioLabels)

    return render_template('index.html', clientes=listarClientes(dici), planos=buscarPlanos(), usuarioLabel=infoUsuarioLabels)


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


@app.route('/alterarSaldo', methods=['POST'])
def alterarSaldo():
    cpf = request.form["cpf"]
    novoSaldo = request.form["novoSaldo"]
    atualizaSaldo(dici, cpf, novoSaldo)

    return redirect(url_for('index'))


@app.route('/adicionarChamada', methods=['POST'])
def inserirChamada():
    cpf = request.form["cpf"]
    novoNumero = request.form["novoNumero"]
    adicionarChamada(dici, cpf, novoNumero)

    return redirect(url_for('index'))


@app.route("/ajaxfile", methods=["POST", "GET"])
def ajaxfile():
    if request.method == 'POST':
        cpf = request.form['cpf']
        tipoAcao = request.form['tipoAcao']
    return jsonify({'htmlresponse': render_template('modal.html', cpf=cpf, tipoAcao=tipoAcao)})


@app.route("/ajaxfilevisualizacao", methods=["POST", "GET"])
def ajaxfilevisualizacao():
    if request.method == 'POST':
        visType = request.form['vis']
        imagem = ""
        if(visType == "vis1"):
            image = graficoPlanosPie(dici, "salvar")
        elif (visType == "vis2"):
            image = graficoIdadeSaldo(dici, "salvar")
        elif (visType == "vis3"):
            image = graficoPlanosIdade(dici, "salvar")
        else:
            image = graficoMinutosChamadas(dici, "salvar")

    return jsonify({'htmlresponse': render_template('modalVisualizacao.html', imagem=image)})


# Desabilitar o cache para que nao interefira na exibição das visualizações
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r