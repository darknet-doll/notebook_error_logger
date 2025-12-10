# notebook_error_logger/airtable_sync.py
import os
import pandas as pd
from pyairtable import Table
from .logger import PROJECT_TYPE

class AirTable:
    def __init__(self, base_id: str = None, token: str = None, ):
        self.airtable_base_id = base_id or os.getenv("AIRTABLE_BASE_ID")
        self.airtable_token = token or os.getenv("AIRTABLE_TOKEN")

        if not (self.airtable_base_id and self.airtable_token):
            raise ValueError("Missing Airtable credentials. Set AIRTABLE_TOKEN and AIRTABLE_BASE_ID.")


    def write(
        self,
        df,
        table_name: str = "SpankBank",
        link_table_name: str = "Impact Conversion",  # Linked table
        link_field_name: str = "project_type",       # Field in linked table
        project_type_value: str = PROJECT_TYPE # Fixed linked record value
    ):
        """
        Uploads a pandas DataFrame of errors to Airtable.
        Resolves the linked 'project_type' field once ('data science notebook') and reuses its record ID.
        Prints a summary only after all records are processed.

        Args:
            table_name (str, optional): Airtable table name
            link_table_name (str, optional): Name for the linked impact conversion table
            link_field_name (str, optional): Name for the field in the linked table
            project_type_value (str, optional): Value in the field `link_field_name` to search for to establish conversion rate
        """
        errors_table = Table(self.airtable_token, self.airtable_base_id, table_name)
        impact_conversion_table = Table(self.airtable_token, self.airtable_base_id, link_table_name)

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

    def read(
        self,
        table_name: str = "SpankBank"
    ) -> pd.DataFrame:
        """
        Read an Airtable table into a pandas DataFrame.

        Args:
            table_name (str, optional): Airtable table name

        Returns:
            pd.DataFrame: A DataFrame containing all records from Airtable.
        """

        # Connect to airtable and read the data from table `table_name`.
        table = Table(self.airtable_token, self.airtable_base_id, table_name)
        records = table.all()

        if not records:
            print("⚠️ No records found in Airtable table.")
            return pd.DataFrame()

        # Flatten Airtable record fields into a DataFrame
        df = pd.DataFrame([r["fields"] for r in records])

        print(f"✅ Retrieved {len(df)} records from Airtable.")
        return df
