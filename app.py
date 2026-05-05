import streamlit as st
import pandas as pd
import time
from data_loader import load_csv
from database import create_db
from query_handler import ask_question
from insights import generate_insight

st.title("📊 AI SQL Data Analyst Agent")

# Session history
if "history" not in st.session_state:
    st.session_state.history = []

uploaded_file = st.file_uploader("📁 Upload CSV", type=["csv"])

if uploaded_file:
    df = load_csv(uploaded_file)
    st.write(df.head())

    create_db(df)

    question = st.text_input("Ask a question")

    if question:
        start_time = time.time()

        sql_query, answer = ask_question(question)

        end_time = time.time()
        execution_time = round(end_time - start_time, 2)

        # Save history
        st.session_state.history.append({
            "question": question,
            "query": sql_query
        })

        # 🔹 SQL Display
        st.subheader("🧠 Generated SQL")
        st.code(sql_query, language="sql")

        st.subheader("✅Answer")

        # ❌ Error handling
        if isinstance(answer, str) and answer.startswith("Error"):
            st.error(answer)

        # ✅ Numeric result
        elif isinstance(answer, (int, float)):
            value = round(answer, 2)
            st.success(value)
            st.metric(label="Computed Value", value=value)

        # ✅ List result (grouped / multi-row)
        elif isinstance(answer, list):
            try:
                df_result = pd.DataFrame(answer)

                # Rename columns
                if "category" in df_result.columns and "value" in df_result.columns:
                    df_result = df_result.rename(columns={
                        "category": "Group",
                        "value": "Value"
                    })
                    df_result["Value"] = df_result["Value"].round(2)

                # 📊 Table
                st.subheader("📊Result Table")
                st.dataframe(df_result, use_container_width=True)

                # 📥 Download
                csv = df_result.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥Download Results",
                    data=csv,
                    file_name="results.csv",
                    mime="text/csv"
                )

                # 📊 SMART Visualization
                st.subheader("📊Visualization")

                if "Group" in df_result.columns:
                    df_plot = df_result.set_index("Group")

                    # 🔥 Smart selection
                    if len(df_plot) <= 5:
                        st.bar_chart(df_plot)
                    else:
                        st.line_chart(df_plot)

                else:
                    if len(df_result.columns) == 1:
                        st.line_chart(df_result)
                    else:
                        st.bar_chart(df_result)

            except Exception:
                st.warning("Could not generate visualization")

        else:
            st.write(answer)

        # 🧠 Insight (NEW)
        try:
            st.subheader("💡Insight")
            insight = generate_insight(question, answer)
            st.info(insight)
        except Exception:
            st.warning("Could not generate insight")

        # ⏱ Time
        st.caption(f"⏱ Execution Time: {execution_time}s")

# 📌 Sidebar history
st.sidebar.title("📜Query History")

for item in reversed(st.session_state.history):
    st.sidebar.write(f"**Q:** {item['question']}")
    st.sidebar.code(item['query'], language="sql")