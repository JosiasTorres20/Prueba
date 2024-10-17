from app.DAO.database import Conexion
class ProyectoDAO:
    def __init__(self):
        self.__conexion = None 
        
    def get_conexion(self):
        if self.__conexion is None:
            self.__conexion = Conexion()
        return self.__conexion
    
    def set_conexion(self, nueva_conexion):
        self.__conexion = nueva_conexion



    def ver_proyectos_asignados(self, jefe_id):

        query = """
        SELECT P.ID, P.NOMBRE, P.DESCRIPCION, P.FECHA_INICIO, P.ESTADO
        FROM PROYECTO P
        JOIN ASIGNACION A ON P.ID = A.PROYECTO_ID
        WHERE A.JEFE_ID = %s
        """
        proyectos = self.get_conexion().ejecutar_query(query, (jefe_id,))

        self.get_conexion().desconectar()
        return proyectos


    def crear_proyecto(self, nombre_del_proyecto, departamento_id):
        query = "INSERT INTO PROYECTO (NOMBRE, DEPARTAMENTO_ID) VALUES (%s, %s)"
        cursor = self.get_conexion().ejecutar_query(query, (nombre_del_proyecto, departamento_id))
        self.get_conexion().guardar() 
        self.get_conexion().desconectar()
        


 