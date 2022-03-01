#Librerias
from flask import Flask, render_template, redirect, url_for, flash, request, session, g, jsonify
from flask_cors import CORS, cross_origin
import json
######################################################
# Database

from dao.DAOComentarios import DAOComentarios
from dao.DAOUsuarios import DAOUsuario

######################################################
# Configuracion
from config import DevelopmentConfig
#######################################################
#Clases database

comentarios_db = DAOComentarios()
users_db = DAOUsuario()
######################################################
#Blueprints

import auth
import user
import admin
######################################################

app = Flask(__name__)
cors  = CORS(app,resources={r"/foo":{"origins":"*"}})
app.config.from_object(DevelopmentConfig)

app.register_blueprint(auth.bp)
app.register_blueprint(user.bp)
app.register_blueprint(admin.bp)

######################################################
@app.route("/")
def index_page():
    return "No deberia estar aqui"

@app.route("/sobre-nosotros", methods = ["GET", "POST"])
def sobre_nosotros_pagina():
    return jsonify(name_webpage = "Sobre Nosotros")

@app.route('/comentarios', methods = ["GET", "POST"])
@cross_origin(origin='*',headers = ['Content-Type', 'Authorization'])
def comment_page():
    
    if request.method == "POST":
        comentarios = comentarios_db.search_all_comments()
        archivo_json = json.dumps(comentarios)
        return archivo_json
    else:
        return "No es el metodo adecuado"

if __name__ == '__main__':
    app.run()