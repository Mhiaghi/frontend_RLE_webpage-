from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_cors import CORS, cross_origin

from dao.DAOUsuarios import DAOUsuario
users_db = DAOUsuario()
from dao.DAOComentarios import DAOComentarios
comentarios_db = DAOComentarios()
from dao.DAOProductos import DAOProducto
productos_db = DAOProducto()
from dao.DAOCarrito import DAOCarrito
carrito_db = DAOCarrito()
#######################################################################################################
#ADMINISTRADORES
#######################################################################################################

bp = Blueprint('admin', __name__, url_prefix='/administrador')

@bp.route('/', methods = ["GET", "POST"])
@cross_origin(origin='*',headers = ['Content-Type', 'Authorization'])
def index_page():
    if request.method == "POST":
        content = request.get_json()
        if (content["mensaje"] == "Requerir_datos"):
            datos_usuario = users_db.get_admin_info(content["usuario"])
            return  jsonify(
                {"Correo_Electronico": datos_usuario[3], 
                "imagen": datos_usuario[5], 
                "Nombre_completo" : datos_usuario[6], 
                "Numero_celular" : datos_usuario[7], 
                "Descripcion" : datos_usuario[4],  
                "Calle_ubicacion" : datos_usuario[8], 
                "Ciudad" : datos_usuario[9], 
                "Region" :datos_usuario[10], 
                "Codigo_postal" : datos_usuario[11]
                })  
        elif(content["mensaje"] == "Actualizar_datos"):
            respuesta_base_de_datos = users_db.update_user_info(content["Nombre_completo"], content["Correo_Electronico"], content["Numero_Celular"], content["Descripcion"], content["Calle"], content["Ciudad"], content["Region"], content["Codigo_postal"], content["usuario"])
            if respuesta_base_de_datos == 'comentario invalido':
                return jsonify({"mensaje" : "Comentario inválido"})
            return jsonify({"mensaje" : "OK"})
        else:
            return jsonify({"mensaje": "Función equivocada"})
    else:
        return "No deberías estar aquí - Admin"

@bp.route('/ingreso', methods = ["GET", "POST"])
@cross_origin(origin='*',headers = ['Content-Type', 'Authorization'])
def ingreso_admin():
    if request.method == "POST":
        content = request.get_json()
        username_value = content["username"]
        password_value = content["password"]
        error = None
        #Empieza la conexion a la base de datos
        user = users_db.get_admin_info(username_value)
        error = None
        if user == "No user":
            error = "Usuario incorrecto"
        elif not users_db.compare_passwords_admin(username_value, password_value):
            error = 'Contraseña incorrecta'
        if error is None:
            session.clear()
            session['user_id'] = user[1]
            #Termina
            return jsonify({"mensaje": "OK"})
        print(error)
        return jsonify({"mensaje": error})
    else:
        return "No se recibió el método POST"
    return jsonify({"mensaje": "Sin enviar"})

@bp.route('/manejar_usuarios', methods = ["GET", "POST"])
@cross_origin(origin='*',headers = ['Content-Type', 'Authorization'])
def admin_account():
    if request.method == "POST":
        content = request.get_json()
        if (content["mensaje"] == "leer_usuarios"):
            data = users_db.read(None)
            return jsonify({"mensaje": "OK", "data" : data})
        elif (content["mensaje"] == "eliminar_usuarios"):
            users_db.delete(content["usuario"])
            print("Se elimina: ", content["usuario"])
            return jsonify({"mensaje" : "OK"})
        elif (content["mensaje"] == "actualizar_usuarios_request"):
            data = users_db.read(content["usuario"])
            return jsonify({"mensaje" : "OK", "email" : data[2]})
        elif (content["mensaje"] == "actualizar_usuarios"):
            users_db.update(content["usuario"], content["nuevo_usuario"], content["correo"])

            return jsonify({"mensaje" : "OK"})

    else:
        return jsonify({"mensaje" : "F"})
@bp.route('/manejar_comentarios', methods = ["GET", "POST"])
@cross_origin(origin='*',headers = ['Content-Type', 'Authorization'])
def admin_comment():
    if request.method == "POST":
        content = request.get_json()
        if (content["mensaje"] == "leer_comentarios"):
            data = comentarios_db.read(None)
            return jsonify({"mensaje": "OK", "data" : data})
        elif (content["mensaje"] == "eliminar_comentarios"):
            comentarios_db.delete(content["comentario"])
            return jsonify({"mensaje" : "OK"})
    else:
        return jsonify({"mensaje" : "F"})
@bp.route('/manejar_productos', methods = ["GET", "POST"])
@cross_origin(origin='*',headers = ['Content-Type', 'Authorization'])
def admin_products():
    if request.method == "POST":
        content = request.get_json()
        if (content["mensaje"] == "leer_productos"):
            data = productos_db.read(None)
            return jsonify({"mensaje": "OK", "data" : data})
        elif (content["mensaje"] == "eliminar_productos"):
            productos_db.delete(content["producto"])
            return jsonify({"mensaje" : "OK"})
        elif (content["mensaje"] == "nuevo_producto"):
            productos_db.insert(content["nombre"], content["imagen"], content["precio"], content["stock"], content["disponible"])
            return jsonify({"mensaje": "OK"})
        elif (content["mensaje"] == "actualizar_productos_request"):
            data = productos_db.read(content["producto"])
            return jsonify({"mensaje" : "OK", "nombre" : data[1], "imagen": data[2], "precio": data[3], "stock":data[4], "disponible":data[5]})
        elif (content["mensaje"] == "actualizar_productos"):
            productos_db.update(content["nombre"], content["imagen"], content["precio"], content["stock"], content["disponible"], content["id_producto"])
            return jsonify({"mensaje" : "OK"})
    else:
        return jsonify({"mensaje" : "F"})

