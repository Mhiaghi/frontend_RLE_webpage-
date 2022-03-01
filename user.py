from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from flask_cors import CORS, cross_origin

#Funciones database
from dao.DAOUsuarios import DAOUsuario
users_db = DAOUsuario()
from dao.DAOComentarios import DAOComentarios
comentarios_db = DAOComentarios()
from dao.DAOProductos import DAOProducto
productos_db = DAOProducto()
from dao.DAOCarrito import DAOCarrito
carrito_db = DAOCarrito()

##################################################################################################
#USUARIOS
##################################################################################################

bp = Blueprint('usuario', __name__, url_prefix='/usuario')
cors  = CORS(app,resources={r"/foo":{"origins":"*"}})
@bp.route('/', methods = ["GET", "POST"])
@cross_origin(origin='*',headers = ['Content-Type', 'Authorization'])
def index_page():
    if request.method == "POST":
        content = request.get_json()
        if (content["mensaje"] == "Requerir_datos"):
            datos_usuario = users_db.get_user_info(content["usuario"])
            return  jsonify(
                {"Correo_Electronico": datos_usuario[2], 
                "imagen": datos_usuario[4], 
                "Nombre_completo" : datos_usuario[5], 
                "Numero_celular" : datos_usuario[6], 
                "Descripcion" : datos_usuario[3],  
                "Calle_ubicacion" : datos_usuario[7], 
                "Ciudad" : datos_usuario[8], 
                "Region" :datos_usuario[9], 
                "Codigo_postal" : datos_usuario[10]
                })  
        elif(content["mensaje"] == "Actualizar_datos"):
            respuesta_base_de_datos = users_db.update_user_info(content["Nombre_completo"], content["Correo_Electronico"], content["Numero_Celular"], content["Descripcion"], content["Calle"], content["Ciudad"], content["Region"], content["Codigo_postal"], content["usuario"])
            if respuesta_base_de_datos == 'comentario invalido':
                return jsonify({"mensaje" : "Comentario inválido"})
            return jsonify({"mensaje" : "OK"})
        else:
            return jsonify({"mensaje": "Función equivocada"})
    else:
        return "No deberías estar aquí - Usuario"

@bp.route("/comentario", methods = ["GET", "POST"])
@cross_origin(origin='*',headers = ['Content-Type', 'Authorization'])
def user_comment_page():
    if request.method == "POST":
        content = request.get_json()
        comentarios_db.add_comments(content["usuario"], content["comentario"])
        return jsonify({"mensaje": "OK"})
    else:
        return "No es el método correcto"

@bp.route("/tienda", methods = ["GET", "POST"])
@cross_origin(origin='*',headers = ['Content-Type', 'Authorization'])
def store_page():
    if request.method == "POST":
        content = request.get_json()
        if(content["mensaje"] == "Leer_Productos"):
            data = productos_db.read(None)
            return jsonify({"mensaje": "OK", "productos": data})
        if(content["mensaje"] == "Actualizar_Productos"):
            stock = productos_db.read_stock(content["producto"])
            cantidad = carrito_db.read_cantidad(content["usuario"],content["producto"])
            if stock[0][0] >= int(content["cantidad"]):
                if cantidad == ():
                    carrito_db.insert(content["usuario"],content["producto"],content["cantidad"])
                    
                    return jsonify({"mensaje": "OK"})
                else:
                    carrito_db.update(content["usuario"], content["producto"], content["cantidad"])
                    return jsonify({"mensaje" : "OK"})
            else:
                return jsonify({"mensaje" : "No hay productos suficientes en el stock"})
        else:
            return jsonify({"mensaje": "Función no disponible"})
    else:
        return jsonify({"mensaje" : "Método no disponible"})
    


@bp.route("/carrito", methods = ["GET", "POST"])
@cross_origin(origin='*',headers = ['Content-Type', 'Authorization'])
def store_carrito():
    if request.method == "POST":
        content = request.get_json()
        if(content["mensaje"] == "leer_datos_carrito"):
            data = carrito_db.read(content['usuario'])
            nombre = []
            valor_nombre = []
            valor_precio = []
            precio_total = 0
            for i in data:
                #i[1] id_producto
                #i[2] cantidad
                valor_nombre = productos_db.read_nombre(i[1]) 
                valor_precio = productos_db.read_precio(i[1]) 
                valor_nombre = valor_nombre[0][0] #nombre producto
                valor_precio_unitario = valor_precio[0][0] #precio producto
                valor_precio = valor_precio_unitario * i[2] # precio total producto
                precio_total = precio_total +  valor_precio #precio total carro
                nombre =nombre + [[valor_nombre, i[2], valor_precio_unitario, valor_precio, i[1]]]
                #nombre-producto, cantidad, precio-producto, precio-total, id_producto
            return jsonify({"mensaje" : "OK", "data" : nombre, "precio_total" : precio_total})
        elif(content["mensaje"] == "eliminar_datos_carrito"):
            carrito_db.delete(content["usuario"],content["id_producto"])
            return jsonify({"mensaje" : "Eliminando carrito"})
        elif(content["mensaje"] == "pagar_carrito"):
            no_stock = 0
            data = carrito_db.read(content["usuario"])
            for i in data:
                stock = productos_db.read_stock(i[1])
                if i[2] > stock[0][0]:
                    no_stock = 1
            if no_stock == 0:
                for i in data:
                    productos_db.borrar_productos(i[2],i[1])
                carrito_db.delete(content["usuario"],None)
                return jsonify({"mensaje" : "OK"})
            else:
                return jsonify({"mensaje" : "No hay stock suficiente para los productos que vas a comprar"})
            return jsonify({"mensaje" : "Eliminando carrito"})
        elif(content["mensaje"] == "eliminar_carrito"):
            carrito_db.delete(content["usuario"],None)
            return jsonify({"mensaje" : "Eliminando todo el carrito"})
        else:
            return jsonify({"mensaje" : "Mensaje incorrecto"})
    else:
        return jsonify({"mensaje" : "No es el método correcto"})

