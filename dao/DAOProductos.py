import pymysql
from werkzeug.security import check_password_hash, generate_password_hash
class DAOProducto:
    def __init__(self):
        pass

    def connection(self):
        return pymysql.connect( host="seidorvet.mysql.database.azure.com", 
                                user= "Mhiaghi", 
                                password= "miguel1234!",
                                database ="seidorpet")
                                #ssl={'ca': '/var/www/html/BaltimoreCyberTrustRoot.crt.pem'})
                                #ssl={'ca' : r'C:\Users\migue\Documents\webpage RLE\backend-test\dao\BaltimoreCyberTrustRoot.crt.pem'})


    def read(self,id):
        con = DAOProducto.connection(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM productos order by nombre")
                return cursor.fetchall()
            else:
                cursor.execute("SELECT * FROM productos where id = %s order by nombre",(id,))
                return cursor.fetchone()
        except:
            return ()
        finally:
            con.close()

    def insert(self,nombre, imagen, precio, stock, disponible):
        con = DAOProducto.connection(self)
        print("here2")
        cursor = con.cursor()
        try:
            cursor.execute("INSERT INTO productos(nombre, imagen, precio, stock, disponible) VALUES(%s,%s,%s,%s,%s)",(nombre, imagen, precio, stock,disponible,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def update(self,nombre, imagen, precio, stock, disponible, id):
        con = DAOProducto.connection(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE productos SET nombre=%s, imagen=%s, precio=%s, stock=%s, disponible=%s where id = %s",(nombre, imagen, precio, stock, disponible,id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def delete(self,id):
        con = DAOProducto.connection(self)
        cursor = con.cursor()

        try:
            cursor.execute("delete from productos where id = %s",(id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def read_nombre(self,id):
        con = DAOProducto.connection(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT nombre FROM productos")
            else:
                cursor.execute("SELECT nombre FROM productos where id = %s",(id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def read_precio(self,id):
        con = DAOProducto.connection(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT nombre FROM productos")
            else:
                cursor.execute("SELECT precio FROM productos where id = %s",(id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def read_stock(self,id):
        con = DAOProducto.connection(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT stock FROM productos")
            else:
                cursor.execute("SELECT stock FROM productos where id = %s",(id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def borrar_productos(self,cantidad,id):
        con = DAOProducto.connection(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE productos SET stock=stock-%s where id = %s",(cantidad, id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()