from app.DAO.proyecto_dao import ProyectoDAO
from app.DTO.jefe_dto import Jefe

import datetime as date
class ProyectoDTO:
    def __init__(self):
        self.__proyecto_dao = ProyectoDAO()
        self.__jefe_dto = Jefe()


    def validar_fecha(self, fecha_contrato):
        try:
            fecha = date.strptime(fecha_contrato, f"%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    def crear_proyecto(self, nombre_proyecto, departamento_id):
        proyecto_dao = ProyectoDAO()
        proyecto_dao.crear_proyecto(nombre_proyecto, departamento_id)
        print(f"Proyecto '{nombre_proyecto}' creado en el departamento con ID {departamento_id}.")