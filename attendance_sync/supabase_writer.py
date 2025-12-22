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

    def get_employee_mappings(self):
        try:
            response = self.client.table('employees').select('id, attendance_device_id').execute()
            mappings = {str(row['attendance_device_id']): row['id'] for row in response.data}
            logger.info(f"Loaded {len(mappings)} employee mappings")
            return mappings
        except Exception as e:
            logger.error(f"Failed to get employee mappings: {e}")
            raise

    def upsert_records(self, records):
        mappings = self.get_employee_mappings()
        # Group records by employee and date to aggregate in/out times
        grouped = {}
        for record in records:
            employee_uuid = mappings.get(str(record['employeeID']))
            if not employee_uuid:
                logger.warning(f"No mapping found for employeeID {record['employeeID']}, skipping")
                continue
            date_str = record['authDate'].isoformat() if record['authDate'] else None
            if not date_str:
                continue
            key = (employee_uuid, date_str)
            if key not in grouped:
                grouped[key] = {
                    'employee_id': employee_uuid,
                    'date': date_str,
                    'office_in_time': None,
                    'office_out_time': None,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
            # Update in/out times based on direction
            if record['direction'].lower() == 'in' and record['authTime']:
                grouped[key]['office_in_time'] = record['authTime'].isoformat()
            elif record['direction'].lower() == 'out' and record['authTime']:
                grouped[key]['office_out_time'] = record['authTime'].isoformat()
        data = list(grouped.values())
        if not data:
            logger.info("No valid records to upsert after grouping")
            return
        try:
            response = self.client.table('attendance_records').upsert(
                data,
                on_conflict='employee_id,date'
            ).execute()
            logger.info(f"Upserted {len(data)} records to Supabase")
            return response
        except Exception as e:
            logger.error(f"Failed to upsert records: {e}")
            raise