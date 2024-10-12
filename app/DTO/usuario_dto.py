
from app.DAO.main_dao import MainDAO
from app.DAO.usuario_dao import UsuarioDAO
from app.DTO.persona_dto import Persona
from app.DAO.proyecto_dao import ProyectoDAO
import pandas as pd
class UsuarioDTO(Persona):
    def __init__(self, id=None, nombre=None, apellido=None, telefono=None, mail=None, usuario=None, psw=None, departamento_asignado=None, es_jefe=False):
        super().__init__(nombre, apellido, telefono, mail, usuario,psw)
        self.__id = id
        self.__departamento_asignado = departamento_asignado
        self.__es_jefe = es_jefe
        self.__usuario_dao = UsuarioDAO()
        self.__main_dao = MainDAO()
        self.__proyecto_dao = ProyectoDAO()

    def get_departamento_asignado(self):
        return self.__departamento_asignado
    def set_departamento_asignado(self, departamento_asignado):
        self.__departamento_asignado = departamento_asignado

    def get_es_jefe(self):
        return self.__es_jefe
    def set_es_jefe(self, es_jefe):
        self.__es_jefe = es_jefe


#creacion de usuarios
    def menu_crear_usuario(self):
        tipos = ["Empleado", "Jefe"]
        for idx, tipo in enumerate(tipos, start=1):
            print(f"{idx}. {tipo}")

        seleccion = int(input(f"Que tipo de Usuario desea crear (1-{len(tipos)})\n\033[03;30m>>> \033[0m"))
        
        if seleccion == 1:
            UsuarioDTO().crear_jefe()
        elif seleccion == 2:
            UsuarioDTO().crear_empleado()
        else:
            print("Seleccione un tipo de Usuario")
        
    def guardar_usuario(self):
        if not self.get_usuario() or not self.get_mail():
            usuario_generado, mail_generado = self.__usuario_dao.generar_usuario_mail(self.get_nombre(), self.get_apellido())
            self.set_usuario(usuario_generado)
            self.set_mail(mail_generado)


        self.__usuario_dao.crear_usuario(
            self.get_nombre(),
            self.get_apellido(),
            self.get_telefono(),
            self.__departamento_asignado,
            es_jefe=self.__es_jefe
        )
       
    def crear_usuario(self, es_jefe=False):       
        self.set_nombre(input(f"Ingrese el nombre\n\033[03;30m>>> \033[0m").strip().lower())
        self.set_apellido(input(f"Ingrese el apellido\n\033[03;30m>>> \033[0m").strip().lower())
        self.set_telefono(input(f"Ingrese el teléfono\n\033[03;30m>>> \033[0m").strip().lower())

        if not self.get_nombre() or not self.get_apellido() or not self.get_telefono():
            print("Rellene todos los campos")
            return None
        
        departamentos = self.__usuario_dao.obtener_departamentos()
        if not departamentos:
            print("No hay departamentos disponibles.")
            return None
        for idx, depto in enumerate(departamentos, start= 1):
            print(f"{idx}. {depto['NOMBRE']}")

        seleccion = int(input(f"Seleccione un departamento (1- {len(departamentos)})\n\033[03;30m>>> \033[0m").strip())
        if 1 <= seleccion <= len(departamentos):
            self.__departamento_asignado = departamentos[seleccion - 1]['ID']
        else:
            print("Seleccione un departamento ")
            return None
       
        self.es_jefe = es_jefe
        return self
    
    def crear_jefe(self):
        jefe = self.crear_usuario(es_jefe=True)
        if jefe:
            jefe.guardar_usuario()
        else:
            print("No se pudo crear el Jefe")

    def crear_empleado(self):
        empleado = self.crear_usuario(es_jefe=False) 
        
        if empleado:
            empleado.guardar_usuario()
        else:
            print("No se pudo crear Usuario Empleado.")


