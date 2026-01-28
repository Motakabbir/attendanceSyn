from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
from logger import logger
from datetime import datetime

class SupabaseWriter:
    def __init__(self):
        try:
            self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            logger.info("Connected to Supabase")
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {e}")
            raise

    def upsert_records(self, records, batch_size=100):
        # Transform records to list of dicts for raw attendance logs
        data = []
        for record in records:
            def serialize_datetime(value):
                if hasattr(value, 'isoformat'):
                    return value.isoformat()
                elif isinstance(value, str):
                    return value
                else:
                    return str(value) if value else None

            # Handle direction field - convert to int or None
            direction_value = record.get('direction')
            if direction_value == '' or direction_value is None:
                direction_value = None
            else:
                try:
                    direction_value = int(direction_value)
                except (ValueError, TypeError):
                    direction_value = None

            transformed = {
                'authDate': serialize_datetime(record.get('authDate')),
                'direction': direction_value,
                'employeeID': record['employeeID'],
                'personName': record['personName'],
                'authDateTime': serialize_datetime(record.get('authDateTime')),
                'deviceName': record['deviceName'],
                'authTime': serialize_datetime(record.get('authTime')),
                'cardNo': record['cardNo'],
                'deviceSn': record['deviceSn']
            }
            data.append(transformed)

        # Deduplicate by (employeeID, authDateTime, deviceSn)
        unique = {}
        for item in data:
            key = (item['employeeID'], item['authDateTime'], item['deviceSn'])
            if key not in unique:
                unique[key] = item
        deduped_data = list(unique.values())

        # Batch upsert
        total = len(deduped_data)
        responses = []
        for i in range(0, total, batch_size):
            batch = deduped_data[i:i+batch_size]
            try:
                response = self.client.table('attendance_logs').upsert(
                    batch,
                    on_conflict='employeeID,authDateTime,deviceSn'
                ).execute()
                logger.info(f"Upserted batch {i//batch_size+1}: {len(batch)} records to Supabase")
                responses.append(response)
            except Exception as e:
                logger.error(f"Failed to upsert batch {i//batch_size+1}: {e}")
                raise
        logger.info(f"Upserted {total} records to Supabase in {((total-1)//batch_size)+1} batches.")
        return responses

    def select_table(self):
        try:
            response = self.client.table('attendance_logs').select('*').execute()
            logger.info(f"Selected records from attendance_logs: {response.data}")
            return response.data
        except Exception as e:
            logger.error(f"Failed to select from table: {e}")
            return []