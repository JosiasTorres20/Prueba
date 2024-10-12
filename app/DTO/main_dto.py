import bcrypt
import os
from app.DAO.main_dao import MainDAO
from app.DTO.usuario_dto import UsuarioDTO
class MainDTO:
    def __init__(self):
        self.__main_dao = MainDAO()
        self.__usuario_dto = UsuarioDTO()

    def limpiar():
        return os.system('cls' if os.name == 'nt' else 'clear')

    def login(self):
        print("Usuario")
        usuario = str(input("\033[03;30m>>> \033[0m"))
        intentos = 0
        while intentos < 3:
            print("Contaseña")
            psw = str(input("\033[03;30m>>> \033[0m"))
            info_usuario = self.__main_dao.validar_credenciales(usuario,psw)
            if info_usuario:
                verificar_dpto_rrhh= self.__main_dao.saber_id_depto('RRHH')
                if info_usuario['ES_JEFE'] and info_usuario['DEPTO_ID'] == verificar_dpto_rrhh:
                    resultado = self.__usuario_dto.get_departamento_asignado()
                    if resultado:
                        pendientes, total_pendiente = resultado
                        if pendientes:
                            print(f"Hay {total_pendiente} usuarios jefe sin departamento asignado ")
                    else:
                        print("No se encontraron pendientes.")
                return info_usuario
            else:
                intentos +=1
                print("Usuario o Contaseña incorrectos")
                if intentos >= 3:
                    self.bloqueo_clave(usuario)             
        return None
    
    def bloqueo_clave(self, usuario):
        print("Clave Bloqueada.\033[03;30m/se necesita reestablecerla\033[0m")
        root_psw = str(input("Ingrese clave del Gerente\n\033[03;30m>>> \033[0m"))
        if self.__main_dao.validar_credenciales("root",root_psw):
            nueva_psw = str(input("Ingrese la nueva clave\n\033[03;30m>>> \033[0m"))
            hashed_nueva_psw = bcrypt.hashpw(nueva_psw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            self.__main_dao.actualizar_psw(usuario, hashed_nueva_psw)
            print("\033[03;30mClave actualizada con exito\033[0m")
        else:
            print("Clave del Gerente incorrecta")

    def hash_claves(self, psw):
        return bcrypt.hashpw(psw.encode('utf-8'), bcrypt.gensalt())
    
    def revision_del_hash(psw, hash_claves):
        if isinstance(hash_claves, str):
            hash_claves = hash_claves.encode('utf-8')
        return bcrypt.checkpw(psw.encode('utf-8'), hash_claves)

    def cambiar_contrasena(self, usuario):
        actual_psw = input("Ingrese su contraseña actual: ")
        info_usuario = self.__main_dao.validar_credenciales(usuario, actual_psw)

        if info_usuario:
            nueva_psw = input("Ingrese la nueva contraseña: ") 
            hashed_nueva_psw = self.hash_claves(nueva_psw)
            self.__main_dao.actualizar_psw(usuario, hashed_nueva_psw)
            print("Contraseña actualizada con éxito.")
        else:
            print("Contraseña actual incorrecta. No se pudo actualizar.")




