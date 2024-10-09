from bson import ObjectId
from app.config.database import get_db

db = get_db()
coleccion_proyecto = db['Proyecto']

class Proyecto:
    def __init__(self,nombre,descripcion,fecha_inicio,fecha_fin):
        self.__id=ObjectId()
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__fecha_incio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__empleados_asignados = []

    def get_id(self):
        return self.__id
    def set_id(self, id):
        self.__id = id

    def get_nombre(self):
        return self.__nombre
    def set_nombre(self, nombre):
        self.__nombre = nombre

    def get_descripcion(self):
        return self.__descripcion
    def set_descripcion(self,descripcion):
        self.__descripcion = descripcion

    def get_fecha_inicio(self):
        return self.__fecha_incio
    def set_fecha_incio(self, fecha_inicio):
        self.__fecha_incio = fecha_inicio

    def get_fecha_fin(self):
        return self.__fecha_fin
    def set_fecha_fin(self, fecha_fin):
        self.__fecha_fin = fecha_fin


    def asignar_empleados(self,empleados_id):
        self.__empleados_asignados.append(ObjectId(empleados_id))

    def ver_empleados_asignados(self):
        return self.__empleados_asignados
    

    def ver_detalles(self):
        return {
            "ID": str(self.__id),
            "Nombre": self.__nombre,
            "Descripcion": self.__descripcion,
            "Fecha Inicio": self.__fecha_incio,
            "Fecha Termino": self.__fecha_fin,
            "Empleados": [str(emp) for emp in self.__empleados_asignados]
        }
            

    
