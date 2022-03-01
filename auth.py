from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_cors import CORS, cross_origin
import json


#Funciones database
from dao.DAOUsuarios import DAOUsuario
users_db = DAOUsuario()

##################################################################################################
#Login-Registro
##################################################################################################

bp = Blueprint('auth', __name__, url_prefix='/autenticacion/')
cors  = CORS(app,resources={r"/foo":{"origins":"*"}})
@bp.route('/ingreso', methods = ["GET", "POST"])
@cross_origin(origin='*',headers = ['Content-Type', 'Authorization'])
def login_page():
    if request.method == "POST":
        content = request.get_json()
        username_value = content["username"]
        password_value = content["password"]
        error = None
        #Empieza la conexion a la base de datos
        user = users_db.get_user_info(username_value)
        error = None
        if user == "No user":
            error = "Usuario incorrecto"
        elif not users_db.compare_passwords(username_value, password_value):
            error = 'Contraseña incorrecta'
        if error is None:
            session.clear()
            session['user_id'] = user[1]
            #Termina
            return jsonify({"mensaje": "OK"})
        return jsonify({"mensaje": error})
    else:
        return "No se recibió el método POST"
    return jsonify({"mensaje": "Sin enviar"})
@bp.route('/registro', methods = ["GET", "POST"])
@cross_origin(origin='*',headers = ['Content-Type', 'Authorization'])
def register_page():
    if request.method == "POST":
        content = request.get_json()
        username_value = content["username"]
        password_value = content["password"]
        email_value = content["email"]
        error = None
        if not username_value:
            error = "Usuario es requerido"
        elif not password_value:
            error = "Contraseña es requerida"
        elif not (users_db.get_user_info(username_value) == "No user" ) | (users_db.get_user_info(username_value) is None):
            error = "El usuario " + username_value + " se encuentra registrado"
        #Empieza la conexion a la base de datos
        if error is None:
            resultado = users_db.add_users(username_value, password_value, email_value)
            #Termina
            if (resultado == "Correo duplicado"):
                error = "El correo se encuentra registrado"
                return jsonify({"mensaje": error})
            else:
                return jsonify({"mensaje": "OK"})
        return jsonify({"mensaje": error})
    else:
        return jsonify ({"mensaje": "No se envio un post GG"})
    return jsonify({"mensaje":"Sin enviar"})

