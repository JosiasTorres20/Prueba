from app.DAO.database import Conexion
class MainDAO:
    def __init__(self):
        self.__conexion = None 

    def get_conexion(self):
        if self.__conexion is None:
            self.__conexion = Conexion()
        return self.__conexion

    def set_conexion(self, nueva_conexion):
        self.__conexion = nueva_conexion

    def actualizar_psw(self, usuario, nueva_psw):
        query = "UPDATE CREDENCIALES SET PSW = %s WHERE USERNAME = %s"
        self.get_conexion().ejecutar_query(query, (nueva_psw, usuario))
        self.get_conexion().desconectar()

    def validar_credenciales(self, usuario, psw):
        from app.DTO.main_dto import MainDTO
        query = """
            SELECT C.*, E.ID, E.NOMBRE, E.APELLIDO, E.TELEFONO, E.MAIL, E.ES_JEFE, E.ES_GERENTE, E.DEPTO_ID, C.PSW
            FROM CREDENCIALES C
            INNER JOIN EMPLEADO E ON C.EMPLEADO_ID = E.ID
            WHERE C.USERNAME = %s
        """
        empleados = self.get_conexion().ejecutar_query(query, (usuario,))
        
        if empleados and MainDTO.revision_del_hash(psw, empleados[0]['PSW']):
            return empleados[0] 
        return None   
    
    def saber_id_depto(self, nombre_departamento):
        query = "SELECT ID FROM DEPARTAMENTO WHERE NOMBRE = %s"
        resultado = self.get_conexion().ejecutar_query(query, (nombre_departamento,))
        
        if resultado:
            return resultado[0]['ID'] 
        else:
            return None
    def obtener_empleado_por_usuario(self, username):
        query = "SELECT E.ID, E.NOMBRE, E.APELLIDO, C.USERNAME FROM EMPLEADO E INNER JOIN CREDENCIALES C ON E.ID = C.EMPLEADO_ID WHERE C.USERNAME = %s"
        resultado = self.get_conexion().ejecutar_query(query, (username,))
        
        if resultado:
            return resultado[0] 
        return None