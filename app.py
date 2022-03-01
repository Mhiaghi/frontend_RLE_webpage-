
from flask import Flask, render_template, redirect, url_for, flash, request, session, g, jsonify
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)

@app.route("/")
def index_page():
    return "No deberia estar aqui"

@app.route("/sobre-nosotros", methods = ["GET", "POST"])
def sobre_nosotros_pagina():
    return jsonify(name_webpage = "Sobre Nosotros")

@app.route('/comentarios', methods = ["GET", "POST"])
@cross_origin(origin='*',headers = ['Content-Type', 'Authorization'])
def comment_page():
    comentarios = comentarios_db.search_all_comments()
    if request.method == "POST":
        archivo_json = json.dumps(comentarios)
        return archivo_json
    else:
        return "No es el metodo adecuado"

if __name__ == '__main__':
    app.run()