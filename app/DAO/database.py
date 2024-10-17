import mysql.connector

class Conexion:
    def __init__(self):
        self.__host = 'localhost'
        self.__user = 'root'
        self.__password = ''
        self.__db_name = 'empresa'
        self._conexion = None

    def get_conexion(self):
        if self._conexion is None or not self._conexion.is_connected():
            self._conexion = mysql.connector.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.__db_name
            )
        return self._conexion

    def ejecutar_query(self, query, params=None):
        conexion = self.get_conexion() 
        cursor = conexion.cursor(dictionary=True)
        tipo_de_query = query.strip().split()[0].upper()

        try:
            if tipo_de_query == 'SELECT':
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                return resultados
            
            elif tipo_de_query in ('DELETE', 'UPDATE', 'INSERT'):
                cursor.execute(query, params)
                conexion.commit()
                if tipo_de_query == 'INSERT':
                    return cursor.lastrowid
                return cursor.rowcount
            else:
                raise ValueError(f"El tipo de query {tipo_de_query} no es correcto.")
        except mysql.connector.Error as error:
            print(f"Error ejecutando la consulta: {error}")
            conexion.rollback()
            return None 
        finally:
            cursor.close()  
    def desconectar(self):
        if self._conexion and self._conexion.is_connected():
            self._conexion.close()