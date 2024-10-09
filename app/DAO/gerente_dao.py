from app.DAO.database import get_db
import mysql.connector
import random
import bcrypt



class GerenteDao:
    
    @staticmethod 
    def obtener_gerente_root():
        db = get_db()
        cursor = db.cursor(dictionary = True)
        cursor.execute('SELECT * FROM EMPLEADO WHERE USUARIO = %s AND ES_GERENTE = TRUE',('root',))
        gerente_data = cursor.fetchone()
        cursor.close()
        db.close()
        return gerente_data   
    @staticmethod
    def generar_usuario_mail(nombre,apellido):
        db = get_db()
        cursor = db.cursor()

        generar_mail = f"{nombre}.{apellido}@empresa.cl".lower()
        generar_usuario = f"{nombre}".lower()

    
        while True:
            cursor.execute('SELECT COUNT(*) FROM EMPLEADO WHERE MAIL = %s', (generar_mail,))
            validar_mail = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM EMPLEADO WHERE USUARIO = %s', (generar_usuario,))
            validar_usuario = cursor.fetchone()[0]

            if validar_mail == 0 and validar_usuario == 0 :
                break
            else:
                numero_random = random.randint(10,99)
                generar_mail = f"{nombre}.{apellido}{numero_random}@empresa.cl"
                generar_usuario = f"{nombre}{numero_random}"
        cursor.close()
        db.close()

        return generar_usuario, generar_mail