#ver usuarios
    def saber_tipo_usuario(self,info_usuario):
        es_gerente = info_usuario.get('ES_GERENTE', False)
        es_jefe = info_usuario.get('ES_JEFE', False)

        if es_gerente:
            return "Gerente"
        elif es_jefe:
            return "Jefe"
        else:
            return "Empleado"
    
    def mostrar_info(self, info_usuario):
        tipo_usuario = self.saber_tipo_usuario(info_usuario)
        if tipo_usuario == "Gerente":
            print(">>>Perfil Gerente<<<")
        elif tipo_usuario == "Jefe":
            print(">>>Perfil Jefe<<<")
        else:
            print("<<<Perfil Empleado>>>")

        data_del_perfil = {
            'ID': info_usuario.get('ID', 'No disponible'),
            'NOMBRE COMPLETO': f"{info_usuario.get('NOMBRE', '')} {info_usuario.get('APELLIDO', '')}",
            'TELEFONO': info_usuario.get('TELEFONO', 'No disponible'),
            'MAIL': info_usuario.get('MAIL', 'No disponible'),
            'INICIO CONTRATO': info_usuario.get('FECHA_INICIO', 'No disponible'),
            'USUARIO': info_usuario.get('USUARIO', 'No disponible'),
            'DEPARTAMENTO': info_usuario.get('NOMBRE_DEPARTAMENTO', 'Sin asignar')  # Asegúrate de que se llama correctamente
        }

        df = pd.DataFrame([data_del_perfil])
        print(f"{df.to_string(index=False)}\n")

    def ver_perfil(self, usuario):
        usuarios = self.__usuario_dao.ver_usuarios(usuario=usuario) 
        if usuarios:
            info_usuario = usuarios[0]
            self.mostrar_info(info_usuario)
        else:
            print(f"Usuario no econtrado")

    def ver_usuario(self, accion='ver', es_jefe=False, es_gerente=False):
        tipos = ["Empleados", "Jefes"]
        for idx, tipo in enumerate(tipos , start=1):
            print(f"{idx}. {tipo}")

        elegir_tipo = input(f"Seleccione un Tipo de Usuario (1-{len(tipos)})\n\033[03;30m>>>  \033[0m").strip().lower()
        
        if elegir_tipo == "1":
            es_jefe = False
            es_gerente = False
        elif elegir_tipo == "2":
            es_jefe = True
            es_gerente = False

        busqueda = ["Ver Todos", "Buscar por Nombre"]
        for idx, opcion in enumerate(busqueda, start=1):
            print(f"{idx}. {opcion}")


        eleccion = int(input(f"Elija una Opcion (1-{len(busqueda)})\n\033[03;30m>>> \033[0m").strip())
        
        if eleccion == 1:
            usuarios = self.__usuario_dao.ver_usuarios(es_jefe=es_jefe, es_gerente=es_gerente)
        elif eleccion == 2:
            nombre = str(input("Ingrese Nombre\n\033[03;30m>>> \033[0m")).strip().lower()
            apellido = str(input("Ingrese Apellido\n\033[03;30m>>> \033[0m")).strip().lower()
            usuarios = self.__usuario_dao.ver_usuarios(nombre=nombre, apellido=apellido, es_jefe=es_jefe)
        else:
            print("Seleccione una opcion")
            return

            
        if not usuarios:
            print(f"No hay {'empleados' if not es_jefe else 'jefes'}")
            return
        else:
            print(f"Lista de {'empleados' if not es_jefe else 'jefes'}")
            for idx, usuario in enumerate(usuarios, start=1):
                print(f"{idx}. {usuario['NOMBRE']} {usuario['APELLIDO']} {usuario['USUARIO']}")

        seleccion = input(f"Seleccione un Usuario para {accion} (1-{len(usuarios)})\n\033[03;30m>>> \033[0m").strip().lower()
        
        if seleccion.isdigit() and 1 <= int(seleccion) <= len(usuarios):
            usuarios_seleccionado = usuarios[int(seleccion) -1]
            usuario_dto = UsuarioDTO() 
            if accion == 'ver':  
                usuario_dto.mostrar_info(usuarios_seleccionado)

            elif accion == 'actualizar':
                self.actualizar_usuarios(usuarios_seleccionado, usuarios_seleccionado['ES_JEFE'])

            elif accion == 'eliminar':
                self.eliminar_usuario(usuarios_seleccionado)
        else:
            print("Seleccione un usuario")


