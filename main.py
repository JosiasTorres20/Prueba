from app.DAO.gerente_dao import GerenteDao
from app.DTO.gerente_dto import Gerente
from app.DTO import main_dto


def menu_principal(info_usuario):
    tipo_de_usuario = main_dto.saber_tipo_usuario(info_usuario)
    nombre_completo = f"{info_usuario['NOMBRE']} {info_usuario['APELLIDO']}"

    while True:
        print(f"\n<<<Bienvenido {nombre_completo}>>>")

        if tipo_de_usuario =="Gerente":
            print("1. Ver perfil")
            print("2. Cambiar contraseña")
            print("3. Crear Jefe")
            print("4. Ver Jefes")
            print("5. Actualizar Jefe")
            print("6. Eliminar Jefe")
            print("7. Salir")

        elif tipo_de_usuario == "Jefe":     #aqui tienen para cargar el menu del jefe 
            pass
        elif tipo_de_usuario == 'Empleado': #aqui el del empleado
            pass

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            main_dto.mostrar_info(info_usuario)  #las principales como ver perfil y cambiar pass van aparte
        elif opcion == "2":
            main_dto.cambiar_contrasena(info_usuario['USUARIO'])
        elif tipo_de_usuario == "Gerente":          #asi como aqui condicionan las demas opciones segun 
            if opcion == "3":
                datos = Gerente.crear_jefe()                    #lo que devuelva la def en la main dto
                if datos:
                    GerenteDao.crear_jefe(datos['nombre'], datos['apellido'], datos['telefono'], datos['departamento_asignado'])
            
            elif opcion == "4":
                main_dto.buscar_jefes() 
            elif opcion == "5":
                main_dto.actualizar_jefe()
                pass
            elif opcion == "7":
                break



#me falta pulir alganas def como la de ver los jefes que el filtro k estoy haciendo le falta un poco de detalle
#nasheei
        else:
            print("Ingrese una opcion correcta")

if __name__ == "__main__":
    print("<<<Inicio de Sesión>>>")
    usuario_data = main_dto.login()
    
    if usuario_data:
        menu_principal(usuario_data)
    else:
        print("Finalizando el programa.")
