from app.DAO import usuario_dao
from app.DAO import main_dao
from app.DTO import main_dto
from app.DAO import usuario_dao

class UsuarioDTO:
    @staticmethod
    def crear_usuario(es_jefe):
        nombre = input(f"Ingrese el nombre\n\033[03;30m>>> \033[0m").strip().lower()
        apellido = input(f"Ingrese el apellido\n\033[03;30m>>> \033[0m").strip().lower()
        telefono = input(f"Ingrese el teléfono\n\033[03;30m>>> \033[0m").strip().lower()

        if not nombre or not apellido or not telefono:
            print("Rellene todos los campos")
            return None
        
        departamentos = main_dao.obtener_departamentos()
        for idx, depto in enumerate(departamentos, start= 1):
            print(f"{idx}. {depto['NOMBRE']}")
        seleccion = int(input(f"Seleccione un departamento (1- {len(departamentos)})\n\033[03;30m>>> \033[0m").strip())
        
        departamento_asignado = departamentos[int(seleccion) - 1]['ID']



        if es_jefe:
            print("Creando Usuario Jefe")
        else:
            print("Creando Usuario Empleado")
            
        return {
                'nombre': nombre,
                'apellido': apellido,
                'telefono': telefono,
                'departamento_asignado': departamento_asignado,
                'es_jefe': es_jefe
            }

    @staticmethod
    def crear_jefe():
        datos = UsuarioDTO.crear_usuario(es_jefe=True)

        if datos:
            usuario_dao.crear_usuario(
                datos['nombre'],
                datos['apellido'],
                datos['telefono'],
                datos['departamento_asignado'],
                es_jefe=True    
            )
        else:
            print("No se pudo crear el Jefe")

    @staticmethod
    def crear_empleado():
        datos = UsuarioDTO.crear_usuario(es_jefe=False) 
        
        if datos:
            usuario_dao.crear_usuario(
                datos['nombre'],
                datos['apellido'],
                datos['telefono'],
                datos['departamento_asignado'],
                es_jefe=False
            )
        else:
            print("No se pudo crear Usuario Empleado.")

    @staticmethod
    def ver_usuario(accion='ver'):
        main_dto.limpiar()
        tipos = ["Empleados", "Jefes"]
        for idx, tipo in enumerate(tipos , start=1):
            print(f"{idx}. {tipo}")


        elegir_tipo = input(f"Seleccione un Tipo de Usuario (1-{len(tipos)})\n\033[03;30m>>>  \033[0m").strip().lower()
        
        
        if elegir_tipo == "1":
            es_jefe = False
        elif elegir_tipo == "2":
            es_jefe = True
        else:
            print("Seleccione un Tipo de Usuario")
            return
        

        main_dto.limpiar()
        busqueda = ["Ver Todos", "Buscar por Nombre"]
        for idx, opcion in enumerate(busqueda, start=1):
            print(f"{idx}. {opcion}")


        eleccion = int(input(f"Elija una Opcion (1-{len(busqueda)})\n\033[03;30m>>> \033[0m").strip())
        
        if eleccion == 1:
            usuarios = usuario_dao.ver_usuarios(es_jefe=es_jefe)
        elif eleccion == 2:
            nombre = str(input("Ingrese Nombre\n\033[03;30m>>> \033[0m")).strip().lower()
            apellido = str(input("Ingrese Apellido\n\033[03;30m>>> \033[0m")).strip().lower()
            usuarios = usuario_dao.ver_usuarios(nombre=nombre, apellido=apellido, es_jefe=es_jefe)
        else:
            print("Seleccione una opcion")
            return

            
        if not usuarios:
            print(f"No hay {'empleados' if not es_jefe else 'jefes'}")
            return
        else:
            main_dto.limpiar()
            print(f"Lista de {'empleados' if not es_jefe else 'jefes'}")
            for idx, usuario in enumerate(usuarios, start=1):
                print(f"{idx}. {usuario['NOMBRE']} {usuario['APELLIDO']} {usuario['USUARIO']}")


        seleccion = input(f"Seleccione un Usuario para {accion} (1-{len(usuarios)})\n\033[03;30m>>> \033[0m").strip().lower()
        
        if seleccion.isdigit() and 1 <= int(seleccion) <= len(usuarios):
            usuarios_seleccionado = usuarios[int(seleccion) -1]
            if accion == 'ver':
                main_dto.mostrar_info(usuarios_seleccionado)

            elif accion == 'actualizar':
                UsuarioDTO.actualizar_usuarios(usuarios_seleccionado, usuarios_seleccionado['ES_JEFE'])

            elif accion == 'eliminar':
                UsuarioDTO.eliminar_usuario(usuarios_seleccionado)
        else:
            print("Seleccione un usuario")

    @staticmethod
    def actualizar_usuarios(usuario, es_jefe):
        main_dto.limpiar()
        tipo_usuario = "Jefe" if es_jefe else "Empleado"
        print(f"Modificar {tipo_usuario}: {usuario['NOMBRE']} {usuario['APELLIDO']}")

        atributos_a_cambiar = ["Nombre", "Apellido", "Departamento", "Cargo"]
        cambios = False


        for idx, campo in enumerate(atributos_a_cambiar, start=1):
            print(f"{idx}. {campo}")

        seleccionar_un_campo = int(input(f"Seleccione un Campo (1-{len(atributos_a_cambiar)})\n\033[03;30m>>> \033[0m").strip())
        

        if seleccionar_un_campo == 1:
            usuario_dao.verificar_usuarios_existentes(usuario['USUARIO'])

            main_dto.limpiar()
            nuevo_nombre = input("Ingrese el nuevo nombre\n\033[03;30m>>> \033[0m").strip().lower()
            if nuevo_nombre:
                usuario['NOMBRE'] = nuevo_nombre
                cambios = True
                
                nuevo_usuario, nuevo_mail = usuario_dao.generar_usuario_mail(usuario['NOMBRE'], usuario['APELLIDO'])
                usuario['USUARIO'] = nuevo_usuario
                usuario['MAIL'] = nuevo_mail
                print(f"Nuevo Usuario y Mail: Usuario: {nuevo_usuario}, Email: {nuevo_mail}")

        elif seleccionar_un_campo == 2:
            main_dto.limpiar()
            nuevo_apellido = input("Ingrese el nuevo apellido\n\033[03;30m>>> \033[0m").strip().lower()
            if nuevo_apellido:
                usuario['APELLIDO'] = nuevo_apellido
                cambios = True


        elif seleccionar_un_campo == 3:
            main_dto.limpiar()
            departamentos = main_dao.obtener_departamentos()

            print("Seleccione un Departamento")
            for idx, depto in enumerate(departamentos, start=1):
                print(f"{idx}. {depto['NOMBRE']}")


            nombre_departamento = None
            id_departamento = None
            
            seleccion = int(input(f"Seleccione un departamento (1-{len(departamentos)})\n\033[03;30m>>> \033[0m").strip())

            if 1 <= seleccion <= len(departamentos):
                nombre_departamento = departamentos[seleccion - 1]['NOMBRE']

                id_departamento = main_dao.saber_id_depto(nombre_departamento)
                print(f"Departamento seleccionado: {nombre_departamento}")
                if id_departamento:
                    usuario['DEPTO_ID'] = id_departamento
                    cambios = True
                else:
                    print("No se encontro el departamento.")
        
            else:
                print("Seleccione un departamento.")


        elif seleccionar_un_campo == 4:
            main_dto.limpiar()
            cargos = ["Jefe", "Empleado"]
            for idx, cargo in enumerate(cargos, start=1):
                print(f"{idx}. {cargo}")

            nuevo_cargo = int(input(f"Que cargo le asignara (1-{len(cargos)})\n\033[03;30m>>> \033[0m").strip())
            
            if nuevo_cargo == 1:
                usuario['ES_JEFE'] = True
                cambios = True
            elif nuevo_cargo == 2:
                usuario['ES_JEFE'] = False
                cambios = True
            else:
                print("No se realizaron cambios.")


        if cambios:
            usuario_dao.actualizar_usuario(
                usuario['ID'],
                usuario['NOMBRE'],
                usuario['APELLIDO'],
                usuario.get('DEPTO_ID', None), 
                usuario.get('TELEFONO', None), 
                usuario['ES_JEFE']
            )

            usuario_dao.actualizar_username_y_email(usuario['ID'], usuario['USUARIO'], usuario['MAIL'])
        else:
            print("No se realizaron cambios.")

    @staticmethod
    def eliminar_usuario(usuario):
        usuario_jefe = usuario['USUARIO']

        confirma = input("Desea Eliminar el Usario Jefe? \033[03;30m(S/N)\n>>> \033[0m").lower().strip()
        if confirma == "s":
            if usuario_dao.eliminar_usuario(usuario_jefe, es_jefe=usuario['ES_JEFE']):
                print(f"El Usuario {usuario_jefe} fue Eliminado del Sistema")
            else:
                print("No se pudo eliminar el usuario")
        else:
            print("Operacion cancelada.")

    def __str__(self):
        txt = f"{super().__str__()}\n"
        return txt