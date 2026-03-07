import csv
import mysql.connector

csv_path = "mental_health_tracker.csv"

def iter_entries(csv_path: str = csv_path):
    with open(csv_path, newline="", encoding = "utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row

def preview_entries(csv_path: str = csv_path, n_rows: int = 3):
    for i, row in enumerate(iter_entries(csv_path), start = 1):
        print(f"--- CSV row {i} ---")
        print(row)
        if i >= n_rows:
            break
        
def insert_habits(conn):
    cur = conn.cursor()
    with open("habits.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT IGNORE INTO habits (habit_id, habit_name, entry_date, notes)
                VALUES (%s,%s, %s, %s)
            """, (row["habit_id"], row["habit_name"], row["entry_date"], row["notes"]))
    conn.commit()

def insert_habit_logs(conn):
    cur = conn.cursor()
    with open("habit_logs.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT IGNORE INTO habit_logs (habit_log_id, habit_id, entry_date, completed)
                VALUES (%s,%s, %s, %s)
            """, (row["habit_log_id"], row["habit_id"], row["entry_date"], row["completed"]))
    conn.commit()

def insert_daily_entries(conn):
    cur = conn.cursor()
    with open("daily_entries.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT IGNORE INTO daily_entries (entry_date, hours_slept, mood_level, stress_level, energy_level, notes)
                VALUES (%s,%s, %s, %s, %s, %s)
            """, (row["entry_date"], row["hours_slept"], row["mood_level"], row["stress_level"], row["energy_level"], row["notes"]))
    conn.commit()

def insert_alerts(conn):
    cur = conn.cursor()
    with open("alerts.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT IGNORE INTO alerts (entry_date, alert_id, alert_type, alert_message)
                VALUES (%s,%s, %s, %s)
            """, (row["entry_date"], row["alert_id"], row["alert_type"], row["alert_message"]))
    conn.commit()
