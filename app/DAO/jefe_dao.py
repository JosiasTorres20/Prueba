from app.DAO.database import get_db

def verificar_jefe_asignar_depo():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    query = """ 
            SELECT COUNT(*) AS TODOS_LOS_PENDIENTES
            FROM EMPLEADO 
            WHERE ES_JEFE = TRUE AND DEPTO_ID IS FULL
            """
    cursor.execute(query)
    resultado = cursor.fetchone()

    total_pendiente = resultado['TODOS_LOS_PENDIENTES']

    verificar_si_hay_pendientes = total_pendiente > 0
    
    cursor.close()
    db.close()
    return verificar_si_hay_pendientes, total_pendiente
