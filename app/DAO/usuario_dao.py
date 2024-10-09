from app.DAO.database import get_db
from app.DAO.gerente_dao import GerenteDao
import bcrypt
import random

@staticmethod
def verificar_usuarios_existentes(usuario):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute('''SELECT * FROM EMPLEADO WHERE USUARIO = %s''', (usuario,))
    resultado = cursor.fetchall()
    
    if resultado:
        print(f"Usuarios encontrados con USUARIO '{usuario}': {resultado}")
    else:
        print(f"No se encontró ningún usuario con el USUARIO '{usuario}'.")
   
@staticmethod
def generar_usuario_mail(nombre,apellido):
    db = get_db()
    cursor = db.cursor()

    generar_mail = f"{nombre}.{apellido}@empresa.cl".lower()
    generar_usuario = f"{nombre}".lower()


    while True:
        cursor.execute('SELECT COUNT(*) FROM EMPLEADO WHERE MAIL = %s', (generar_mail,))
        validar_mail = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM EMPLEADO WHERE USUARIO = %s', (generar_usuario,))
        validar_usuario = cursor.fetchone()[0]

        if validar_mail == 0 and validar_usuario == 0 :
            break
        else:
            numero_random = random.randint(10,99)
            generar_mail = f"{nombre}.{apellido}{numero_random}@empresa.cl".lower()
            generar_usuario = f"{nombre}{numero_random}".lower()
    cursor.close()
    db.close()

    return generar_usuario, generar_mail  
@staticmethod
def actualizar_username_y_email(id_usuario, nuevo_username, nuevo_email):
    db = get_db()
    cursor = db.cursor()


    query = '''UPDATE EMPLEADO
                SET USUARIO = %s, MAIL = %s
                WHERE ID = %s'''
    cursor.execute(query, (nuevo_username, nuevo_email, id_usuario))
    db.commit()
    print(f"Username y Email actualizados: Usuario: {nuevo_username}, Email: {nuevo_email}")

    cursor.close()
    db.close()    




@staticmethod
def crear_usuario(nombre,apellido,telefono,departamento_asignado, es_jefe = False, es_gerente = False):
    db = get_db()
    cursor = db.cursor()

    generar_usuario, generar_mail = GerenteDao.generar_usuario_mail(nombre,apellido)
 
    psw = "clavetemporal"
    hash_psw = bcrypt.hashpw(psw.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')

    query = '''
    INSERT INTO EMPLEADO (NOMBRE, APELLIDO, TELEFONO, MAIL, SALARIO, FECHA_INICIO, DEPTO_ID, ES_JEFE, ES_GERENTE, USUARIO, PSW)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(query, (
        nombre, apellido, telefono, generar_mail, None, None, departamento_asignado, es_jefe, es_gerente, generar_usuario, hash_psw
        ))
    db.commit()
    print(f"Usuario para '{nombre} {apellido}' se creo con exito ")
    cursor.close()
    db.close()  

@staticmethod
def ver_usuarios(nombre=None, apellido=None, es_gerente=None, es_jefe=None):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT E.ID, E.NOMBRE, E.APELLIDO, E.TELEFONO, E.MAIL, E.USUARIO, E.ES_JEFE, E.ES_GERENTE, 
               D.NOMBRE AS DEPARTAMENTO
        FROM EMPLEADO E
        LEFT JOIN DEPARTAMENTO D ON E.DEPTO_ID = D.ID
    """
    condiciones = []
    valores = []

    if nombre:
        condiciones.append("E.NOMBRE = %s")
        valores.append(nombre)

    if apellido:
        condiciones.append("E.APELLIDO = %s")
        valores.append(apellido)


    if es_gerente is not None:
        condiciones.append("E.ES_GERENTE = %s")
        valores.append(es_gerente)

   
    if es_jefe is not None:
        if es_jefe:
            condiciones.append("E.ES_JEFE = TRUE")
        else: 
            condiciones.append("E.ES_JEFE = FALSE" + " AND E.ES_GERENTE = FALSE")
    if condiciones:
        query += " WHERE " + " AND ".join(condiciones)

    cursor.execute(query, valores)
    usuarios = cursor.fetchall()
        
    usuarios = []
    
    cursor.close()
    db.close()
    return usuarios
@staticmethod
def actualizar_usuario(id_usuario, nombre, apellido, depto_id, telefono, es_jefe):
    db = get_db()
    cursor = db.cursor()

    depto_id = depto_id if depto_id is not None else None
    telefono = telefono if telefono is not None else None

    
    print(f"Actualizando en la base de datos: ID: {id_usuario}, Nombre: {nombre}, Apellido: {apellido}, Depto_ID: {depto_id}, Teléfono: {telefono}, Es_Jefe: {es_jefe}")

    query = '''UPDATE EMPLEADO
            SET NOMBRE = %s, APELLIDO = %s, DEPTO_ID = %s, TELEFONO = %s, ES_JEFE = %s
            WHERE ID = %s'''
    cursor.execute(query, (nombre, apellido, depto_id, telefono, es_jefe, id_usuario))
    db.commit()
    print(f"Filas afectadas: {cursor.rowcount}")

    if cursor.rowcount == 0:
        print("No se realizaron cambios en la base de datos (ID no encontrado o sin cambios).")
    else:
        print("Actualización realizada con éxito.")

    
    db.rollback() 
    cursor.close()
    db.close()

@staticmethod
def eliminar_usuario(usuario, es_jefe=False):
    db = get_db()
    cursor = db.cursor()

    query_eliminar = "DELETE FROM EMPLEADO WHERE USUARIO = %s"
    if es_jefe:
        query_eliminar += ' AND ES_JEFE = TRUE'

    cursor.execute(query_eliminar, (usuario,))
    db.commit()

    cursor.close()
    db.close()
