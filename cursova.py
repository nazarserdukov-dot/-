import streamlit as st
import pandas as pd

st.title("Кіберінциденти")

# форма
date = st.date_input("Дата")
type_inc = st.selectbox("Тип", ["Phishing", "Malware", "DDoS"])
severity = st.selectbox("Рівень", ["low", "medium", "high"])
desc = st.text_area("Опис")

if st.button("Додати"):
    new_data = {
        "date": str(date),
        "type": type_inc,
        "severity": severity,
        "description": desc
    }
    df = pd.DataFrame([new_data])
    try:
        old = pd.read_csv("data.csv")
        df = pd.concat([old, df])
    except:
        pass
    df.to_csv("data.csv", index=False)
    st.success("Додано!")

# аналітика
st.subheader("Аналітика")

try:
    df = pd.read_csv("data.csv")
    st.dataframe(df)

    st.write("Кількість інцидентів:", len(df))
    st.bar_chart(df["type"].value_counts())

except:
    st.warning("Немає даних")
