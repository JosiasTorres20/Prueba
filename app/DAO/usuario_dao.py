from app.DAO.database import Conexion
import mysql.connector
import bcrypt
import random


# self.conectar la usaremos para establecer conexion con la BASE DE DATOS MYSQL
# self.cerrar conexion la usaremos para cerra la conexion con la BASE DE DATOS MYSQL
#self.__cursor para ejecutar varibles con QUERYS en la base de datos o ejecutar directamente las QUERYS depende lo que queramos hacer y su contexto
#self.__db.commit() para guardar los cambios

#definimos las clase UsuarioDAO. Esta clase la usaremos para interacturs con la BASE de DATOS MYSQL
class UsuarioDAO:
    def __init__(self):
        self.__conexion = None 

    def get_conexion(self):
        if self.__conexion is None:
            self.__conexion = Conexion()
        return self.__conexion
    def set_conexion(self, nueva_conexion):
        self.__conexion = nueva_conexion
    

    def buscar_valores_unicos(self, query, valor):
        while True:
            resultado = self.get_conexion().ejecutar_query(query, (valor,))
            self.get_conexion().desconectar()
            if resultado is None or len(resultado) == 0:
                break
            numero_random = random.randint(10,99)
            valor = f"{valor}{numero_random}"
        return valor
    def obtener_info(self, usuario_id):
        query = """
        SELECT E.ID, E.NOMBRE, E.APELLIDO, E.TELEFONO, E.DEPTO_ID, E.ES_JEFE, E.ES_GERENTE, E.MAIL,
               C.USERNAME, C.PSW
        FROM EMPLEADO E
        LEFT JOIN CREDENCIALES C ON E.ID = C.EMPLEADO_ID
        WHERE E.ID = %s
        """
        parametros = (usuario_id,)
        resultado = self.get_conexion().ejecutar_query(query, parametros)

        if resultado:
            return {
                'ID': resultado[0]['ID'],
                'NOMBRE': resultado[0]['NOMBRE'],
                'APELLIDO': resultado[0]['APELLIDO'],
                'TELEFONO': resultado[0]['TELEFONO'],
                'DEPTO_ID': resultado[0]['DEPTO_ID'],
                'ES_JEFE': resultado[0]['ES_JEFE'],
                'USERNAME': resultado[0]['USERNAME'],
                'MAIL': resultado[0]['MAIL'],
                'PSW': resultado[0]['PSW'],
                'ES_GERENTE': resultado[0]['ES_GERENTE']
            }
        return None
    
    def obtener_departamentos(self):
        query = "SELECT ID, NOMBRE FROM DEPARTAMENTO" 
        resultado = self.get_conexion().ejecutar_query(query)
        self.get_conexion().desconectar()
        return resultado if resultado else []
    
    #con esta funcion si un usuario exite en la base de datos 
    def verificar_usuarios_existentes(self, id):
        #aqui usamos cursor para seleccionar los campos de la tabla EMPLEADO donde el usuario coincide con el que le pasamos como varianle (usuario)
        resultado = self.get_conexion().ejecutar_query('SELECT * FROM EMPLEADO WHERE ID = %s', (id,))
        self.get_conexion().desconectar()
        return resultado #devolvemos los resultados obtenidos
    
    def generar_usuario_mail(self, nombre, apellido):
        #creamos un formato para USERNAME y Mail y lo inicializamos
        generar_mail = f"{nombre}.{apellido}@empresa.cl".lower()
        generar_usuario = f"{nombre}".lower()

        #mandamos un consulta para saber si el mail antes creado existe en la BASE DE DATO MYSQL
        generar_mail = self.buscar_valores_unicos(
            'SELECT COUNT(*) AS CONTAR FROM EMPLEADO WHERE MAIL = %s', (generar_mail,))
        return generar_usuario, generar_mail

        
    def crear_usuario(self, nombre, apellido, telefono, departamento_asignado, es_jefe=False, es_gerente=False):
        generar_usuario, generar_mail = self.generar_usuario_mail(nombre, apellido)
        if isinstance(generar_mail, tuple):
            generar_mail = generar_mail[0]
        psw = "clavetemporal" 
        hash_psw = bcrypt.hashpw(psw.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')

        query_empleado = '''
        INSERT INTO EMPLEADO (NOMBRE, APELLIDO, TELEFONO, MAIL, DEPTO_ID, ES_JEFE, ES_GERENTE)        VALUES (%s, %s, %s, %s, %s, %s, %s)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''

        valores_empleado = (nombre, apellido, telefono, generar_mail, departamento_asignado, 1 if es_jefe else 0, 1 if es_gerente else 0)

        print("Valores de la consulta:", valores_empleado) 
        try:
            conexion = self.get_conexion()
            cursor = conexion.ejecutar_query(query_empleado, valores_empleado)




            ultimo_id_registrado = cursor.lastrowid
            query_credenciales = '''
                INSERT INTO CREDENCIALES (EMPLEADO_ID, USERNAME, PSW)
                VALUES (%s, %s, %s)
            '''
            conexion.ejecutar_query(query_credenciales, (ultimo_id_registrado, generar_usuario, hash_psw))
            

        except Exception as error:
            print(f"Error - {error}")

        finally:
            # Cerrar el cursor y la conexión
            self.get_conexion().desconectar()


    #esta funcion la usaremos paera obtener un lista de los usuarios segundo las condiciones que le demos
    def ver_usuarios(self, usuario=None, depto_id=None, nombre=None, apellido=None, es_gerente=None, es_jefe=None):
        #btenemos lso datos de la tabla EMPLEADO unida con  DEPARTAMENTO
        query = """
        SELECT E.ID, E.NOMBRE, E.APELLIDO, E.TELEFONO, E.MAIL, E.ES_JEFE, E.ES_GERENTE, 
            E.DEPTO_ID, D.NOMBRE AS NOMBRE_DEPARTAMENTO, C.USERNAME AS USUARIO
        FROM EMPLEADO E
        LEFT JOIN DEPARTAMENTO D ON E.DEPTO_ID = D.ID
        LEFT JOIN CREDENCIALES C ON E.ID = C.EMPLEADO_ID
        """

        condiciones = [] #aqui metemos las condicione de la consulta 
        valores = []# aqui metemos los valoreas 

        #si buscamos jefes o empleados y vamos agregando condiciones segun el caso en cada if
        if es_jefe or es_gerente:
            #excluimos al gerente 
            condiciones.append("E.ES_GERENTE = FALSE")

        if usuario:
            condiciones.append("C.USERNAME = %s")
            valores.append(usuario)

        if depto_id is not None:
            condiciones.append("E.DEPTO_ID = %s")
            valores.append(depto_id)

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
            condiciones.append("E.ES_JEFE = %s")
            valores.append(es_jefe)

        #si hay condciones y por ende dentro de la lista la agregamos a la query
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)#aqui convertimos la lista en una cadena y la metemos dentro de la query

        usuarios = self.get_conexion().ejecutar_query(query, valores)

        self.get_conexion().desconectar()

        #esto lo usamos para que si el departamento = a None diga Sin asignar
        for usuario in usuarios:
            if usuario['NOMBRE_DEPARTAMENTO'] is None:
                usuario['NOMBRE_DEPARTAMENTO'] = 'Sin asignar'

        return usuarios #devolvemos dichos usuarios en base a los filtros que tenamos 

    def actualizar_usuario(self, id, nombre, apellido, depto_id, telefono, es_jefe, es_gerente, nuevo_usuario=None, nuevo_mail=None):
        conexion = self.get_conexion()

        campos = ['NOMBRE = %s', 'APELLIDO = %s', 'TELEFONO = %s', 'ES_JEFE = %s', 'ES_GERENTE = %s', ]
        valores = [nombre, apellido, telefono, es_jefe, es_gerente]
        
        if depto_id is not None:
            campos.append('DEPTO_ID = %s')
            valores.append(depto_id)

        valores.append(id)

        query = f'''
            UPDATE EMPLEADO
            SET {', '.join(campos)}
            WHERE ID = %s
        '''

        conexion.ejecutar_query(query, valores)

        if nuevo_usuario:
            while True:
                reviar_username_query = '''
                    SELECT COUNT(*) AS CONTAR
                    FROM CREDENCIALES
                    WHERE USERNAME = %s AND EMPLEADO_ID != %s;
                '''      
                #usamos el cursor para ejecutar la query con los valores a asignar
                usuario = conexion.ejecutar_query(reviar_username_query, (nuevo_usuario, id))
                
                if usuario[0]['CONTAR'] > 0:
                    numero_random = random.randint(10, 99)
                    nuevo_usuario = f"{nuevo_usuario}{numero_random}"
                else:
                    break

            actualizar_usario_query = '''
                UPDATE CREDENCIALES
                SET USERNAME = %s
                WHERE EMPLEADO_ID = %s;
            '''
            conexion.ejecutar_query(actualizar_usario_query, (nuevo_usuario, id))


        if nuevo_mail:
            while True:
                reviar_mail_query = '''
                    SELECT COUNT(*) AS CONTAR
                    FROM EMPLEADO
                    WHERE MAIL = %s;
                '''      
                #usamos el cursor para ejecutar la query con los valores a asignar
                mail = conexion.ejecutar_query(reviar_mail_query, (nuevo_mail,))
                
                if mail[0]['CONTAR'] > 0:
                    numero_random = random.randint(10, 99)
                    nuevo_mail = f"{nuevo_mail}{numero_random}"
                else:
                    break

            actualizar_mail_query = '''
                UPDATE EMPLEADO
                SET MAIL = %s
                WHERE ID = %s;
            '''
            conexion.ejecutar_query(actualizar_mail_query, (nuevo_mail, id))

        conexion.desconectar()

    def eliminar_usuario(self, usuario, es_jefe=False):
        query = "DELETE FROM EMPLEADO WHERE ID = (SELECT EMPLEADO_ID FROM CREDENCIALES WHERE USERNAME = %s) AND ES_JEFE = %s"
        self.get_conexion().ejecutar_query(query, (usuario, es_jefe))

        self.get_conexion().desconectar()



#mas opciones
   
    def obtener_usuarios_sin_sueldo(self):
        
        query = "SELECT * FROM EMPLEADO WHERE SALARIO IS NULL OR SALARIO = 0"
        usuarios_sin_sueldo = self.get_conexion().ejecutar_query(query)
        
        self.get_conexion().desconectar()
        return usuarios_sin_sueldo

    def obtener_usuarios_sin_contrato(self):

        query = "SELECT * FROM EMPLEADO WHERE FECHA_INICIO IS NULL"
        usuarios_sin_contrato = self.get_conexion().ejecutar_query(query)

        self.get_conexion().desconectar()
        return usuarios_sin_contrato
    
    def asignar_sueldo(self, id_usuario, nuevo_sueldo):
        query = "UPDATE EMPLEADO SET SALARIO = %s WHERE ID = %s"
        self.get_conexion().ejecutar_query(query, (nuevo_sueldo, id_usuario))

        self.get_conexion().desconectar()

    def asignar_fecha_contrato(self, id_usuario, fecha_contrato):
        query = '''UPDATE EMPLEADO
                   SET FECHA_INICIO = %s
                   WHERE ID = %s'''
        
        self.get_conexion().ejecutar_query(query, (fecha_contrato, id_usuario))
        self.get_conexion().desconectar()

    def asignar_empleado_a_proyecto(self, proyecto_id, empleado_id):
        query = "INSERT INTO ASIGNACION (PROYECTO_ID, EMPLEADO_ID) VALUES (%s, %s)"
        self.get_conexion().ejecutar_query(query, (proyecto_id, empleado_id))
        self.get_conexion().desconectar()

#mostrar datos usuario
    def __init__(self):
        self.conexion = Conexion()  # Crear una instancia de la clase Conexion

    def mostrar_usuario(self, datos_usuario):
        query = """
            SELECT * FROM empleado 
            WHERE id = %s AND nombre = %s AND apellido = %s AND depto_id = %s
        """
        params = (
            datos_usuario['ID'], 
            datos_usuario['NOMBRE'], 
            datos_usuario['APELLIDO'], 
            datos_usuario['DEPTO_ID']
        )
        # Ejecuta el query a través de la instancia de Conexion
        usuarios = self.conexion.ejecutar_query(query, params)
        return usuarios
    def cerrar_conexion(self):
        self.conexion.desconectar()