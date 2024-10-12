from app.DAO.database import get_db
class MainDAO:
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

    def actualizar_psw(self, usuario, nueva_psw):
        self.conectar()
        self.__cursor.execute("UPDATE EMPLEADO SET PSW = %s WHERE USUARIO = %s", (nueva_psw, usuario))
        self.__db.commit()

        self.cerrar_conexion()

    def validar_credenciales(self, usuario, psw):
        from app.DTO.main_dto import MainDTO
        self.conectar()
        self.__cursor.execute("SELECT * FROM EMPLEADO WHERE USUARIO = %s", (usuario,))
        empleado = self.__cursor.fetchone()


        if empleado and MainDTO.revision_del_hash(psw, empleado['PSW']):
            return empleado
        
        self.cerrar_conexion()
        return None
    
    def saber_id_depto(self, nombre_departamento):
        self.conectar()
        
        self.__cursor.execute("SELECT ID FROM DEPARTAMENTO WHERE LOWER (NOMBRE) = %s", (nombre_departamento,))
        departamento = self.__cursor.fetchone()


        self.cerrar_conexion()
        return departamento['ID'] if departamento else None