#actualizar y eliminar usuarios
    def actualizar_usuarios(self, usuario, es_jefe):
        tipo_usuario = "Empleado" if es_jefe else "Jefes"
        print(f"Modificar {tipo_usuario}: {usuario['NOMBRE']} {usuario['APELLIDO']}")

        atributos_a_cambiar = ["Nombre", "Apellido", "Departamento", "Cargo"]
        cambios = False


        for idx, campo in enumerate(atributos_a_cambiar, start=1):
            print(f"{idx}. {campo}")

        seleccionar_un_campo = int(input(f"Seleccione un Campo (1-{len(atributos_a_cambiar)})\n\033[03;30m>>> \033[0m").strip())
        

        if seleccionar_un_campo == 1:
            self.__usuario_dao.verificar_usuarios_existentes(usuario['USUARIO'])


            nuevo_nombre = input("Ingrese el nuevo nombre\n\033[03;30m>>> \033[0m").strip().lower()
            if nuevo_nombre:
                usuario['NOMBRE'] = nuevo_nombre
                cambios = True
                
                nuevo_usuario, nuevo_mail = self.__usuario_dao.generar_usuario_mail(usuario['NOMBRE'], usuario['APELLIDO'])
                usuario['USUARIO'] = nuevo_usuario
                usuario['MAIL'] = nuevo_mail
                print(f"Nuevo Usuario y Mail: Usuario: {nuevo_usuario}, Email: {nuevo_mail}")

        elif seleccionar_un_campo == 2:
            nuevo_apellido = input("Ingrese el nuevo apellido\n\033[03;30m>>> \033[0m").strip().lower()
            if nuevo_apellido:
                usuario['APELLIDO'] = nuevo_apellido
                cambios = True


        elif seleccionar_un_campo == 3:
            departamentos = self.__usuario_dao.obtener_departamentos()

            print("Seleccione un Departamento")
            for idx, depto in enumerate(departamentos, start=1):
                print(f"{idx}. {depto['NOMBRE']}")


            nombre_departamento = None
            depto_id = None
            
            seleccion = int(input(f"Seleccione un departamento (1-{len(departamentos)})\n\033[03;30m>>> \033[0m").strip())

            if 1 <= seleccion <= len(departamentos):
                nombre_departamento = departamentos[seleccion - 1]['NOMBRE']

                usuario['DEPTO_ID'] = departamentos[seleccion - 1]['ID']
                print(f"Departamento seleccionado: {nombre_departamento}")
                cambios = True

        elif seleccionar_un_campo == 4:
            cargos = ["Jefe", "Empleado"]
            for idx, cargo in enumerate(cargos, start=1):
                print(f"{idx}. {cargo}")

            nuevo_cargo = int(input(f"Que cargo le asignara (1-{len(cargos)})\n\033[03;30m>>> \033[0m").strip())

            if nuevo_cargo == 1 :
                usuario['ES_JEFE'] = True
                usuario['ES_GERENTE'] = False
                cambios = True
            elif nuevo_cargo == 2:
                usuario['ES_JEFE'] = False
                usuario['ES_GERENTE'] = False 
                cambios = True
            else:
                print("No se realizaron cambios.")

        
        if cambios:
            self.__usuario_dao.actualizar_usuario(
                usuario['ID'],
                usuario['NOMBRE'],
                usuario['APELLIDO'],
                usuario.get('DEPTO_ID'), 
                usuario.get('TELEFONO', None), 
                usuario['ES_JEFE'],
                usuario['ES_GERENTE']
            )

            self.__usuario_dao.actualizar_username_y_email(usuario['ID'], usuario['USUARIO'], usuario['MAIL'])
        else:
            print("No se realizaron cambios.")

    def eliminar_usuario(self,usuario):
        usuario_jefe = usuario['USUARIO']

        confirma = input("Desea Eliminar el Usario Jefe? \033[03;30m(S/N)\n>>> \033[0m").lower().strip()
        if confirma == "s":
            if self.__usuario_dao.eliminar_usuario(usuario_jefe, es_jefe=usuario['ES_JEFE']):
                print(f"El Usuario {usuario_jefe} fue Eliminado del Sistema")
        else:
            print("Operacion cancelada.")



#mas opciones
    def crear_proyecto(self, info_usuario):
        nombre_proyecto = input("Ingrese el nombre del proyecto\n\033[03;30m>>> \033[0m").strip().lower()

        departamentos = self.__usuario_dao.obtener_departamentos(info_usuario['ID']) 
        if not departamentos:
            print("No hay departamentos disponibles.")
            return None

        print("Seleccione un departamento:")
        for idx, depto in enumerate(departamentos, start=1):
            print(f"{idx}. {depto['NOMBRE']}")

        seleccion_departamento = int(input("Seleccione un departamento (número): ")) - 1

        if 0 <= seleccion_departamento < len(departamentos):
            departamento_id = int(departamentos[seleccion_departamento]['ID'])
        else:
            print("Seleccione un departamento valido.")
            return None

        self.__proyecto_dao.crear_proyecto(nombre_proyecto, departamento_id)
        print(f"Proyecto {nombre_proyecto} creado con exito")

    def __str__(self):
        txt = f"{super().__str__()}\n"
        return txt