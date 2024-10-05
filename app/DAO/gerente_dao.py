from app.DAO.database import get_db
import mysql.connector
import random
import bcrypt


class GerenteDao:
    
    @staticmethod 
    def obtener_gerente_root():
        db = get_db()
        cursor = db.cursor(dictionary = True)
        cursor.execute('SELECT * FROM EMPLEADO WHERE USUARIO = %s AND ES_GERENTE = TRUE',('root',))
        gerente_data = cursor.fetchone()
        cursor.close()
        db.close()
        return gerente_data
      
    @staticmethod
    def crear_jefe(nombre_jefe,apellido_jefe,telefono_jefe,departamento_asignado):
        db = get_db()
        cursor = db.cursor()

        generar_mail = f"{nombre_jefe}.{apellido_jefe}@empresa.cl"
        generar_usuario = f"{nombre_jefe}"

        while True:
            cursor.execute('SELECT COUNT(*) FROM EMPLEADO WHERE MAIL = %s', (generar_mail,))
            validar_mail = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM EMPLEADO WHERE USUARIO = %s', (generar_usuario,))
            validar_usuario = cursor.fetchone()[0]

            if validar_mail == 0 and validar_usuario == 0 :
                break
            else:
                numero_random = random.randint(10,99)
                generar_mail = f"{nombre_jefe}.{apellido_jefe}{numero_random}@empresa.cl"
                generar_usuario = f"{nombre_jefe}{numero_random}"
 
        psw = "clavetemporal"
        hash_psw = bcrypt.hashpw(psw.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')

        query = '''
        INSERT INTO EMPLEADO (NOMBRE, APELLIDO, TELEFONO, MAIL, SALARIO, FECHA_INICIO, DEPTO_ID, ES_JEFE, ES_GERENTE, USUARIO, PSW)
        VALUES (%s, %s, %s, %s, %s, %s,%s, TRUE, FALSE, %s, %s)
        '''
        try:  
            cursor.execute(query, (nombre_jefe, apellido_jefe, telefono_jefe, generar_mail, None, None, departamento_asignado, generar_usuario, hash_psw))
            db.commit()
            print(f"Usuario para '{nombre_jefe} {apellido_jefe}' se creo con exito ")
        except mysql.connector.Error as error:
            print(f"Error al crear usuario: {error}")
        finally:
            cursor.close()
            db.close()    
    
    @staticmethod
    def mostrar_jefe(nombre = None, apellido= None):
        db = get_db()
        cursor = db.cursor(dictionary = True)

        if nombre and apellido:
            query = '''
                SELECT E.ID, E.NOMBRE, E.APELLIDO, E.MAIL, E.USUARIO,E.FECHA_INICIO, E.DEPTO_ID, D.NOMBRE AS DEPARTAMENTO
                FROM EMPLEADO E
                LEFT JOIN DEPARTAMENTO D ON E.DEPTO_ID = D.ID
                WHERE E.NOMBRE = %s AND E.APELLIDO = %s AND E.ES_JEFE = TRUE
            '''
            cursor.execute(query,(nombre, apellido))
        
        else:
            query = '''
                SELECT E.ID, E.NOMBRE, E.APELLIDO, E.TELEFONO, E.MAIL, E.USUARIO,E.FECHA_INICIO, E.DEPTO_ID, D.NOMBRE AS DEPARTAMENTO
                FROM EMPLEADO E
                LEFT JOIN DEPARTAMENTO D ON E.DEPTO_ID = D.ID
                WHERE E.ES_JEFE = TRUE
            '''
            cursor.execute(query)

        jefes = cursor.fetchall()
        cursor.close()
        db.close()
        return jefes
       
    @staticmethod
    def actualizar_jefe(usuario, nombre, apellido,nuevo_usuario,id_departamento,telefono,mail):
        db = get_db()
        cursor = db.cursor()

        valores_a_actualizar = []
        valores = []

        for campo, valor in [
            ("NOMBRE", nombre), 
            ("APELLIDO", apellido), 
            ("USUARIO", nuevo_usuario), 
            ("DEPTO_ID", id_departamento),
            ("TELEFONO", telefono), 
            ("MAIL", mail)
        ]:
            if valor:
                valores_a_actualizar.append(f"{campo} = %s")
                valores.append(valor)

        if not valores_a_actualizar:
            print("No se ingresaron valores")
            return False
        
            
        valores.append(usuario)
        query = f'UPDATE EMPLEADO SET {', '.join(valores_a_actualizar)} WHERE USUARIO = %s AND ES_JEFE = TRUE'
        
        
        
        try:
            cursor.execute(query, valores)
            db.commit()


            if cursor.rowcount == 0:
                print("No hay usuarios para actualizar")
                return False
            else:
                print("Usuario actualizado")
                return True
        except mysql.connector.Error as error:
            print(f"Error al actualizar el usuario: {error}")
            return False
        finally:
            cursor.close()
            db.close()
        
    @staticmethod
    def eliminar_jefe(usuario):
        db = get_db()
        cursor = db.cursor()

        query_verificadora = 'SELECT * FROM EMPLEADO WHERE USUARIO = %s AND ES_JEFE = TRUE'
        try :
            cursor.execute(query_verificadora, (usuario,))
            jefe = cursor.fetchone()

            if not jefe:
                print("No hay Usuario Jefe")
                return False
        
            query_eliminadora = 'DELETE FROM EMPLEADO WHERE USUARIO = %s AND ES_JEFE = TRUE'
            cursor.execute(query_eliminadora, (usuario, ))
            db.commit()

            if cursor.rowcount == 0:
                return False
            else:
                return True
        except mysql.connector.Error as error:
            print(f"Error al intenar eliminar el Jefe {error}")
            return None
        finally:
            cursor.close()
            db.close()

