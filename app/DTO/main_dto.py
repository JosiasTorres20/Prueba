import pandas as pd
import bcrypt
import os
from app.DAO import main_dao
from app.DAO import jefe_dao
from app.DAO.gerente_dao import GerenteDao

def limpiar():
    return os.system('cls' if os.name == 'nt' else 'clear')

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
                pendientes, total_pendiente = jefe_dao.verificar_jefe_asignar_depo()
                if pendientes:
                    print(f"Hay {total_pendiente} usuarios jefe sin departamento asignado ")
            return info_usuario
        else:
            intentos +=1
            print("Usuario o Contaseña incorrectos")
            if intentos >= 3:
                bloqueo_clave(usuario)             
    return None


def bloqueo_clave(usuario):
    print("Clave Bloqueada.\033[03;30m/se necesita reestablecerla\033[0m")
    root_psw = str(input("Ingrese clave del Gerente\n\033[03;30m>>> \033[0m"))
    if main_dao.validar_credenciales("root",root_psw):
        nueva_psw = str(input("Ingrese la nueva clave\n\033[03;30m>>> \033[0m"))
        hashed_nueva_psw = bcrypt.hashpw(nueva_psw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        main_dao.actualizar_psw(usuario, hashed_nueva_psw)
        print("\033[03;30mClave actualizada con exito\033[0m")
    else:
        print("Clave del Gerente incorrecta")
def hash_claves(psw):
    return bcrypt.hashpw(psw.encode('utf-8'), bcrypt.gensalt())
def revision_del_hash(psw, hash_claves):
    if isinstance(hash_claves, str):
        hash_claves = hash_claves.encode('utf-8')
    return bcrypt.checkpw(psw.encode('utf-8'), hash_claves)

def cambiar_contrasena(usuario):
    actual_psw = input("Ingrese su contraseña actual: ")
    info_usuario = main_dao.validar_credenciales(usuario, actual_psw)

    if info_usuario:
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

    data_del_perfil={
        'ID': info_usuario.get('ID', 'No disponible'),
        'NOMBRE COMPLETO': f"{info_usuario['NOMBRE']} {info_usuario['APELLIDO']}",
        'TELEFONO': info_usuario.get('TELEFONO', 'No disponible'),
        'MAIL': info_usuario.get('USUARIO', 'No disponible'),
        'INICIO CONTRATO': info_usuario.get('FECHA_INICIO', 'No disponible'),
        'USUARIO': info_usuario.get('USUARIO', 'No disponible'),
        'DEPARTAMENTO': info_usuario.get('DEPARTAMENTO', 'No disponible')
    }

    df = pd.DataFrame([data_del_perfil])
    print(df.to_string(index=False))

