import pymysql
class DAOComentarios:
    def __init__(self):
        pass
    def connection(self):
        return pymysql.connect( host="seidorvet.mysql.database.azure.com", 
                                user= "Mhiaghi@seidorvet", 
                                password= "miguel1234!",
                                database ="seidorpet",
                                ssl_ca='/var/www/html/DigiCertGlobalRootCA.crt.pem')

    def search_our_comments(self, username_value):
        con = DAOComentarios.connection(self)
        cur = con.cursor()
        cur.execute("SELECT * FROM comentarios WHERE Username = %s", (username_value,))
        try:
            return cur.fetchall()
        except:
            return()
        finally:
            con.close()
    def add_comments(self, username_value,comment_value):
        con = DAOComentarios.connection(self)
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO comentarios(Username, Comment) VALUES (%s,%s)', [username_value, comment_value])
            con.commit()
            return 'comentario exitoso'
        except:
            return 'comentario invalido'
        finally:
            con.close()
    def search_all_comments(self):
        con = DAOComentarios.connection(self)
        cur = con.cursor()
        cur.execute("SELECT * FROM comentarios")
        try:
            #print(cur.fetchall())
            return cur.fetchall()
        except:
            return()
        finally:
            con.close()

    def read(self,id):
        con = DAOComentarios.connection(self)
        cursor = con.cursor()
        try:
            if id == None:
                cursor.execute("SELECT * FROM comentarios order by Username")
            else:
                cursor.execute("SELECT * FROM comentarios where idComment = %s order by Username",(id,))
            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()


    def update(self,id,data):
        con = DAOComentarios.connection(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE comentarios SET Comment=%s where idComment = %s",( data['comment'], id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()

    def delete(self,id):
        con = DAOComentarios.connection(self)
        cursor = con.cursor()

        try:
            cursor.execute("delete from comentarios where idComment = %s",(id,))
            con.commit()
            return True
        except:
            con.rollback()
            return False
        finally:
            con.close()
