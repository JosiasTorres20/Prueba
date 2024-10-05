from app.DAO.database import get_db

class empleado_dao:
    
    @staticmethod
    def obtener_info():
        db = get_db()
        cursor = db.cursor()