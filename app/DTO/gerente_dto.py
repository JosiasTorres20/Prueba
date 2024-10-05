import bcrypt
from app.DTO.jefe_dto import Jefe
from app.DAO.gerente_dao import GerenteDao

class Gerente(Jefe):
    def __init__(self, id, nombre,apellido,telefono,mail,salario,
                 fecha_inicio,depto_id,horas_trabajadas=0, root=False, usuario= None, psw= None):
        super().__init__(id,nombre,apellido,telefono,mail,salario,fecha_inicio,depto_id,horas_trabajadas)
        self.__root = root

    def get_root(self):
        return self.__root
    def set_root(self,root):
        self.__root = root

    def hash_psw(self, psw):
        return bcrypt.hashpw(psw.encode("utf-8"), bcrypt.gensalt())

    def cambiar_psw(self):
        print("Ingrese contraseña actual")
        psw_actual = input(f"\033[03;30m>>> \033[0m")
        if GerenteDao.validar_credenciales(self.__usuario, psw_actual):
            print("Ingrese la nueva contraseña")
            nueva_psw = input(f"\033[03;30m>>> \033[0m")
            nueva_psw_hash = self.hash_psw(nueva_psw)

            GerenteDao.actualizar_psw(self.__usuario, nueva_psw_hash)
            self.__psw = nueva_psw_hash

            print("Contrasena Actualiza")

        else:
            print("Contrasena actual incorrecta")

    def crear_jefe():
        nombre_jefe = input("Ingrese el nombre del jefe: ")
        apellido_jefe = input("Ingrese el apellido del jefe: ")
        telefono_jefe = input("Ingrese el teléfono del jefe: ")

        GerenteDao.crear_jefe(nombre_jefe, apellido_jefe, telefono_jefe)

    def actualizar_jefe():
        usuario_del_jefe =str(input("Ingrese "))


    def __str__(self):
        txt = f"{super().__str__()}\n"
        return txt

