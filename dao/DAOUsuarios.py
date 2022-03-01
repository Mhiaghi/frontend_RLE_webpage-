import pymysql
from werkzeug.security import check_password_hash, generate_password_hash
class DAOUsuario:
    def __init__(self):
        pass

    def connection(self):
        return pymysql.connect( host="seidorvet.mysql.database.azure.com", 
                                user= "Mhiaghi@seidorvet", 
                                password= "miguel1234!",
                                database ="seidorpet",
                                ssl_ca='./BaltimoreCyberTrustRoot.crt.pem')
    def get_user_info(self, username_value):
        con = DAOUsuario.connection(self)
        cursor = con.cursor()
        try:
            consulta = "SELECT * FROM Cliente INNER JOIN usuarios using(Username) WHERE Username = '%s' " % (username_value)
            cursor.execute(consulta)
            user = cursor.fetchone()
            return user
        except:
            return("No user")
        finally:
            con.close()
    def compare_passwords_admin(self, username_value, password_value):
        user = DAOUsuario.get_admin_info(self,username_value)
        if user[2] == password_value:

            return True
        else:
            return False
    def get_admin_info(self, username_value):
        con = DAOUsuario.connection(self)
        cursor = con.cursor()
        try:
            consulta = "SELECT * FROM trabajador INNER JOIN usuarios using(Username) WHERE Username = '%s' " % (username_value)
            cursor.execute(consulta)
            user = cursor.fetchone()
            return user
        except:
            return("No user")
        finally:
            con.close()
    def compare_passwords(self, username_value, password_value):
        user = DAOUsuario.get_user_info(self,username_value)
        if check_password_hash(user[1], password_value):
            return True
        else:
            return False
    def add_users(self, username_value, password_value, email_value):
        con = DAOUsuario.connection(self)
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO usuarios(Username, Password, Email) VALUES (%s,%s,%s)', [username_value,generate_password_hash(password_value),email_value])
            con.commit()
            cur.execute('INSERT INTO Cliente(Username) VALUES (%s)', [username_value])
            con.commit()
            return("Usuario insertado con exito")
        except:
            return("Correo duplicado")
        finally:
            con.close()
    def update_user_info(self, NombreCompleto_value, Email_value, Telefono_value, Descripcion_value, Street_value, City_value, Region_value, Codigo_Postal_value, username_value):
        con = DAOUsuario.connection(self)
        cur = con.cursor()
        try:
            cur.execute("UPDATE usuarios SET NombreCompleto=%s, Email = %s, Telefono = %s, Descripcion = %s, Street =%s, City = %s, Region = %s, Codigo_Postal =%s where Username = %s", [NombreCompleto_value,Email_value,Telefono_value,Descripcion_value,Street_value,City_value,Region_value,Codigo_Postal_value,username_value])
            con.commit()
            return("Usuario actualizado con exitos")
        except:
            return("Usuario no actualizado")
        finally:
            con.close()
    def read(self,id):
            con = DAOUsuario.connection(self)
            cursor = con.cursor()

            try:
                if id == None:
                    cursor.execute("SELECT * FROM Cliente INNER JOIN usuarios using(Username) order by Username")
                    return cursor.fetchall()
                else:
                    cursor.execute("SELECT * FROM Cliente INNER JOIN usuarios using(Username) where Username = %s order by Username",(id,))
                    return cursor.fetchone()
                
            except:
                return ()
            finally:
                con.close()
    def delete(self,id):
        con = DAOUsuario.connection(self)
        cursor = con.cursor()

        try:
            cursor.execute("delete from cliente where username = %s",(id,))
            con.commit()
            cursor.execute("delete from usuarios where username = %s",(id,))
            con.commit()
            print("here")
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
    def update(self,id,nuevo_usuario, nuevo_correo):
        con = DAOUsuario.connection(self)
        cursor = con.cursor()

        try:
            print("here")
            cursor.execute("DELETE from cliente WHERE Username=%s",(id,))
            con.commit()
            cursor.execute("UPDATE usuarios SET Username=%s, Email=%s where Username = %s",(nuevo_usuario, nuevo_correo, id,))
            con.commit()
            cursor.execute("INSERT INTO cliente(Username) VALUES (%s)",[nuevo_usuario])
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    # def read_id(self,id):
    #     con = DAOUsuario.connection(self)
    #     cursor = con.cursor()

    #     try:
    #         cursor.execute("SELECT idUsuario FROM usuarios where Username = %s",(id,))
    #         return cursor.fetchall()
    #     except:
    #         return ()
    #     finally:
    #         con.close()

    # def get_user_info(self, username_value):
    #     con = DAOUsuario.connection(self)
    #     cur = con.cursor()
    #     try:
    #         cur.execute("SELECT * FROM usuarios WHERE Username = %s", (username_value,))
    #         user = cur.fetchone()
    #         return user
    #     except:
    #         return("No user")
    #     finally:
    #         con.close()	
    
    # def update_user_info(self, data):
    #     con = DAOUsuario.connection(self)
    #     cur = con.cursor()
    #     try:
    #         cur.execute("UPDATE usuarios SET NombreCompleto=%s, Email = %s, Telefono = %s, Descripcion = %s, Street =%s, City = %s, Region = %s, Codigo_Postal =%s where Username = %s", [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]])
    #         con.commit()
    #         return("Usuario actualizado con exitos")
    #     except:
    #         return("Usuario no actualizado")
    #     finally:
    #         con.close()

    # def add_users(self, username_value, password_value, email_value, type_value):
    #     con = DAOUsuario.connection(self)
    #     cur = con.cursor()
    #     try:
    #         cur.execute('INSERT INTO usuarios(Username, Password, Email, Tipo) VALUES (%s,%s,%s, %s)', [username_value,generate_password_hash(password_value),email_value, type_value])
    #         con.commit()
    #         return("Usuario insertado con exito")
    #     except:
    #         return("Correo duplicado")
    #     finally:
    #         con.close()

    # def compare_passwords(self, username_value, password_value):
    #     user = DAOUsuario.search_users(self,username_value)
    #     if check_password_hash(user[2], password_value):
    #         return True
    #     else:
    #         return False

    # def insert(self,data):
    #     con = DAOUsuario.connection(self)
    #     cursor = con.cursor()
    #     try:
    #         cursor.execute("INSERT INTO usuarios(Username, Password, Email, Tipo) VALUES(%s,%s,%s,%s)",(data['username'], generate_password_hash(data['password']), data['email'],data['tipo'],))
    #         con.commit()
    #         return True
    #     except:
    #         con.rollback()
    #         return False
    #     finally:
    #         con.close()

    # def update(self,id,data):
    #     con = DAOUsuario.connection(self)
    #     cursor = con.cursor()

    #     try:
    #         cursor.execute("UPDATE usuarios SET Username=%s, Email=%s, Tipo=%s where idUsuario = %s",(data['username'], data['email'], data['tipo'], id,))
    #         con.commit()
    #         return True
    #     except:
    #         con.rollback()
    #         return False
    #     finally:
    #         con.close()

    # def delete(self,id):
    #     con = DAOUsuario.connection(self)
    #     cursor = con.cursor()

    #     try:
    #         cursor.execute("delete from usuarios where idUsuario = %s",(id,))
    #         con.commit()
    #         return True
    #     except:
    #         con.rollback()
    #         return False
    #     finally:
    #         con.close()

    # def insert_image(self, username_value, version):
    #     con = DAOUsuario.connection(self)
    #     cur = con.cursor()
    #     try:
    #         cur.execute('UPDATE usuarios SET Imagen = %s where Username = %s', [version,username_value])
    #         con.commit()
    #         return("Se ingreso con exito la imagen")
    #     except:
    #         return("No se inserto la version")
    #     finally:
    #         con.close()

    # def get_image(self, username_value):
    #     con = DAOUsuario.connection(self)
    #     cur = con.cursor()
    #     try:
    #         cur.execute('SELECT Imagen FROM usuarios where Username = %s', [username_value])
    #         version = cur.fetchone()
    #         return version
    #     except:
    #         return 0 
    #     finally:
    #         con.close()