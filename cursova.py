import streamlit as st
import pandas as pd
import os

#Налаштування файлу даних
DATA_FILE = "data.csv"

#Функція для завантаження даних
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["date", "type", "severity", "description"])

#Навігація в боковій панелі
st.sidebar.title("Навігація")
page = st.sidebar.radio("Оберіть сторінку:", ["Додати інцидент", "Аналітика та порівняння"])

#ДОДАТИ ІНЦИДЕНТ
if page == "Додати інцидент":
    st.title("🛡️ Реєстрація кіберінцидентів")
    
    with st.form("incident_form"):
        date = st.date_input("Дата події")
        type_inc = st.selectbox("Тип інциденту", ["Phishing", "Malware", "DDoS", "SQL Injection", "Ransomware"])
        severity = st.select_slider("Рівень загрози", options=["low", "medium", "high"])
        desc = st.text_area("Опис інциденту")
        
        submit = st.form_submit_button("Зберегти у базу")

    if submit:
        new_data = {
            "date": str(date),
            "type": type_inc,
            "severity": severity,
            "description": desc
        }
        df_new = pd.DataFrame([new_data])
        
        df_existing = load_data()
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
        df_final.to_csv(DATA_FILE, index=False)
        
        st.success(f"Інцидент '{type_inc}' успішно додано!")

#АНАЛІТИКА ТА ПОРІВНЯННЯ
elif page == "Аналітика та порівняння":
    st.title("📊 Аналітика та порівняння")
    
    df = load_data()

    if not df.empty:
        #Загальна таблиця
        st.subheader("Список усіх інцидентів")
        st.dataframe(df, use_container_width=True)

        #Розподіл на колонки для статистики
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Загальна кількість", len(df))
        
        with col2:
            most_common = df["type"].mode()[0] if not df["type"].empty else "Н/Д"
            st.metric("Найчастіша загроза", most_common)

        st.divider()

        #Порівняння за типами (Графік)
        st.subheader("Порівняння кількості за типами")
        type_counts = df["type"].value_counts()
        st.bar_chart(type_counts)

        #Порівняння за рівнем важливості
        st.subheader("Аналіз критичності")
        severity_counts = df["severity"].value_counts()
        st.pie_chart(severity_counts)

        #Детальне порівняння (Таблиця агрегації)
        st.subheader("Зведена аналітика")
        summary_df = df.groupby('type').agg(
            кількість=('type', 'count')
        ).sort_values(by='кількість', ascending=False)
        
        st.table(summary_df)
        
    else:
        st.warning("База даних порожня. Додайте перший інцидент на відповідній сторінці.")
