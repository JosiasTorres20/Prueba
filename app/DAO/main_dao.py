from app.DAO.database import get_db
from app.DTO import main_dto


def actualizar_psw(usuario, nueva_psw):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE EMPLEADO SET PSW = %s WHERE USUARIO = %s", (nueva_psw, usuario))
    db.commit()
    cursor.close()
    db.close()


def validar_credenciales(usuario, psw):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM EMPLEADO WHERE USUARIO = %s", (usuario,))
    empleado = cursor.fetchone()
    cursor.close()
    db.close()
    return empleado if empleado and main_dto.revision_del_hash(psw, empleado['PSW']) else None


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


def saber_id_depto(nombre_departamento):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT ID FROM DEPARTAMENTO WHERE NOMBRE = %s", (nombre_departamento,))
    departamento = cursor.fetchone()
    cursor.close()
    db.close()
    return departamento['ID'] if departamento else None



def obtener_departamentos():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM DEPARTAMENTO")  # Cambia la consulta según tu estructura de base de datos
    departamentos = cursor.fetchall()
    cursor.close()
    db.close()
    return departamentos