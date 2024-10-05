from app.DAO.database import get_db
from app.DTO.jefe_dto import Jefe
import mysql.connector
import random
import bcrypt
class GerenteDao:
    
    @staticmethod 
    def obtener_gerente_root():
        db = get_db()
        cursor = db.cursor(dictionary = True)
        query = "SELECT * FROM EMPLEADO WHERE USUARIO = %s AND ES_GERENTE = TRUE"
        cursor.execute(query, ("root",))
        gerente_data = cursor.fetchone()
        cursor.close()
        db.close()
        return gerente_data
      


#entramos en funciones crud 
    @staticmethod
    def crear_jefe(nombre_jefe,apellido_jefe,telefono_jefe,departamento_asignado):
        #conexion y cursor
        db = get_db()
        cursor = db.cursor()

        #generar el mail y usuareio
        generar_mail = f"{nombre_jefe}.{apellido_jefe}@empresa.cl"
        generar_usuario = f"{nombre_jefe}"

        while True:

            #validamos que ambos sean unicos
            cursor.execute("SELECT COUNT(*) FROM EMPLEADO WHERE MAIL = %s", (generar_mail,))
            validar_mail = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM EMPLEADO WHERE USUARIO = %s", (generar_usuario,))
            validar_usuario = cursor.fetchone()[0]

            #si son unicos salimos del while
            if validar_mail == 0 and validar_usuario == 0 :
                break
            #si no
            else:
                numero_random = random.randint(10,99)#obtenemos un numero random de dos dijitos
                generar_mail = f"{nombre_jefe}.{apellido_jefe}{numero_random}@empresa.cl"
                generar_usuario = f"{nombre_jefe}{numero_random}"
 

        psw = "clavetemporal"
        hash_psw = bcrypt.hashpw(psw.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')

        #asignacion de departamentos 

        query = """
        INSERT INTO EMPLEADO (NOMBRE, APELLIDO, TELEFONO, MAIL, SALARIO, FECHA_INICIO, DEPTO_ID, ES_JEFE, ES_GERENTE, USUARIO, PSW)
        VALUES (%s, %s, %s, %s, %s, %s,%s, TRUE, FALSE, %s, %s)
        """
    #manejoc de erroes como un nazi
        try:
           
            cursor.execute(query, (nombre_jefe, apellido_jefe, telefono_jefe, generar_mail, None, None, departamento_asignado, generar_usuario, hash_psw))
            db.commit()
            print(f"Usuario para '{nombre_jefe} {apellido_jefe}' se creo con exito ")
    
        except mysql.connector.Error as err:
            print(f"Error al crear usuario: {err}")
        finally:
            cursor.close()
            db.close()    

        
    @staticmethod
    def actualizar_jefe(usuario, nombre, apellido, telefono,mail):
        db = get_db()
        cursor = db.cursor()

        try:

            valores_a_actualizar = []
            valores = []

            if nombre:
                valores_a_actualizar.append("NOMBRE = %s")
                valores.append(nombre)

            if apellido:
                valores_a_actualizar.append("APELLIDO = %s")            #son condicionales independientes
                valores.append(apellido)

            if telefono:
                valores_a_actualizar.append("TELEFONO = %s")
                valores.append(telefono)

            if mail:
                valores_a_actualizar.append("MAIL =%s")
                valores.append(mail)

            if not valores_a_actualizar:
                raise ValueError("No se ingresaron valores")
            

            valores.append(usuario)
            query = f"UPDATE EMPLEADO SET {', '. JOIN(valores_a_actualizar)} WHERE USUARIO = %s AND ES_JEFE = TRUE"
            cursor.execute(query, (tuple(valores)))
            db.commit()

            return cursor.rowcount > 0
        
        except Exception as e:
            print(f"Error al actualizar el usuario {str(e)}")
            return False
        
        finally:
            cursor.close()
            db.close()
        
        #aplicamos una naziada de manejor de errores 
    @staticmethod
    def mostrar_jefe(nombre = None, apellido= None):
        db = get_db()
        cursor = db.cursor(dictionary = True)

        if nombre and apellido:
            query = """
                SELECT E.ID, E.NOMBRE, E.APELLIDO, E.MAIL, E.USUARIO,E.FECHA_INICIO, E.DEPTO_ID, D.NOMBRE AS DEPARTAMENTO
                FROM EMPLEADO E
                LEFT JOIN DEPARTAMENTO D ON E.DEPTO_ID = D.ID
                WHERE E.NOMBRE = %s AND E.APELLIDO = %s AND E.ES_JEFE = TRUE
            """
            cursor.execute(query,(nombre, apellido))
        
        else:
            query = """
                SELECT E.ID, E.NOMBRE, E.APELLIDO, E.TELEFONO, E.MAIL, E.USUARIO,E.FECHA_INICIO, E.DEPTO_ID, D.NOMBRE AS DEPARTAMENTO
                FROM EMPLEADO E
                LEFT JOIN DEPARTAMENTO D ON E.DEPTO_ID = D.ID
                WHERE E.ES_JEFE = TRUE
            """
            cursor.execute(query)

        jefes = cursor.fetchall()
        cursor.close()
        db.close()
        return jefes