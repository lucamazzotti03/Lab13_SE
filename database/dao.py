from database.DB_connect import DBConnect
from model.gene import Gene
from model.interazione import Interazione


class DAO:


    @staticmethod
    def get_interazioni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM interazione"""

        cursor.execute(query)

        for row in cursor:
            result.append(Interazione(row["id_gene1"], row["id_gene2"], row["tipo"], row["correlazione"]))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_geni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM gene where cromosoma > 0"""

        cursor.execute(query)

        for row in cursor:
            result.append(Gene(row["id"], row["funzione"], row["essenziale"], row["cromosoma"]))

        cursor.close()
        conn.close()
        return result


