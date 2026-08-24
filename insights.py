from langchain_groq import ChatGroq
import os

def generate_insight(question, result):
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
model_name="openai/gpt-oss-20b"    )

    prompt = f"""
You are a data analyst.

User question:
{question}

Result:
{result}

Generate a clear insight:
- Highlight key differences or trends
- Use percentages if possible
- Avoid vague words like "slightly"
- Be specific and meaningful
- Keep it short (2-3 lines)

Do NOT repeat the numbers blindly.
"""

    response = llm.invoke(prompt)
    return response.content.strip()
