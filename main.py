

from app.DTO import main_dto
from app.DTO.usuario_dto import UsuarioDTO


def menu_principal(info_usuario):
    tipo_de_usuario = main_dto.saber_tipo_usuario(info_usuario)
    nombre_completo = f"{info_usuario['NOMBRE']} {info_usuario['APELLIDO']}"

    while True:
        print(f"<<<Bienvenido {nombre_completo}>>>\n")
        opciones_principales=["Ver Perfil", "Cambiar contraseña"]

        if tipo_de_usuario == "Gerente":
            opciones_gerente = ["Crear Usuario", "Ver Usuario", "Actualizar Usuario", "Eliminar Usuario", "Salir"]
            opciones_principales += opciones_gerente

        elif tipo_de_usuario == "Jefe":
            opciones_jefe = ["Crear Empleado", "Ver Empleados", "Actualizar Usuario", "Salir"]
            opciones_principales += opciones_jefe

        elif tipo_de_usuario == 'Empleado': 
            pass

        for idx, opcion_gerente in enumerate(opciones_principales, start=1):
            print(f"{idx}.{opcion_gerente}")
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
                main_dto.menu_crear_usuario()
            elif opcion == "4":
                main_dto.limpiar()
                UsuarioDTO.ver_usuario(accion = 'ver')
            elif opcion == "5":
                print("Entrando en la opción de Actualizar Usuario...")
                UsuarioDTO.ver_usuario(accion='actualizar')
            elif opcion == "6":
                main_dto.limpiar()
                UsuarioDTO.ver_usuario(accion='eliminar')
            elif opcion == "7":
                break

        elif tipo_de_usuario == "Jefe":
            if opcion == "3":
                main_dto.menu_crear_usuario()

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
