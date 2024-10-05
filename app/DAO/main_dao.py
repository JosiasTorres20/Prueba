import mysql.connector
from app.DAO.database import get_db
from app.DTO import main_dto
import pandas as pd
import bcrypt

def actualizar_psw(usuario, nueva_psw):
    db = get_db()
    cursor = db.cursor()
    query = "UPDATE EMPLEADO SET PSW = %s WHERE USUARIO = %s"
    if isinstance(nueva_psw, bytes):
        nueva_psw = nueva_psw.decode('utf-8')
        
    cursor.execute(query, (nueva_psw, usuario))
    db.commit()
    cursor.close()
    db.close()


def validar_credenciales(usuario, psw):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM EMPLEADO WHERE USUARIO = %s"
    cursor.execute(query, (usuario,))
    empleado = cursor.fetchone()
    cursor.close()
    db.close()
    if empleado:
        if main_dto.revision_del_hash(psw, empleado['PSW']):
            return empleado
    return None
    

def ver_perfil(usuario):
    db = get_db()
    cursor = db.cursor(dictionary= True)

    query = """
            SELECT E.ID, E.NOMBRE, E.APELLIDO, E.TELEFONO, E.MAIL, E.SALARIO, E.FECHA_INICIO, E.USUARIO, E.PSW, E.ES_GERENTE, E.ES_JEFE,
                D.NOMBRE AS DEPARTAMENTO
            FROM EMPLEADO E
            LEFT JOIN DEPARTAMENTO D ON E.DEPTO_ID = D.ID
            WHERE E.USUARIO = %s
            """
    cursor.execute(query,(usuario,))
    info_usuario = cursor.fetchone()
    cursor.close()
    db.close
    return info_usuario


def saber_id_depto(nombre_departameto):
    if not nombre_departameto:
        print("Ingrese un departamento")
        return None
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT ID FROM DEPARTAMENTO WHERE NOMBRE = %s"
        cursor.execute(query, (nombre_departameto, ))
        departamento = cursor.fetchone()

        if departamento:
            return departamento['ID']
        else:
            print("No se encontro el departamento")
            return None
    except mysql.connector.Error as error:
        print(f"No se accedio a la Base de Datos: {error}")
        return None
    finally:

        cursor.close()
        db.close()



