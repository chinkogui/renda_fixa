from flask import Blueprint, request, Response
from config import mongo_db
from bson.json_util import dumps

transaction_routes = Blueprint("transaction", __name__, url_prefix = "/transaction")

#Inserindo transacoes
@transaction_routes.route("insert", methods=["POST"])
def inserTransaction():
    try:
        #Pegamos os dados da requisicao e guardamos na variavel transaction
        transaction = request.get_json()
        
        #Verificamos se o Id ja existe no banco de dados
        inserted = mongo_db.transaction.find({"Id": transaction["Id"]})
        inserted = inserted.count()
        
        #Se inserted for diferente de 0, sabemos que o ID ja esta incluso
        if inserted != 0:
            #Montamos o documento de resposta
            response = {"message": "Transacao '%s' ja incluida"%(transaction["Id"])}
            return Response(dumps(response), status=400, content_type="application/json")
       
        #Se nao houver aquele Id 
        else:
            #Montamos o documento e inserimos
            mongo_db.transaction.insert_one(
                {
                    "Data": transaction["Data"],
                    "Hora": transaction["Hora"],
                    "Id": transaction["Id"],
                    "ContaInicial": transaction["ContaInicial"],
                    "ContaFinal": transaction["ContaFinal"],
                    "Valor": transaction["Valor"]
                }
            )
        
            #Respondemos que inserimos
            response = {"message": "Transacao '%s' incluida no banco de dados com sucesso!"%(transaction["Id"])}
            return Response(dumps(response), status=201, content_type="application/json")
  
    #Caso ocorra qualquer erro, retornaremos um report
    except Exception as e:
        return "Erro: %s"%(e)


#Selecionando transacoes
@transaction_routes.route("get", methods = ["GET"])
def getUsuarios():
    try:
        #Recuperamos os filtros vindo do request
        transaction = request.get_json()
        
        #Realizamos o find com os filtros
        #Data >= Data informado na requisicao
        #Hora >= Hora informado na requisicao
        #Valor >= Hora informado na requisicao
        transaction = mongo_db.transaction.find(
            {
                "Data": { "$gte": transaction["Data"] },
                "Hora": { "$gte": transaction["Hora"] },
                "Valor": { "$gte": transaction["Valor"] }
            }
        )

        #Respondendo o request
        return Response(dumps(transaction), status=200, content_type="application/json")

    except Exception as e:
        return "Erro: %s"%(e)
            
#Atualizando transacoes
@transaction_routes.route("update", methods = ["PATCH"])
def updateTransaction():
    try:
        #Recuperamos os dados do request
        transaction = request.get_json()
        #O update tera como 'condicao' o Id
        update = mongo_db.transaction.update_one(
            { "Id": transaction["Id"] },
            { "$set": transaction }
        )

        #Verificamos se algo foi atualizado
        if update.modified_count:
            response = { "message": "Transacao '%s' atualizada com sucesso"%(transaction["Id"]) }
            return Response(dumps(response), status=200, content_type="application/json")
       
        #Se a transacao foi encontrada, mas nao tem nada para modificar
        elif update.matched_count:
            response = { "message": "Transacao '%s' encontrada, mas nao foi modificada"%(transaction["Id"]) }
            return Response(dumps(response), status=400, content_type="application/json")

        #Se o Id nao foi encontrado
        else:
            response = { "message": "Transacao '%s' nao encontrada"%(transaction["Id"]) }
            return Response(dumps(response), status=404, content_type="application/json")
    
    except Exception as e:
        return "Erro: %s"%(e)

#Deletendo transacoes
@transaction_routes.route("delete", methods=["DELETE"])
def deleteTransaction():
    try:
      
        #Recuperamos os dados do request
        transaction = request.get_json()
        
        #O delete tera como 'condicao' o Id
        deleted = mongo_db.transaction.delete_one(
            { "Id": transaction["Id"] }
        )
     
        #Verificamos se algo foi deletado
        if deleted.deleted_count:
            response = { "message": "Transacao '%s' removido com sucesso"%(transaction["Id"]) }
            return Response(dumps(response), status=200, content_type="application/json")
     
        #Se a transacao nao foi removida, ela nao foi encontrada
        else:
            response = { "message": "Transacao '%s' nao encontrada"%(transaction["Id"])}
            return Response(dumps(response), status = 404, content_type="application/json")
     
    except Exception as e:
        return "Erro: %s"%(e)

