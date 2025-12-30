from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

def show_supabase_data():
    try:
        print("Connecting to Supabase...")
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("Connected successfully.")
        response = client.table("attendance_logs").select("*").limit(5).execute()
        data = response.data
        print(f"Total records fetched: {len(data)}")
        if data:
            print("First 5 records:")
            for record in data:
                print(record)
        else:
            print("No records found in Supabase.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    show_supabase_data()