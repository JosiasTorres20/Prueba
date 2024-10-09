from app.DTO.jefe_dto import Jefe
from app.DAO import main_dao
from app.DTO import main_dto
from app.DAO import usuario_dao


class Gerente(Jefe):
    def __init__(self, id, nombre,apellido,telefono,mail,salario,
                 fecha_inicio,depto_id,horas_trabajadas=0, root=False, usuario= None, psw= None):
        super().__init__(id,nombre,apellido,telefono,mail,salario,fecha_inicio,depto_id,horas_trabajadas)
        self.__root = root
    def get_root(self):
        return self.__root
    def set_root(self,root):
        self.__root = root

        
 

