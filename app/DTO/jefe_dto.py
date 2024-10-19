from app.DTO.usuario_dto import UsuarioDTO
from app.DTO.usuario_dto import UsuarioDTO

from app.DAO.usuario_dao import UsuarioDAO
from datetime import datetime as date

class Jefe(UsuarioDTO):
    def __init__(self, id=None, nombre=None, apellido=None, telefono=None, mail=None, usuario=None, psw=None, departamento_asignado=None):
        super().__init__(id, nombre, apellido, telefono, mail, usuario, psw, departamento_asignado, es_jefe=True) 
        self.__usuario_dao = UsuarioDAO()



    def validar_fecha(self, fecha_contrato):
        try:
            fecha = date.strptime(fecha_contrato, f"%Y-%m-%d")
            return True
        except ValueError:
            return False
    def notificaciones_rrhh(self):
        usuarios_pendientes = self.__usuario_dao.obtener_usuarios_sin_contrato()
        if usuarios_pendientes:
            print(f"Usuarios con fecha de inicio de contrato pendiente({len(usuarios_pendientes)})")
            for idx, usuario in enumerate(usuarios_pendientes, start=1):
                print(f"{idx}. {usuario['NOMBRE']} {usuario['APELLIDO']} - {usuario['USUARIO']}")

            seleccion = input("Seleccione un usuario para agregar fecha de inicio\033[03;30m(0 para salir)\033[0m: ")
            if seleccion.isdigit() and 1 <= int(seleccion) <= len(usuarios_pendientes):
                usuario_seleccionado = usuarios_pendientes[int(seleccion) - 1]
                while True:
                    fecha_contrato = input(f"Ingrese la fecha de contrato {usuario_seleccionado['NOMBRE']} {usuario_seleccionado['APELLIDO']} (YYYY-MM-DD): ")
                        
                    if self.validar_fecha(fecha_contrato):
                        self.__usuario_dao.asignar_fecha_contrato(usuario_seleccionado['ID'], fecha_contrato)
                        print("Fecha asignada con exito.")
                        break 
                    else:
                        print("Ingrese una fecha correcta")
            elif seleccion == 0:
                return None
        else:
            print("No hay usuarios pendientes de contrato.")


    def notificaciones_finanzas(self):
        usuarios_sin_sueldo = self.__usuario_dao.obtener_usuarios_sin_sueldo()
        if usuarios_sin_sueldo:
            print(f"Usuarios pendientes de asignacion de sueldo: {len(usuarios_sin_sueldo)}")

            for indice, usuario in enumerate(usuarios_sin_sueldo, start=1):
                print(f"{indice}. {usuario['USUARIO']}: {usuario['NOMBRE']} {usuario['APELLIDO']} ")
            
            seleccion = int(input("Seleccione el usuario para asignar sueldo\033[03;30m(0 para salir)\033[0m"))
            if seleccion > 0 and seleccion <= len(usuarios_sin_sueldo):
                nuevo_sueldo = float(input("Ingrese el nuevo sueldo: "))
                usuario_seleccionado = usuarios_sin_sueldo[seleccion - 1]
                self.__usuario_dao.asignar_sueldo(usuario_seleccionado['ID'], nuevo_sueldo)
                print(f"Sueldo de {usuario_seleccionado['NOMBRE']} {usuario_seleccionado['APELLIDO']} actualizado a {nuevo_sueldo}.")
            elif seleccion == 0:
                return None
            else:
                print(f"Seleccione un usuario" )
        else:
            print("No hay usuarios pendientes para asignacion de sueldo.")




