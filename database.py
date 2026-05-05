import sqlite3

def create_db(df, db_name="data.db"):
    conn = sqlite3.connect(db_name)
    df.to_sql("data_table", conn, if_exists="replace", index=False)
    conn.close()