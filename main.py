
from app.DTO.main_dto import MainDTO
from app.DTO.usuario_dto import UsuarioDTO
from app.DTO.jefe_dto import Jefe

def menu_principal(info_usuario):
    usuario_dto = UsuarioDTO()
    jefe_dto = Jefe() 


    tipo_de_usuario = usuario_dto.saber_tipo_usuario(info_usuario)
    nombre_completo = f"{info_usuario['NOMBRE']} {info_usuario['APELLIDO']}"

    while True:
        print(f"<<<Bienvenido {nombre_completo}>>>\n")


        opciones_principales=["Ver Perfil", "Cambiar contraseña"]

        if tipo_de_usuario == "Gerente":
            opciones_gerente = ["Crear Usuario", "Ver Usuario", "Actualizar Usuario", "Eliminar Usuario", "Otras Opciones"]
            opciones_principales += opciones_gerente

        elif tipo_de_usuario == "Jefe":
            opciones_jefe = ["Crear Empleado", "Ver Empleados", "Crear Proyecto"]
            if info_usuario['DEPTO_ID'] == 1: 
                opciones_jefe.append("Notificaciones RRHH")
            elif info_usuario['DEPTO_ID'] == 2:
                opciones_jefe.append("Notificaciones Finanzas")

            opciones_principales += opciones_jefe

        elif tipo_de_usuario == 'Empleado': 
            pass

        for idx, opcion_gerente in enumerate(opciones_principales, start=1):
            print(f"{idx}.{opcion_gerente}")
        opcion = input("Seleccione una opción\033[03;30m(0 para salir)\033[0m: ")
        
        if opcion == "0":
            usuario_data = main_dto.login()
            if usuario_data:
                menu_principal(usuario_data)


        

        elif opcion == "1":
            usuario_dto.ver_perfil(info_usuario['USUARIO'])
        elif opcion == "2":
            main_dto.cambiar_contrasena(info_usuario['USUARIO'])
        elif tipo_de_usuario == "Gerente":
            if opcion == "3":
                usuario_dto.menu_crear_usuario()
            elif opcion == "4":
                usuario_dto.ver_usuario(accion='ver', es_gerente=True)
            elif opcion == "5":
                usuario_dto.ver_usuario(accion='actualizar')
            elif opcion == "6":
                usuario_dto.ver_usuario(accion='eliminar')
            
            #mas opciones
            elif opcion == "7":
                otras_opciones = ["Crear Proyecto", "Crear Tareas", "Generar Informe", "Notificaciones RRHH", "Notificaciones Finanzas"]
                for indice, mas in enumerate(otras_opciones, start=1):
                    print(f"{indice}. {mas}")
                eleccion_mas_opciones = input("Seleccione una opcion\033[03;30m(0 para salir)\033[0m: ")
                if eleccion_mas_opciones == "1":
                    usuario_dto.crear_proyecto(info_usuario)

                elif eleccion_mas_opciones == "2":
                    pass
                elif eleccion_mas_opciones == "3":
                    pass
                elif eleccion_mas_opciones == "4":
                    jefe_dto.notificaciones_rrhh() 
                elif eleccion_mas_opciones == "5":
                    jefe_dto.notificaciones_finanzas()
                elif eleccion_mas_opciones == "0":
                    continue


        elif tipo_de_usuario == "Jefe":
            if opcion == "3":
                jefe_dto.crear_empleado()  
            elif opcion == "4":
                pass
            elif opcion == "5":
                jefe_dto.crear_proyecto()
            elif opcion == "6":            
                if info_usuario['DEPTO_ID'] == 1: 
                    jefe_dto.notificaciones_rrhh() 
                elif info_usuario['DEPTO_ID'] == 2:
                    jefe_dto.notificaciones_finanzas()
                 
            elif opcion == "8":
                break
        
        else:
            print("Ingrese una opción correcta")
            

if __name__ == "__main__":
    print("<<<Inicio de Sesión>>>")
    main_dto = MainDTO() 
    usuario_data = main_dto.login()
    
    if usuario_data:
        menu_principal(usuario_data)
    else:
        print("Finalizando el programa.")
