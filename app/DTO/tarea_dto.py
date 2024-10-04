from bson import ObjectId
from app.config.database import get_db

db = get_db()
coleccion_tarea = db['Tareas']

class Tarea:
    def __init__(self, descripcion, empleado_id, proyecto_id, estado= 'Pendiente'):
        self.__id = ObjectId()
        self.__descripcion = descripcion
        self.__empleado_id = ObjectId(empleado_id)
        self.__proyecto_id = ObjectId(proyecto_id)
        self.__estado = estado


    @staticmethod
    def crear_tarea(data):
        tarea_id = coleccion_tarea.insert_one(data).inserted_id
        return tarea_id
    
    @staticmethod
    def obtener_por_empleado(empleado_id):
        return list(coleccion_tarea.find({"Id_empleado": ObjectId(empleado_id)}))
    
    @staticmethod
    def obtener_por_proyecto(proyecto_id):
        return list(coleccion_tarea.find({"Id_proyecto": ObjectId(proyecto_id)}))
    
    @staticmethod
    def actualizar_tarea(tarea_id,data):
        return coleccion_tarea.update_one({"ID": ObjectId(tarea_id)})
    
    @staticmethod
    def eliminar_tarea(tarea_id):
        return coleccion_tarea.delete_one({"ID": ObjectId(tarea_id)})