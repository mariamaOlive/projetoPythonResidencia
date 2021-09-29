# Projeto Python - Residência de Dados

## Sobre o projeto
**Este projeto faz parte da disciplina Introdução a Python da Residência de Engenharia e Ciência de Dados - UFPE**

Nesse projeto desenvolvemos um sistema CRUD de um sistema de operadora de celualr pré-pago.

Funcionalidades do sistema:
* Adicionar cliente
* Deletar cliente
* Buscar cliente por CPF
* Adicionar saldo
* Adicionar chamadas
* Apresentar quatro tipos diferentes de visualização

Todas funcionalidade salvam em tempo real um arquivo de leitura e escrita (default: listaClientes.txt)

## Construido com
* Python 
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Bootstrap 4](https://getbootstrap.com/docs/4.0/)


## Configurando o projeto
Você pode configurar o ambiente do programa via pip instalando as bibliotecas a seguir

### Instalação

Bibliotecas separadas via conda ou pip:
1. Via conda:
    ```sh
    conda install matplotlib
    ```
    ```sh
    conda install numpy
    ```
    ```sh
    conda install flask
    ```
    ```sh
    pip install bootstrap-4
    ```

2. Via pip:
    ```sh
    pip install matplotlib
    ```
    ```sh
    pip install numpy
    ```
    ```sh
    pip install flask
    ```
    ```sh
    pip install bootstrap-4
    ```

### Executando o programa
O arquivo `projetoPython.py` deve ser executado via Flask a partir dos seguintes passos:

1. No diretório do projeto execute os seguites comandos:

    Usuário Mac:
     ```sh
    export FLASK_APP=projetoPython.py
    ```
    ```sh
    flask run
    ```

    Usuário Windows no cmd:
     ```sh
    set FLASK_APP=projetoPython
    ```
    ```sh
    flask run
    ```

    Usuário Windows no PowerShell:
     ```sh
    $env:FLASK_APP = "projetoPython"
    ```
    ```sh
    flask run
    ```

2. Abra em seu browswer o endereço apresentado no terminal (default: `http://127.0.0.1:5000/`)

3. Pronto!


