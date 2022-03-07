import pymysql
class DAOCarrito:
    def __init__(self):
        pass

    def connection(self):
        return pymysql.connect( host="seidorvet.mysql.database.azure.com", 
                                user= "Mhiaghi", 
                                password= "miguel1234!",
                                database ="seidorpet")
                                #ssl={'ca': '/var/www/html/BaltimoreCyberTrustRoot.crt.pem'})
                                #ssl={'ca' : r'C:\Users\migue\Documents\webpage RLE\backend-test\dao\BaltimoreCyberTrustRoot.crt.pem'})

    def read(self,username ):
        con = DAOCarrito.connection(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM carrito where Username = '%s'"%(username))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def read_cantidad(self,id_usuario,id_producto):
        con = DAOCarrito.connection(self)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT cantidad FROM carrito where username=%s AND id_producto=%s",(id_usuario, id_producto,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self,username,id_producto,cantidad):
        con = DAOCarrito.connection(self)
        cursor = con.cursor()
        try:
            consulta = "INSERT INTO carrito(Username,id_producto,cantidad) VALUES('%s','%s','%s')"%(username, id_producto, cantidad)
            cursor.execute(consulta)
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
    
    def update(self,id_usuario,id_producto, cantidad):
        con = DAOCarrito.connection(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE carrito SET cantidad=%s where Username=%s AND id_producto=%s",(cantidad, id_usuario, id_producto,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def delete(self,id_usuario,id_producto):
        con = DAOCarrito.connection(self)
        cursor = con.cursor()

        try:
            if id_producto == None:
                cursor.execute("delete from carrito where Username = %s",(id_usuario,))
                con.commit()
            else:
                cursor.execute("delete from carrito where Username = %s AND id_producto = %s",(id_usuario, id_producto,))
                con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()