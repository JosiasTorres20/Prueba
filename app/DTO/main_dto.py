import pandas as pd
import bcrypt
from app.DAO import main_dao
from app.DAO import jefe_dao
from app.DAO.gerente_dao import GerenteDao



def login():
    print("Usuario")
    usuario = str(input("\033[03;30m>>> \033[0m"))
    
    #validación
    while True:
        if main_dao.validar_existencia_usuario(usuario) == False:
            print("Error, usuario no encontrado")
            print("Porfavor intente nuevamente")
            usuario = str(input("\033[03;30m>>> \033[0m"))
        else:
            break
        

    intentos = 0

    while intentos < 3:
        print("Contaseña")
        psw = str(input("\033[03;30m>>> \033[0m"))


        info_usuario = main_dao.validar_credenciales(usuario,psw)

        if info_usuario:
            verificar_dpto_rrh= main_dao.saber_id_depto("RRHH")
            if info_usuario['ES_JEFE'] and info_usuario['DEPTO_ID'] == verificar_dpto_rrh:
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
    if info_usuario['ES_GERENTE']:
        return "Gerente"
    elif info_usuario['ES_JEFE']:
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



    data_del_perfil={
        'ID': info_usuario['ID'],
        'NOMBRE COMPLETO': f"{info_usuario['NOMBRE']} {info_usuario['APELLIDO']}",
        'TELEFONO': info_usuario['TELEFONO'],
        'MAIL': info_usuario['MAIL'],
        'INICIO CONTRATO': info_usuario['FECHA_INICIO'],
        'USUARIO': info_usuario['USUARIO']
    }

    df = pd.DataFrame([data_del_perfil])
    print(df.to_string(index=False))

def buscar_jefes():
    print("1.Ver todos los Jefes\n2.Buscar Jefe")
    ver_opcion = input(">>> ").strip()
    if ver_opcion == "1":
        jefes = GerenteDao.mostrar_jefe()
        if not jefes:
            print("No se encontraron jefes.")
            return

        print("\n>>> Lista de Jefes <<<")
        for idx, jefe in enumerate(jefes, start=1):
            print(f"{idx}. {jefe['NOMBRE']} {jefe['APELLIDO']} (Usuario: {jefe['USUARIO']}, Departamento: {jefe.get('DEPARTAMENTO', 'No asignado')})")

        seleccion = input(f"Seleccione el número del jefe para ver detalles (1-{len(jefes)}): ").strip()

        if seleccion.isdigit() and 1 <= int(seleccion) <= len(jefes):
            jefe_seleccionado = jefes[int(seleccion) - 1]
            mostrar_info(jefe_seleccionado) 
        else:
            print("Selección no válida.")
    elif ver_opcion == "2":
        print("Ingrese nombre y apellido del jefe a bucar")
        nombre = input("Nombre>>> ").strip()
        apellido = input("Apellido>>> ").strip()

        jefes = GerenteDao.mostrar_jefe(nombre , apellido)

        
        if jefes: 
            print(f"<<<Lista de Usuarios Jefe>>>")
            for idx, jefe in enumerate(jefes, start=1):
                print(f"{idx}. {jefe['NOMBRE']} {jefe['APELLIDO']} (Usuario): {jefe['USUARIO']}")
                seleccion = input(f"Seleccione uno (1-{len(jefes)}): ").strip()
                if seleccion.isdigit() and 1 <= int(seleccion) <= len(jefes):
                    jefe_seleccionado = jefes[int(seleccion) -1]
                    mostrar_info(jefe_seleccionado)
                    return jefes[int(seleccion) - 1] 
                else:
                    print("Seleccione un Usuario de la lista")
                    return None
        else:
            print("No hay Usuarios Jefe Registrados")