# @bp.route('/admin_account/add')
# @login_admin_required
# def admin_account_add():
#     return render_template("es/admin/users_managment/admin_account_add.html")

# @bp.route('/admin_account/add_acc', methods=['POST','GET'])
# @login_admin_required
# def admin_account_add_acc():
#     if request.method == 'POST' and request.form['save']:
#         users_db.insert(request.form)
#     return redirect(url_for("admin_admin_account"))

# @bp.route('/admin_account/update/<int:id>')
# @login_admin_required
# def admin_account_update(id):
#     data = users_db.read(id)
#     if len(data) == 0:
#         return redirect(url_for('admin_admin_account'))
#     else:
#         session['update'] = id
#         return render_template('es/admin/users_managment/admin_account_update.html', data=data)

# @bp.route('/admin_account/update_acc', methods=['POST','GET'])
# @login_admin_required
# def admin_account_update_acc():
#     if request.method == 'POST' and request.form['update']:
#         users_db.update(session['update'],request.form)
#         session.pop('update',None)
#         return redirect(url_for('admin_admin_account'))

# @bp.route('/admin_account/delete/<int:id>/')
# @login_admin_required
# def admin_account_delete(id):
#     data = users_db.read(id)
#     if len(data) == 0:
#         return redirect(url_for('admin_admin_account'))
#     else:
#         session['delete'] = id
#         return render_template('es/admin/users_managment/admin_account_delete.html', data=data)

# @bp.route('/admin_account/delete_acc',methods=['POST'])
# @login_admin_required
# def admin_account_delete_acc():
#     if request.method == 'POST' and request.form['delete']:
#         users_db.delete(session['delete'])
#         session.pop('delete',None)
#         return redirect(url_for('admin_admin_account'))

# #*********************Productos CRUD**********************************

# @bp.route('/productos')
# @login_admin_required
# def productos():
#     data = productos_db.read(None)
#     return render_template("es/admin/products_managment/productos.html", data = data)

# @bp.route('/productos/add')
# @login_admin_required
# def productos_add():
#     return render_template("es/admin/products_managment/productos_add.html")

# @bp.route('/productos/add_producto', methods=['POST','GET'])
# @login_admin_required
# def productos_add_producto():
#     if request.method == 'POST' and request.form['save']:
#         productos_db.insert(request.form)
#     return redirect(url_for("admin_productos"))

# @bp.route('/productos/update/<int:id>')
# @login_admin_required
# def productos_update(id):
#     data = productos_db.read(id)
#     if len(data) == 0:
#         return redirect(url_for('admin_productos'))
#     else:
#         session['update'] = id
#         return render_template('es/admin/products_managment/productos_update.html', data=data)

# @bp.route('/productos/update_producto', methods=['POST','GET'])
# @login_admin_required
# def productos_update_producto():
#     if request.method == 'POST' and request.form['update']:
#         productos_db.update(session['update'],request.form)
#         session.pop('update',None)
#         return redirect(url_for('admin_productos'))

# @bp.route('/productos/delete/<int:id>/')
# @login_admin_required
# def productos_delete(id):
#     data = productos_db.read(id)
#     if len(data) == 0:
#         return redirect(url_for('admin_productos'))
#     else:
#         session['delete'] = id
#         return render_template('es/admin/products_managment/productos_delete.html', data=data)

# @bp.route('/productos/delete_producto',methods=['POST'])
# @login_admin_required
# def productos_delete_producto():
#     if request.method == 'POST' and request.form['delete']:
#         productos_db.delete(session['delete'])
#         session.pop('delete',None)
#         return redirect(url_for('admin_productos'))

# #*********************Commentarios CRUD**********************************

# @bp.route('/comments_manage')
# @login_admin_required
# def comments_manage():
#     data = comentarios_db.read(None)
#     return render_template("es/admin/comments_managment/comments_manage.html", data = data)

# @bp.route('/comments_manage/delete/<int:id>')
# @login_admin_required
# def comments_manage_delete(id):
#     data = comentarios_db.read(id)
#     if len(data) == 0:
#         return redirect(url_for('admin_comments_manage'))
#     else:
#         session['delete'] = id
#         return render_template('es/admin/comments_managment/comments_manage_delete.html', data=data)

# @bp.route('/comments_manage/delete_comment',methods=['POST'])
# @login_admin_required
# def comments_manage_delete_acc():
#     if request.method == 'POST' and request.form['delete']:
#         comentarios_db.delete(session['delete'])
#         session.pop('delete',None)
#         return redirect(url_for('admin_comments_manage'))
# #############################################################################