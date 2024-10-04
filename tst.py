#si tienen problemas con el hash y los usuarios borren aqui el usuario y lo vuelven a cargar a la bs
#nasheeei
import bcrypt
from app.DAO.database import get_db
password = "root"
hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')

db = get_db()
cursor = db.cursor()

#obvio cambien el usuario a borrar 
cursor.execute("DELETE FROM EMPLEADO WHERE USUARIO = 'root'")
db.commit()

# y cambien la query segun el user
insert_query = """
INSERT INTO EMPLEADO (NOMBRE, APELLIDO, TELEFONO, MAIL, SALARIO, FECHA_INICIO, ES_JEFE, ES_GERENTE, USUARIO, PSW)
VALUES ('Gerente', 'General', '12345678', 'gerente@empresa.cl', 10000.00, '2024-02-26', FALSE, TRUE, 'root', %s)
"""
cursor.execute(insert_query, (hashed_password,))
db.commit()


cursor.close()
db.close()