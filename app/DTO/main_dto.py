import pandas as pd
import bcrypt
import os
from app.DAO import main_dao
from app.DAO import jefe_dao
from app.DAO.gerente_dao import GerenteDao

def login():
    print("Usuario")
    usuario = str(input("\033[03;30m>>> \033[0m"))

    intentos = 0
    while intentos < 3:
        print("Contaseña")
        psw = str(input("\033[03;30m>>> \033[0m"))

        info_usuario = main_dao.validar_credenciales(usuario,psw)
        if info_usuario:
            verificar_dpto_rrhh= main_dao.saber_id_depto("RRHH")
            if info_usuario['ES_JEFE'] and info_usuario['DEPTO_ID'] == verificar_dpto_rrhh:
                verificar_si_hay_pendientes, total_pendiente = jefe_dao.verificar_jefe_asignar_depo()

                if verificar_si_hay_pendientes:
                    print(f"Hay {total_pendiente} usuarios jefe sin departamento asignado ")


            return info_usuario


        else:
            intentos +=1
            print("Usuario o Contaseña incorrectos")

            if intentos >= 3:
                print("Clave Bloqueada.\033[03;30m/se necesita reestablecerla\033[0m")
                print("Ingrese clave del Gerente")

                root_psw = str(input("\033[03;30m>>> \033[0m"))


                if main_dao.validar_credenciales("root",root_psw):
                    print("Ingrese la nueva clave")
                    nueva_psw = str(input("\033[03;30m>>> \033[0m"))
                    hashed_nueva_psw = bcrypt.hashpw(nueva_psw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                    main_dao.actualizar_psw(usuario, hashed_nueva_psw)
                    print("\033[03;30mClave actualizada con exito\033[0m")

                else:
                    print("Clave del Gerente incorrecta")
                break

                                    
    return None
def hash_claves(psw):
    psw_en_bytes = psw.encode('utf-8')
    hashear_claves = bcrypt.hashpw(psw_en_bytes, bcrypt.gensalt())
    return hashear_claves
def revision_del_hash(psw, hash_claves):
    if isinstance(hash_claves, str):
        hash_claves = hash_claves.encode('utf-8')
    return bcrypt.checkpw(psw.encode('utf-8'), hash_claves)

def cambiar_contrasena(usuario):
    actual_psw = input("Ingrese su contraseña actual: ")

    if main_dao.validar_credenciales(usuario, actual_psw):
        nueva_psw = input("Ingrese la nueva contraseña: ") 
        hashed_nueva_psw = hash_claves(nueva_psw)
        main_dao.actualizar_psw(usuario, hashed_nueva_psw)
        print("Contraseña actualizada con éxito.")
    else:
        print("Contraseña actual incorrecta. No se pudo actualizar.")

def saber_tipo_usuario(info_usuario):
    es_gerente = info_usuario.get('ES_GERENTE', False)
    es_jefe = info_usuario.get('ES_JEFE', False)

    if es_gerente:
        return "Gerente"
    elif es_jefe:
        return "Jefe"
    else:
        return "Empleado"
    
def mostrar_info(info_usuario):
    tipo_usuario = saber_tipo_usuario(info_usuario)

    if tipo_usuario == "Gerente":
        print(">>>Perfil Gerente<<<")
    elif tipo_usuario == "Jefe":
        print(">>>Perfil Jefe<<<")
    else:
        print("<<<Perfil Empleado>>>")

    depto_id = info_usuario.get('DEPTO_ID')


    data_del_perfil={
        'ID': info_usuario.get('ID', 'No disponible'),
        'NOMBRE COMPLETO': f"{info_usuario['NOMBRE']} {info_usuario['APELLIDO']}",
        'TELEFONO': info_usuario.get('TELEFONO', 'No disponible'),
        'MAIL': info_usuario.get('USUARIO', 'No disponible'),
        'INICIO CONTRATO': info_usuario.get('FECHA_INICIO', 'No disponible'),
        'USUARIO': info_usuario.get('USUARIO', 'No disponible'),
        'DEPARTAMENTO': info_usuario['DEPARTAMENTO'] if info_usuario['DEPARTAMENTO'] else "no asignado",

    }

    df = pd.DataFrame([data_del_perfil])
    print(df.to_string(index=False))

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
                mostrar_info(jefe_seleccionado) 
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
                mostrar_info(jefe_seleccionado)
                return jefes[int(seleccion) - 1] 
            else:
                    print("Seleccione un Usuario de la lista")
                    return None
        else:
            print("No hay Usuarios Jefe Registrados")

def actualizar_jefe():
    buscar_el_jefe = buscar_jefes()
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
            departamentos = main_dao.saber_id_depto()
            print("Seleccione un Departamento")
            for idx, depto in enumerate(departamentos, start=1):
                print(f"{idx}. {depto['NOMBRE']}")

            nombre_departamento = input("Seleccione un departamento\n\033[03;30m>>> \033[0m").strip()
            if nombre_departamento:
                id_departamento = main_dao.saber_id_depto(nombre_departamento)
                if id_departamento:
                    print(f"Departamento {nombre_departamento} actualizado con exito.")
                else:
                    print("No se pudoc actualizar")

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

        GerenteDao.actualizar_jefe(buscar_el_jefe['ID'], nombre, apellido,usuario,id_departamento)
        print(f"Jefe {buscar_el_jefe['NOMBRE']} {buscar_el_jefe['APELLIDO']}")
            
