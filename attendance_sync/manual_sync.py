from mysql_reader import MySQLReader
from supabase_writer import SupabaseWriter
from logger import logger

def manual_sync():
    try:
        logger.info("Starting manual sync...")
        reader = MySQLReader()
        records = reader.get_unsynced_records()
        if records:
            logger.info(f"Found {len(records)} unsynced records.")
            writer = SupabaseWriter()
            writer.upsert_records(records)
            reader.mark_as_synced(records)
            logger.info("Manual sync completed.")
        else:
            logger.info("No unsynced records found.")
    except Exception as e:
        logger.error(f"Manual sync failed: {e}")

if __name__ == "__main__":
    manual_sync()