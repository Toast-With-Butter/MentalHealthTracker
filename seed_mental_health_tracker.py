import csv

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