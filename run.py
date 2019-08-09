#!/usr/bin/env python3

from flask import Flask, Response
import json

from transaction.blueprint import transaction_routes

app = Flask(__name__)
app.register_blueprint(transaction_routes)

@app.route("/")
def index():
    retorno = {
        "app": "Sistema de controle de transacoes",
        "version": 1.0
    }
    return Response(
        json.dumps(retorno),
        200,
        content_type = "application/json"
    )

if __name__ == "__main__":
    app.run(debug = True)
