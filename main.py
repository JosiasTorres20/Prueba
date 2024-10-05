
from app.DAO.gerente_dao import GerenteDao
from app.DTO.gerente_dto import Gerente
from app.DTO import main_dto


def menu_principal(info_usuario):
    tipo_de_usuario = main_dto.saber_tipo_usuario(info_usuario)
    nombre_completo = f"{info_usuario['NOMBRE']} {info_usuario['APELLIDO']}"

    while True:
        print(f"<<<Bienvenido {nombre_completo}>>>\n")
        opciones_principales=["Ver Perfil", "Cambiar contraseña"]

        if tipo_de_usuario == "Gerente":
            opciones_gerente = ["Crear Jefe", "Ver Jefes", "Actualizar Usuario", "Eliminar Jefes", "Salir"]
            opciones_principales += opciones_gerente
            for idx, opcion_gerente in enumerate(opciones_principales, start=1):
                print(f"{idx}.{opcion_gerente}")

        elif tipo_de_usuario == "Jefe":
            pass

        elif tipo_de_usuario == 'Empleado': 
            pass

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            main_dto.limpiar()
            main_dto.mostrar_info(info_usuario) 
        elif opcion == "2":
            main_dto.limpiar()
            main_dto.cambiar_contrasena(info_usuario['USUARIO'])
        elif tipo_de_usuario == "Gerente":
            if opcion == "3":
                main_dto.limpiar()
                datos = Gerente.crear_jefe()
                if datos:
                    GerenteDao.crear_jefe(datos['nombre'], datos['apellido'], datos['telefono'], datos['departamento_asignado'])      
            elif opcion == "4":
                main_dto.limpiar()
                Gerente.buscar_jefes()
            elif opcion == "5":
                main_dto.limpiar()
                Gerente.actualizar_jefe()
            elif opcion == "6":
                main_dto.limpiar()
                Gerente.eliminar_jefe()
            elif opcion == "7":
                main_dto.login()
                
        else:
            print("Ingrese una opcion correcta")

if __name__ == "__main__":
    print("<<<Inicio de Sesión>>>")
    usuario_data = main_dto.login()
    main_dto.limpiar()
    
    if usuario_data:
        menu_principal(usuario_data)
    else:
        print("Finalizando el programa.")
