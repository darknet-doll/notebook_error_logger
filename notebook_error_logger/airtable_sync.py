# colab_error_logger/airtable_sync.py
import os
import pandas as pd
from pyairtable import Table

def write_airtable(
    df,
    airtable_token: str = None,
    base_id: str = None,
    table_name: str = "Errors",
    link_table_name: str = "Impact Conversion",  # Linked table
    link_field_name: str = "project_type",       # Field in linked table
    project_type_value: str = "data science notebook" # Fixed linked record value
):
    """
    Uploads a pandas DataFrame of errors to Airtable.
    Resolves the linked 'project_type' field once ('data science notebook') and reuses its record ID.
    Prints a summary only after all records are processed.
    """
    airtable_token = airtable_token or os.getenv("AIRTABLE_TOKEN")
    base_id = base_id or os.getenv("AIRTABLE_BASE_ID")

    if not (airtable_token and base_id):
        raise ValueError("Missing Airtable credentials. Set AIRTABLE_TOKEN and AIRTABLE_BASE_ID.")

    errors_table = Table(airtable_token, base_id, table_name)
    impact_conversion_table = Table(airtable_token, base_id, link_table_name)

    # 🔍 Lookup linked record ID once
    records = impact_conversion_table.all(formula=f"{{{link_field_name}}} = '{project_type_value}'")
    if not records:
        raise ValueError(
            f"No record found for project_type '{project_type_value}' in '{link_table_name}'. "
            "Please ensure the linked record exists."
        )

    project_type_id = records[0]["id"]

    # Track results
    failed_records = []

    # 🚀 Upload records
    for _, row in df.iterrows():
        record_data = {
            "project_type": [project_type_id],
            "project_name": row.get("project_name"),
            "error_type": row.get("error_type"),
            "date": row.get("date"),
        }

        try:
            errors_table.create(record_data)
        except Exception as e:
            failed_records.append({
                "project_name": row.get("project_name"),
                "error_type": row.get("error_type"),
                "error": str(e)
            })

    # 📋 Final summary
    if failed_records:
        print("\n⚠️ Some records failed to upload:")
        for r in failed_records:
            print(f"  - {r['project_name']} ({r['error_type']}): {r['error']}")
    else:
        print("\n✅ All records uploaded successfully to Airtable.")

def read_airtable(
    airtable_token: str = None,
    base_id: str = None,
    table_name: str = "Errors"
) -> pd.DataFrame:
    """
    Read an Airtable table into a pandas DataFrame.

    Args:
        airtable_token (str, optional): Airtable API token (uses env if None)
        base_id (str, optional): Airtable base ID (uses env if None)
        table_name (str, optional): Airtable table name

    Returns:
        pd.DataFrame: A DataFrame containing all records from Airtable.
    """
    airtable_token = airtable_token or os.getenv("AIRTABLE_TOKEN")
    base_id = base_id or os.getenv("AIRTABLE_BASE_ID")

    if not (airtable_token and base_id):
        raise ValueError("Missing Airtable credentials. Set AIRTABLE_TOKEN and AIRTABLE_BASE_ID.")
    
    # Connecting to airtable dataframe.
    table = Table(airtable_token, base_id, table_name)
    records = table.all()

    if not records:
        print("⚠️ No records found in Airtable table.")
        return pd.DataFrame()

    # Flatten Airtable record fields into a DataFrame
    df = pd.DataFrame([r["fields"] for r in records])

    print(f"✅ Retrieved {len(df)} records from Airtable.")
    return df
