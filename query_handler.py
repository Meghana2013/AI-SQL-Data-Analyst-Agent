import sqlite3
from agent import generate_sql

def ask_question(question):
    query = generate_sql(question)

    # Clean markdown artifacts if any
    query = query.replace("```sql", "").replace("```", "").strip()

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as e:
        conn.close()
        return query, f"Error executing query: {str(e)}"

    conn.close()

    # 🔥 Correct and consistent result handling

    if result:
        # Case 1: Multiple rows (GROUP BY, ORDER BY, etc.)
        if len(result) > 1:
            # If 2 columns → treat as category + value
            if len(result[0]) == 2:
                clean_result = [
                    {"category": r[0], "value": r[1]} for r in result
                ]
            else:
                clean_result = result

        # Case 2: Single row, single column (e.g., AVG, COUNT)
        elif len(result[0]) == 1:
            clean_result = result[0][0]

        # Case 3: Single row, multiple columns
        else:
            clean_result = result

    else:
        clean_result = "No results found"

    return query, clean_result