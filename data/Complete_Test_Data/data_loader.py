import os
import csv
from typing import List, Dict


def get_data(path: str) -> List[Dict[str, str]]:
    """
    Load test data from CSV or Excel (.xlsx). Returns a list of dict rows.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")

    lower = path.lower()
    if lower.endswith('.csv'):
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader]
    elif lower.endswith(('.xls', '.xlsx')):
        # import pandas only when needed to avoid requiring it for CSV-only runs
        try:
            import pandas as pd
        except Exception:
            raise RuntimeError("pandas is required to read Excel files (install pandas and openpyxl)")
        df = pd.read_excel(path, engine='openpyxl')
        # Convert NaN to empty string and then to dicts of strings
        df = df.fillna('')
        return df.astype(str).to_dict(orient='records')
    else:
        raise ValueError("Unsupported data file type. Provide .csv or .xlsx")
