import os
import pandas as pd

# 1. Load the Excel file (replace 'sample_data.xlsx' with your actual file path)
# If your data is on a specific sheet, add sheet_name='Sheet1'
df = pd.read_excel("UG5_ssis_sqls.xlsx")

# 2. Clean up column names (stripping any accidental hidden spaces)
df.columns = df.columns.str.strip()

# 3. Create an output directory for the SQL files
output_dir = "ug5_ssis_sqls"
os.makedirs(output_dir, exist_ok=True)

# 4. Iterate through each row to create and populate the files
for index, row in df.iterrows():
    # Extract the file name and the SQL content
    filename = str(row["file_name"]).strip()
    sql_content = str(row["sqltextinfo"])

    # Skip if the filename or content is missing/NaN
    if pd.isna(row["file_name"]) or pd.isna(row["sqltextinfo"]):
        print(f"Skipping row {index} due to missing filename or content.")
        continue

    # Ensure the filename ends with .sql
    if not filename.endswith(".sql"):
        filename += ".sql"

    # Define the full file path
    file_path = os.path.join(output_dir, filename)

    # 5. Write the SQL text into the file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(sql_content)

    print(f"Created: {file_path}")

print("\nAll files have been successfully processed from the Excel sheet!")
