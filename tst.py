import bcrypt
from app.DAO.database import Conexion

contrasena = "root"
contrasena_hash = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')

db = Conexion()

departamentos = [
    (1, 'RRHH'),
    (2, 'Finanzas'),
    (3, 'Marketing')
]

for id_depto, _ in departamentos:
    eliminar_depto_query = "DELETE FROM DEPARTAMENTO WHERE ID = %s"
    db.ejecutar_query(eliminar_depto_query, (id_depto,))

for id_depto, nombre_depto in departamentos:
    insertar_depto_query = "INSERT INTO DEPARTAMENTO (ID, NOMBRE) VALUES (%s, %s)"
    db.ejecutar_query(insertar_depto_query, (id_depto, nombre_depto))
    print(f"Departamento {nombre_depto} insertado correctamente.")

verificar_email_query = "SELECT * FROM EMPLEADO WHERE MAIL = 'gerente@empresa.cl'"
resultado = db.ejecutar_query(verificar_email_query)

if resultado:
    eliminar_empleado_query = "DELETE FROM EMPLEADO WHERE MAIL = 'gerente@empresa.cl'"
    db.ejecutar_query(eliminar_empleado_query)
    print("Empleado existente borrado.")

try:
    departamento_id = 1 

    insertar_empleado_query = """
    INSERT INTO EMPLEADO (NOMBRE, APELLIDO, TELEFONO, MAIL, SALARIO, FECHA_INICIO, DEPTO_ID, ES_JEFE, ES_GERENTE)
    VALUES ('Gerente', 'General', '12345678', 'gerente@empresa.cl', 10000.00, '2024-02-26', %s, FALSE, TRUE)
    """
    db.ejecutar_query(insertar_empleado_query, (departamento_id,))
    db.guardar()

    ultimo_id_query = "SELECT ID FROM EMPLEADO WHERE MAIL = 'gerente@empresa.cl'"
    resultado_id = db.ejecutar_query(ultimo_id_query)

    if resultado_id and len(resultado_id) > 0:
        ultimo_id = resultado_id[0]['ID']
        print(f"Último ID obtenido: {ultimo_id}")

        eliminar_credenciales_query = "DELETE FROM CREDENCIALES WHERE EMPLEADO_ID = %s"
        db.ejecutar_query(eliminar_credenciales_query, (ultimo_id,))

        insertar_credenciales_query = """
        INSERT INTO CREDENCIALES (EMPLEADO_ID, USERNAME, PSW)
        VALUES (%s, 'root', %s)
        """
        db.ejecutar_query(insertar_credenciales_query, (ultimo_id, contrasena_hash))
        db.guardar()

        print("Usuario root insertado correctamente.")
    else:
        print("No se pudo obtener un ID válido del empleado.")
except Exception as e:
    print(f"Error al insertar empleado: {e}")

db.desconectar()
