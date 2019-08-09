# renda_fixa

Desenvolvimento de endpoints para cada letra da sigla CRUD, utilizando Python, Flask e MongoDB

Raiz:

  run.py
  
    - Iniciará o flask na porta 5000 do localhost
    - Indicará ao flask a rota 'transaction' que fará parte dos endpoints
    
  config.py
  
    - Arquivo de configuração para conexão com o MongoDB

/transaction:

  blueprint.py
  
    - Arquivo de blueprint para os endpoints relacionados ao controle de transações
    - Conterá um endpoint para cada letra da sigla CRUD. Sendo os caminhos:
      * transaction/insert
      * transaction/get
      * transaction/update
      * transaction/delete
      
Requisições para exemplo:

Insert
{
    "Data": "07/08/2019",
    "Hora": "20:49:00",
    "Id": "90860",
    "ContaInicial": "6022",
    "ContaFinal": "7654",
    "Valor": 20000.00
}

Get
{
    "Data": "08/08/2019",
    "Hora": "20:00:00",
    "Valor": 1200.00
}

Update
#Atributo 'Valor' alterado
{
    "Data": "07/08/2019",
    "Hora": "20:49:00",
    "Id": "90860",
    "ContaInicial": "6022",
    "ContaFinal": "7654",
    "Valor": 10000.00
}

Delete
{
    "Id": "90860"
}
