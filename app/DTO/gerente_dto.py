import bcrypt
from app.DTO.jefe_dto import Jefe
from app.DTO import main_dto
from app.DAO import main_dao
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


    @staticmethod
    def crear_jefe():
        nombre_jefe = input("Ingrese el nombre del jefe: ")
        apellido_jefe = input("Ingrese el apellido del jefe: ")
        telefono_jefe = input("Ingrese el teléfono del jefe: ")

        departamentos = [
            {'ID': 1, 'NOMBRE': 'RR.HH'},
            {'ID': 2, 'NOMBRE': 'Finanzas'},
            {'ID': 3, 'NOMBRE': 'Marketing'}
        ]

        for idx, dep in enumerate(departamentos, start= 1):
            print(f"{idx}. {dep['NOMBRE']}")

        seleccion = input(f"Seleccione un departamento (1- {len(departamentos)})\n\033[03;30m>>> \033[0m").strip()
        if seleccion.isdigit() and 1 <= int(seleccion) <= len(departamentos):
            departamento_asignado = departamentos[int(seleccion) - 1]['ID']
            return {
                "nombre": nombre_jefe,
                "apellido": apellido_jefe,
                "telefono": telefono_jefe,
                "departamento_asignado": departamento_asignado
            }
        else:
            print("Ingrese un departamento Valido")
            return None   
    @staticmethod
    def buscar_jefes():

        ver_opcion = input("1.Ver todos los Jefes\n2.Buscar Jefe\n\033[03;30m>>> \033[0m").strip()

        if ver_opcion == "1":
            jefes = GerenteDao.mostrar_jefe()
            if not jefes:
                print("No se encontraron jefes.")
                return None
            
            else:
                print("\n>>> Lista de Jefes <<<")
                for idx, jefe in enumerate(jefes, start=1):
                    departamento = jefe['DEPARTAMENTO'] if jefe['DEPARTAMENTO'] else "No asignado"
                    print(f"{idx}. {jefe['NOMBRE']} {jefe['APELLIDO']} (Usuario: {jefe['USUARIO']}, Departamento: {jefe.get('DEPARTAMENTO', 'No asignado')})")

                seleccion = input(f"Seleccione el número del jefe para ver detalles (1-{len(jefes)})\n\033[03;30m>>> \033[0m").strip()

                if seleccion.isdigit() and 1 <= int(seleccion) <= len(jefes):
                    jefe_seleccionado = jefes[int(seleccion) - 1]
                    main_dto.mostrar_info(jefe_seleccionado) 
                    return jefe_seleccionado
                else:
                    print("Selección no válida.")
                    return None
                
        elif ver_opcion == "2":
            print("Ingrese nombre y apellido del jefe a bucar")
            nombre = input("Nombre\033[03;30m>>> \033[0m").strip()
            apellido = input("Apellido\033[03;30m>>> \033[0m").strip()

            jefes = GerenteDao.mostrar_jefe(nombre , apellido)

            
            if jefes: 
                print(f"<<<Lista de Usuarios Jefe>>>")
                for idx, jefe in enumerate(jefes, start=1):
                    print(f"{idx}. {jefe['NOMBRE']} {jefe['APELLIDO']} (Usuario): {jefe['USUARIO']}")
                seleccion = input(f"Seleccione uno (1-{len(jefes)})\n\033[03;30m>>> \033[0m").strip()
                if seleccion.isdigit() and 1 <= int(seleccion) <= len(jefes):
                    jefe_seleccionado = jefes[int(seleccion) -1]
                    main_dto.mostrar_info(jefe_seleccionado)
                    return jefes[int(seleccion) - 1] 
                else:
                        print("Seleccione un Usuario de la lista")
                        return None
            else:
                print("No hay Usuarios Jefe Registrados")
    @staticmethod
    def actualizar_usuario():
        tipos = ["Empleado", "Jefe"]
        for idx, tipo in enumerate(tipos , start=1):
            print(f"{idx}. {tipo}")
        elegir_tipo = input(f"Seleccione un Tipo de Usuario (1-{len(tipos)})\n\033[03;30m>>>  ")
        if elegir_tipo == "1":
            pass
        buscar_el_jefe = Gerente.buscar_jefes()
        if buscar_el_jefe:
            print("Que desea modificar")
            campos = ["Nombre", "Apellido" ,"Departamento", "Usuario"]
            for idx, campos in enumerate(campos, start=1):
                print(f"{idx}. {campos}")

            seleccion = input("\033[03;30m>>> \033[0m")  


            nombre = buscar_el_jefe['NOMBRE']
            apellido = buscar_el_jefe['APELLIDO']
            usuario = buscar_el_jefe['USUARIO']
            id_departamento = buscar_el_jefe.get('DEPTO_ID', None)
            telefono = buscar_el_jefe.get('TELEFONO', None)
            mail = buscar_el_jefe.get('MAIL', None)

            if seleccion == "1":
                nuevo_nombre = input("Ingrese el nuevo nombre\n\033[03;30m>>> \033[0m").strip()
                if nuevo_nombre:
                    nombre = nuevo_nombre
                    print(f"Nombre {nuevo_nombre} actualizado con exito.")
                else:
                    print("No se realizaron los cambios")

            elif seleccion =="2":
                nuevo_apellido = input("Ingrese el nuevo apellido\n\033[03;30m>>> \033[0m").strip()
                if nuevo_apellido:
                    apellido = nuevo_apellido
                    print(f"Apellido {nuevo_apellido} actualizado con exito")
                else:
                    print("No se realizaron los cambios")

            elif seleccion == "3":
                departamentos = main_dao.obtener_departamentos()
                print("Seleccione un Departamento")
                for idx, depto in enumerate(departamentos, start=1):
                    print(f"{idx}. {depto['NOMBRE']}")

                nombre_departamento = input("Seleccione un departamento\n\033[03;30m>>> \033[0m").strip()
                if nombre_departamento:
                    id_departamento = main_dao.saber_id_depto(nombre_departamento)
                    if id_departamento:
                        print(f"Departamento {nombre_departamento} actualizado con exito.")
                    else:
                        print("No se pudo actualizar")

                else:
                    print("Seleccion invalida")

            elif seleccion == "4":
                nuevo_usuario = input(f"Ingrese el nuevo usuarios\n\033[03;30m>>> \033[0m")
                if nuevo_usuario:
                    usuario = nuevo_usuario
                    print(f"Usuario {nuevo_usuario} actualizado con exito")
                else:
                    print("No se realizaron los cambios")
            else:
                print("Opcion ingresada no es valida")
            actualizacion_realizada = GerenteDao.actualizar_jefe(
                buscar_el_jefe['USUARIO'], 
                nombre,
                apellido,
                usuario,
                id_departamento,
                telefono,
                mail
            )
            if actualizacion_realizada:
                print(f"Jefe {buscar_el_jefe['NOMBRE']} {buscar_el_jefe['APELLIDO']}")
            else:
                print("Nose pudo actualizar el jefe") 
    @staticmethod
    def eliminar_jefe():
        buscar_jefe = Gerente.buscar_jefes()
        if buscar_jefe:
            usuario_jefe = buscar_jefe['USUARIO']

            confirma = input("Desea Eliminar el Usario Jefe? \033[03;30m(S/N)\n>>> \033[0m").lower()
            if confirma == "s":
                if GerenteDao.eliminar_jefe(usuario_jefe):
                    print(f"El Usuario {usuario_jefe} fue Eliminado del Sistema")
                else:
                    print("No se pudo Eliminar el Usuario")
            else:
                pass


    def __str__(self):
        txt = f"{super().__str__()}\n"
        return txt

