from app.DAO.database import get_db

class ProyectoDAO:
    def __init__(self):
        self.__db = None
        self.__cursor = None

    def conectar(self):
        if self.__db is None or not self.__db.is_connected():
            self.__db = get_db()
            self.__cursor = self.__db.cursor(dictionary=True)
    def cerrar_conexion(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__db and self.__db.is_connected():
            self.__db.close()



    def ver_proyectos_asignados(self, jefe_id):
        self.conectar()

        query = """
        SELECT P.ID, P.NOMBRE, P.DESCRIPCION, P.FECHA_INICIO, P.ESTADO
        FROM PROYECTO P
        JOIN ASIGNACION A ON P.ID = A.PROYECTO_ID
        WHERE A.JEFE_ID = %s
        """
        self.__cursor.execute(query, (jefe_id,))
        proyectos = self.__cursor.fetchall()

        self.cerrar_conexion()
        return proyectos




    def crear_proyecto(self, nombre_del_proyecto, departamento_id):
        self.conectar()
        query = "INSERT INTO PROYECTO (NOMBRE, DEPARTAMENTO_ID) VALUES (%s, %s)"
        self.__cursor.execute(query, (nombre_del_proyecto, departamento_id))
        self.__db.commit() 
        self.cerrar_conexion()
        


 