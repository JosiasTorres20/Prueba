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
    def crear_jefe(nombre_jefe,apellido_jefe,telefono_jefe):
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

        departamentos = ["RR.HH", "Finanzas", "Marketing"]
        for idx, dep in enumerate(departamentos, start=1):
            print(f"{idx}. {dep}")

        seleccion = input(f"Seleccione un departamento (1-{len(departamentos)}): ").strip()
        if seleccion.isdigit() and 1 <+ int(seleccion) <= len(departamentos):
            departamento_asignado= departamentos[int(seleccion) -1 ]['ID']
        else:
            print("Seleccione uno departamento")
            return

        query = """
        INSERT INTO EMPLEADO (NOMBRE, APELLIDO, TELEFONO, MAIL, SALARIO, FECHA_INICIO, DEPTO_ID, ES_JEFE, ES_GERENTE, USUARIO, PSW)
        VALUES (%s, %s, %s, %s, %s, %s,%s, TRUE, FALSE, %s, %s)
        """
    #manejoc de erroes como un nazi
        try:
            cursor.execute(query, (nombre_jefe, apellido_jefe, telefono_jefe, generar_mail, None, None, generar_usuario, hash_psw))
            db.commit()
            print(f"Usuario para '{nombre_jefe} {apellido_jefe}' se creo con exito y fue asignado al departmento {departamentos[int(seleccion) -1]['NOMBRE']}")
    
            usuario_jefe = Jefe(nombre_jefe,apellido_jefe,telefono_jefe, generar_mail,departamento_asignado, None, None, generar_usuario, hash_psw)
            usuario_jefe.__str__()
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
            query = "SELECT * FROM EMPLEADO WHERE NOMBRE = %s AND APELLIDO = %s AND ES_JEFE = TRUE"
            cursor.execute(query,(nombre, apellido))
        
        else:
            query = "SELECT * FROM EMPLEADO WHERE ES_JEFE = TRUE"
            cursor.execute(query)

        jefes = cursor.fetchall()
        cursor.close()
        db.close()
        return jefes