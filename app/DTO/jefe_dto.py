from app.DTO.empleado_dto import Empleado
class Jefe(Empleado):
    def __init__(self,id, nombre, apellido, telefono, mail, salario, fecha_inicio, depto_id, horas_trabajadas, proyecto_id):
        super().__init__(id, nombre, apellido, telefono, mail, salario, fecha_inicio, depto_id, horas_trabajadas)
        self.__proyecto_id = proyecto_id




    def __str__(self):
        txt = f"\n{super().__str__()}\n"
        txt += f"Id Proyecto: {self.__proyecto_id}"
        return txt



  