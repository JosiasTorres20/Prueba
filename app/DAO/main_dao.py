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
            SELECT ID, NOMBRE, APELLIDO, TELEFONO, MAIL, SALARIO, FECHA_INICIO, USUARIO, PSW, ES_GERENTE, ES_JEFE
            FROM EMPLEADO
            WHERE USUARIO = %s
            """
    cursor.execute(query,(usuario,))
    info_usuario = cursor.fetchone()
    cursor.close()
    db.close
    return info_usuario


def saber_id_depto(nombre_departameto):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = "SELECT ID FROM DEPARTAMENTO WHERE NOMBRE = %s"
    cursor.execute(query, (nombre_departameto, ))
    departamento = cursor.fetchone()

    cursor.close()
    db.close()

    if departamento:
        return departamento['ID']
    return None




