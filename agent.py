from langchain_groq import ChatGroq
import os

def generate_sql(question):
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.3-70b-versatile"
    )

    prompt = f"""
You are a SQL expert.

Table name: data_table

Columns:
Age, Sex, ChestPainType, RestingBP, Cholesterol,
FastingBS, RestingECG, MaxHR, ExerciseAngina

Rules:
- Use exact column names
- ALWAYS return category column first, then aggregated value
- For GROUP BY queries, use:
  SELECT category_column, AGG(column) FROM data_table GROUP BY category_column
- For single value queries, return only one column
- Return ONLY raw SQL
- DO NOT use ``` or markdown
- DO NOT explain anything

Examples:

Q: average cholesterol by sex
A: SELECT Sex, AVG(Cholesterol) FROM data_table GROUP BY Sex;

Q: average restingbp
A: SELECT AVG(RestingBP) FROM data_table;

Q: maximum heart rate
A: SELECT MAX(MaxHR) FROM data_table;

Question: {question}
"""

    response = llm.invoke(prompt)

    # 🔥 Clean output (extra safety)
    query = response.content.strip()
    query = query.replace("```sql", "").replace("```", "").strip()

    return query
