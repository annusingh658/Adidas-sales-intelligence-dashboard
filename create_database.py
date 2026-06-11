import pandas as pd
import sqlite3

# Read Excel file
df = pd.read_excel("Adidas.xlsx")

# Create SQLite database
conn = sqlite3.connect("adidas.db")

# Store data in table named sales
df.to_sql("sales", conn, if_exists="replace", index=False)

# Close connection
conn.close()

print("Database created successfully!")