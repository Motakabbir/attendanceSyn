import mysql.connector
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from logger import logger

class MySQLReader:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE
            )
            logger.info("Connected to MySQL database")
        except mysql.connector.Error as e:
            logger.error(f"Failed to connect to MySQL: {e}")
            raise

    def get_unsynced_records(self):
        cursor = self.conn.cursor(dictionary=True)
        query = """
        SELECT employeeID, authDateTime, authDate, authTime, direction, deviceName, deviceSn, personName, cardNo
        FROM attlog
        WHERE synced_at IS NULL OR updated_at > synced_at
        """
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        return records

    def mark_synced(self, records):
        cursor = self.conn.cursor()
        for record in records:
            cursor.execute("""
            UPDATE attlog
            SET synced_at = NOW()
            WHERE employeeID = %s AND authDateTime = %s AND deviceSn = %s
            """, (record['employeeID'], record['authDateTime'], record['deviceSn']))
        self.conn.commit()
        cursor.close()
        logger.info(f"Marked {len(records)} records as synced")