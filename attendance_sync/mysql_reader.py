import pymysql
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
from logger import logger

class MySQLReader:
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE,
                connect_timeout=5,
                autocommit=True  # Enable autocommit to see new data
            )
            logger.info("Connected to MySQL database")
        except pymysql.Error as e:
            logger.error(f"Failed to connect to MySQL: {e}")
            raise

    def ensure_connection(self):
        """Reconnect if connection is lost"""
        try:
            self.conn.ping(reconnect=True)
        except pymysql.Error:
            self.connect()

    def get_unsynced_records(self):
        self.ensure_connection()
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
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
        self.ensure_connection()
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