import time
import signal
import sys
from mysql_reader import MySQLReader
from supabase_writer import SupabaseWriter
from config import SYNC_INTERVAL_SECONDS
from logger import logger

running = True

def signal_handler(sig, frame):
    global running
    logger.info("Received shutdown signal, stopping sync...")
    running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def sync():
    reader = MySQLReader()
    writer = SupabaseWriter()
    existing_records = writer.select_table()
    # Now proceed with sync

    while running:
        try:
            records = reader.get_unsynced_records()
            if records:
                logger.info(f"Found {len(records)} records to sync")
                writer.upsert_records(records)
                reader.mark_synced(records)
                logger.info("Sync completed successfully")
            else:
                logger.info("No new records to sync")

            time.sleep(SYNC_INTERVAL_SECONDS)
        except Exception as e:
            logger.error(f"Sync failed: {e}")
            time.sleep(SYNC_INTERVAL_SECONDS)  # Wait before retrying

if __name__ == "__main__":
    logger.info("Starting attendance sync service")
    sync()
    logger.info("Attendance sync service stopped")