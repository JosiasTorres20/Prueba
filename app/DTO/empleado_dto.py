from app.DTO.persona_dto import Persona


class Empleado(Persona):
    def __init__(self,id,nombre,apellido,telefono,mail,salario,fecha_inicio,depto_id,horas_trabajadas = 0):
        super().__init__(id,nombre,apellido,telefono,mail)
        self.__salario = salario
        self.__fecha_inicio = fecha_inicio
        self.__depto_id = depto_id
        self.__horas_trabajadas = horas_trabajadas
        self.__proyecto_id = None

    def ver_perfil(self):
        return {
            "Nombre Completo": f"{self.get_nombre()} {self.get_apellido()}",
            "Telefono": self.get_telefono(),
            "Mail": self.get_mail,
            "Salario": self.__salario(),
            "Fecha Incio de Contrado": self.__fecha_inicio,
            "Id Departamento": self.__depto_id
        }
    
    def get_salario(self):
        return self.__salario
    def set_salario(self,salario):
        self.__salario = salario

    def get_fecha_incio(self):
        return self.__fecha_inicio
    def set_fecha_incio(self, fecha_inicio):
        self.__fecha_inicio = fecha_inicio
    
    def get_depto_id(self):
        return self.__depto_id
    def set_depto_id(self, depto_id):
        self.__depto_id = depto_id

    def get_horas_trabajadas(self):
        return self.__horas_trabajadas
    def set_horas_trabajadas(self, horas_trabajadas):
        self.__horas_trabajadas = horas_trabajadas



    def __str__(self):
        txt = f"\n{super().__str__()}"
        txt+= f"Salario = {self.__salario}/n"
        txt+= f"Incio de Contrato = {self.__fecha_inicio}\n"
        txt += f"Id Departamento = {self.__depto_id}\n"
        txt += f"Horas Trabajadas = {self.__horas_trabajadas}"