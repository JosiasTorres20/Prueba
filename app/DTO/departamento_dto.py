from bson import ObjectId
from app.DAO.database import get_db

db = get_db()
coleccion_departamento = db['Departamentos']


class Departamento:
    def __init__(self, nombre):
        self.__id = ObjectId()
        self.__nombre = nombre
        self.__jefe_id = None
        self.__empleados = []

    def asignar_jefe(self, jefe_id):
        self.__jefe_id = ObjectId(jefe_id)


    def asignar_empleado(self,empleado_id):
        if empleado_id not in self.__empleados:
            self.__empleados.append(ObjectId(empleado_id))


    def detalles(self):
        return {
            "ID": str(self.__id),
            "Nombre": self.__nombre,
            "Id Jefe": str(self.__jefe_id) if self.__jefe_id else None,
            "Empleado": [str(emp) for emp in self.__empleados]
        }
    
    @staticmethod
    def crear(data):
        departamento_id = coleccion_departamento.inserte_one(data).inserted_id
        return departamento_id
    
    @staticmethod
    def obtener_por_id(departamento_id):
        return coleccion_departamento.find_one({"ID": ObjectId(departamento_id)})

    @staticmethod
    def actualizar(departamento_id, data):
        return coleccion_departamento.update_one({"ID": ObjectId(departamento_id)})