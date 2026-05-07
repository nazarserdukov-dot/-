import streamlit as st
import pandas as pd
import os

# Налаштування сторінки
st.set_page_config(page_title="Cyber Tracker", layout="wide")

DATA_FILE = "data.csv"

# Функція завантаження даних
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # Перетворюємо дату у формат datetime для графіків
        df['date'] = pd.to_datetime(df['date'])
        return df
    return pd.DataFrame(columns=["date", "type", "severity", "description"])

# --- БОКОВА ПАНЕЛЬ (КЕРУВАННЯ) ---
st.sidebar.header("Меню керування")
page = st.sidebar.selectbox("Перейти до розділу:", ["➕ Реєстрація інцидентів", "📈 Аналітика та порівняння"])

# --- СТОРІНКА 1: ДОДАТИ ІНЦИДЕНТ ---
if page == "➕ Реєстрація інцидентів":
    st.title("🛡️ Новий запис про кіберінцидент")
    st.info("Заповніть форму нижче, щоб додати подію до бази даних.")
    
    with st.form("incident_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Дата виявлення")
            type_inc = st.selectbox("Тип загрози", ["Phishing", "Malware", "DDoS", "SQL Injection", "Ransomware"])
        with col2:
            severity = st.select_slider("Рівень важливості", options=["low", "medium", "high"])
        
        desc = st.text_area("Детальний опис інциденту")
        
        submit = st.form_submit_button("Зберегти дані")

    if submit:
        new_row = {
            "date": date,
            "type": type_inc,
            "severity": severity,
            "description": desc
        }
        df_new = pd.DataFrame([new_row])
        df_existing = load_data()
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
        df_final.to_csv(DATA_FILE, index=False)
        st.success("✅ Інцидент успішно зареєстровано!")

# --- СТОРІНКА 2: АНАЛІТИКА ТА ПОРІВНЯННЯ ---
elif page == "📈 Аналітика та порівняння":
    st.title("📊 Аналітичний дашборд")
    
    df = load_data()

    if not df.empty:
        # Верхні показники (Метрики)
        total = len(df)
        st.metric("Загальна кількість зафіксованих подій", total)
        
        st.divider()

        # ЛІНІЙНИЙ ГРАФІК (Динаміка за часом)
        st.subheader("📉 Динаміка інцидентів у часі")
        # Групуємо кількість інцидентів за датами
        timeline_df = df.groupby('date').size().reset_index(name='Кількість')
        timeline_df = timeline_df.set_index('date')
        st.line_chart(timeline_df)

        # СЕКЦІЯ ПОРІВНЯННЯ
        st.subheader("⚖️ Порівняння параметрів")
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.write("**Кількість за типами:**")
            type_counts = df["type"].value_counts()
            st.bar_chart(type_counts)
            
        with col_right:
            st.write("**Розподіл за критичністю:**")
            severity_summary = df.groupby('severity').size()
            st.table(severity_summary)

        # ПОВНА ТАБЛИЦЯ
        with st.expander("Переглянути всі сирі дані"):
            st.dataframe(df.sort_values(by='date', ascending=False), use_container_width=True)
            
    else:
        st.warning("Дані відсутні. Будь ласка, додайте інформацію на першій сторінці.")
