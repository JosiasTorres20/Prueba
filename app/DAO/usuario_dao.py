from app.DAO.database import get_db
import mysql.connector
import bcrypt
import random

# self.conectar la usaremos para establecer conexion con la BASE DE DATOS MYSQL
# self.cerrar conexion la usaremos para cerra la conexion con la BASE DE DATOS MYSQL
#self.__cursor para ejecutar varibles con QUERYS en la base de datos o ejecutar directamente las QUERYS depende lo que queramos hacer y su contexto
#self.__db.commit() para guardar los cambios

#definimos las clase UsuarioDAO. Esta clase la usaremos ara interacturs con la BASE de DATOS MYSQL
class UsuarioDAO:
    #Usamos el metodo construcortor para que la instanciar la clase(crear un objeto) 
    def __init__(self):
        self.__db = None #se inicie __db como None lo que quiere decir que no hay conexion con la BASE DE DATOS MYSQL
        self.__cursor = None #de la misma manera con el cursor

    #funcion antes mencionada para establecer la conexion
    def conectar(self):
        #verificamos qur la conexionn este iniciada o si no
        if self.__db is None or not self.__db.is_connected():
            self.__db = get_db() #obtenemos la conexion 
            self.__cursor = self.__db.cursor(dictionary=True) #creamos el cursor y 
                                                            #le decimos que nos devuelva los resultados como diccionario [dictionary=True]
    # funcion antes mencionada para cerra la conexion
    def cerrar_conexion(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__db and self.__db.is_connected():
            self.__db.close()
    
    
    def ver_perfil(self, usuario):
        self.conectar()
        query = """
            SELECT E.ID, E.NOMBRE, E.APELLIDO, E.TELEFONO, E.MAIL, E.USUARIO, E.ES_JEFE, E.ES_GERENTE, 
                E.DEPTO_ID, D.NOMBRE AS NOMBRE_DEPARTAMENTO
            FROM EMPLEADO E
            LEFT JOIN DEPARTAMENTO D ON E.DEPTO_ID = D.ID
                """
        self.__cursor.execute(query, (usuario,))
        info_usuario = self.__cursor.fetchone()
        self.cerrar_conexion()
        return info_usuario
    
    def obtener_departamentos(self):
        self.conectar()
        query = "SELECT ID, NOMBRE FROM DEPARTAMENTO" 
        self.__cursor.execute(query)
        resultado = self.__cursor.fetchall() 
        self.__db.commit()
        self.cerrar_conexion()
        return resultado if resultado else []
    
    #con esta funcion si un usuario exite en la base de datos 
    def verificar_usuarios_existentes(self, id):
        self.conectar()
        #aqui usamos cursor para seleccionar los campos de la tabla EMPLEADO donde el usuario coincide con el que le pasamos como varianle (usuario)
        self.__cursor.execute('SELECT * FROM EMPLEADO WHERE ID = %s', (id,))
        resultado = self.__cursor.fetchone()#obtenemos todos los campos antes seleccionados

        self.cerrar_conexion()
        return resultado #devolvemos los resultados obtenidos
    
    #esta funcion la usaremos para generar un USERNAME y un MAIL unicos
    def generar_usuario_mail(self, nombre, apellido):
        self.conectar()
        
        #creamos un formato para USERNAME y Mail y lo inicializamos
        generar_mail = f"{nombre}.{apellido}@empresa.cl".lower()
        generar_usuario = f"{nombre}".lower()

        while True:
            #mandamos un consulta para saber si el mail antes creado existe en la BASE DE DATO MYSQL
            self.__cursor.execute('SELECT COUNT(*) AS CONTAR FROM EMPLEADO WHERE MAIL = %s', (generar_mail,))
            resultado_mail = self.__cursor.fetchone()#recuperamos un resultado
            if resultado_mail['CONTAR'] == 0: #si no encontramos un correo igual salimos del bucle
                break #salimos del bucle

            #si este no exite creamos un USERNAME y MAIL con otro formato agregando un numero aleatorio de dos digitos
            numero_random = random.randint(10, 99)
            generar_mail = f"{nombre}.{apellido}{numero_random}@empresa.cl".lower()
            generar_usuario = f"{nombre}{numero_random}".lower()

        self.__db.commit()
        self.cerrar_conexion()
        #devolvemos el USERNAME y MAIL creados
        return generar_usuario, generar_mail

    #esta funcion la usaremos para que cuando actualizemos el nombre de pila del usuario el USERNAME y MAIL se actualizen en base a eso
    def actualizar_username_y_email(self, id_usuario, nuevo_username, nuevo_email):
        self.conectar()
        #con esta query actualizamos USERNAME y MAIL  en la base de datos MYSQL
        query = '''UPDATE EMPLEADO
                SET USUARIO = %s, MAIL = %s
                WHERE ID = %s'''
        
        #usamos el cursor para ejecutar la query con los valores a asignar
        self.__cursor.execute(query, (nuevo_username, nuevo_email, id_usuario))
        self.__db.commit()
        self.cerrar_conexion()

    #con esta funcion crearemos un usuario en la base de datos mysql
    def crear_usuario(self, nombre,apellido,telefono,departamento_asignado, es_jefe = False, es_gerente = False):
        self.conectar()

        #generamos el USERNAME y MAIL llamando a la funcion antes creada y le pasamos el nombre y apellido
        generar_usuario, generar_mail = self.generar_usuario_mail(nombre, apellido)
        psw = "clavetemporal" #le damos un clave temporal
        #hasheamos esta clave usando bcrypt
        hash_psw = bcrypt.hashpw(psw.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')

        #creamos un query para insertar el usuario generado en la base de datos
        query = '''
        INSERT INTO EMPLEADO (NOMBRE, APELLIDO, TELEFONO, MAIL, SALARIO, FECHA_INICIO, DEPTO_ID, ES_JEFE, ES_GERENTE, USUARIO, PSW)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        #ejecutamos esa query con los valores a asignar
        try:
            self.__cursor.execute(query, (
                nombre, apellido, telefono, generar_mail, None, None, departamento_asignado, es_jefe, es_gerente, generar_usuario, hash_psw, 
            ))
            self.__db.commit()
        except mysql.connector.Error as err:
            print(f"Error al crear usuario: {err}")
        finally:
            self.cerrar_conexion()  

    #esta funcion la usaremos paera obtener un lista de los usuarios segundo las condiciones que le demos
    def ver_usuarios(self, usuario=None, depto_id=None, nombre=None, apellido=None, es_gerente=None, es_jefe=None):
        self.conectar()

        #btenemos lso datos de la tabla EMPLEADO unida con  DEPARTAMENTO
        query = """
        SELECT E.ID, E.NOMBRE, E.APELLIDO, E.TELEFONO, E.MAIL, E.USUARIO, E.ES_JEFE, E.ES_GERENTE, 
            E.DEPTO_ID, D.NOMBRE AS NOMBRE_DEPARTAMENTO
        FROM EMPLEADO E
        LEFT JOIN DEPARTAMENTO D ON E.DEPTO_ID = D.ID
        """

        condiciones = [] #aqui metemos las condicione de la consulta 
        valores = []# aqui metemos los valoreas 

        #si buscamos jefes o empleados y vamos agregando condiciones segun el caso en cada if
        if es_jefe or es_gerente:
            #excluimos al gerente 
            condiciones.append("E.ES_GERENTE = FALSE")

        if usuario:
            condiciones.append("E.USUARIO = %s")
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

        self.__cursor.execute(query, valores)
        usuarios = self.__cursor.fetchall()
        
        self.cerrar_conexion()

        #esto lo usamos para que si el departamento = a None diga Sin asignar
        for usuario in usuarios:
            if usuario['NOMBRE_DEPARTAMENTO'] is None:
                usuario['NOMBRE_DEPARTAMENTO'] = 'Sin asignar'

        return usuarios #devolvemos dichos usuarios en base a los filtros que tenamos 

    #esta funcion la usaremos para actrualzair la informacion de un usuario existente
    def actualizar_usuario(self, id, nombre, apellido, depto_id, telefono, es_jefe, es_gerente):
        self.conectar()

        #creamos una lista con los campos a actualizar
        campos = ['NOMBRE = %s', 'APELLIDO = %s', 'TELEFONO = %s', 'ES_JEFE = %s', 'ES_GERENTE = %s']
        #aqui otra lista con las variables que contendran dichos valores
        valores = [nombre, apellido, telefono, es_jefe, es_gerente]
        #en caso de que le demos un id de departamento este lo agregaremos a los campos para evitar cambios innecesairios 
        #y evitar errores si no se proporiciona este 
        if depto_id is not None:
            campos.append('DEPTO_ID = %s')
            valores.append(depto_id)

        valores.append(id) #agregamos el ID usuario para usarlo en el WHERE ya que pertenece a la query siguiente y evitamos errores

        query = f'''
            UPDATE EMPLEADO
            SET {', '.join(campos)}
            WHERE ID = %s
        '''

        self.__cursor.execute(query, valores)
        self.__db.commit()

        if self.__cursor.rowcount == 0:
            print("El usuario ya tiene estos datos.")
        else:
            print("Actualizacion realizada.")

        self.cerrar_conexion()

    def eliminar_usuario(self, usuario, es_jefe=False):
        self.conectar()
        query = "DELETE FROM EMPLEADO WHERE USUARIO = %s AND ES_JEFE = %s"
        self.__cursor.execute(query, (usuario, es_jefe))
        self.__db.commit()

        self.cerrar_conexion()



#mas opciones
    def crear_proyecto(self, nombre, departamento_id):
        self.conectar()
        query = "INSERT INTO PROYECTO (NOMBRE, DEPARTAMENTO_ID) VALUES (%s, %s)"
        self.__cursor.execute(query, (nombre, departamento_id))
        self.__db.commit()
        proyecto_id = self.__cursor.lastrowid
        self.cerrar_conexion()
        return proyecto_id
    
    def obtener_usuarios_sin_sueldo(self):
        self.conectar()
        
        query = "SELECT * FROM EMPLEADO WHERE SALARIO IS NULL OR SALARIO = 0"
        self.__cursor.execute(query)
        usuarios_sin_sueldo = self.__cursor.fetchall()
        
        self.cerrar_conexion()
        return usuarios_sin_sueldo

    def obtener_usuarios_sin_contrato(self):
        self.conectar()

        query = "SELECT * FROM EMPLEADO WHERE FECHA_INICIO IS NULL"
        self.__cursor.execute(query)
        usuarios_sin_contrato = self.__cursor.fetchall()

        self.cerrar_conexion()
        return usuarios_sin_contrato
    
    def asignar_sueldo(self, id_usuario, nuevo_sueldo):
        self.conectar()
        query = "UPDATE EMPLEADO SET SALARIO = %s WHERE ID = %s"
        self.__cursor.execute(query, (nuevo_sueldo, id_usuario))
        self.__db.commit()
        self.cerrar_conexion()

    def asignar_fecha_contrato(self, id_usuario, fecha_contrato):
        self.conectar()
        
        query = '''UPDATE EMPLEADO
                   SET FECHA_INICIO = %s
                   WHERE ID = %s'''
        
        self.__cursor.execute(query, (fecha_contrato, id_usuario))

        self.cerrar_conexion()

    def asignar_empleado_a_proyecto(self, proyecto_id, empleado_id):
        self.conectar()
        query = "INSERT INTO ASIGNACION (PROYECTO_ID, EMPLEADO_ID) VALUES (%s, %s)"
        self.__cursor.execute(query, (proyecto_id, empleado_id))
        self.cerrar_conexion()