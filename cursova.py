import streamlit as st
import pandas as pd
import os

# =========================

# НАЛАШТУВАННЯ СТОРІНКИ

# =========================

st.set_page_config(
page_title="Cyber Tracker",
page_icon="🛡️",
layout="wide"
)

DATA_FILE = "data.csv"

# =========================

# СТВОРЕННЯ ФАЙЛУ БД

# =========================

if not os.path.exists(DATA_FILE):
pd.DataFrame(
columns=["date", "type", "severity", "description"]
).to_csv(DATA_FILE, index=False)

# =========================

# ЗАВАНТАЖЕННЯ ДАНИХ

# =========================

def load_data():
try:
df = pd.read_csv(DATA_FILE)

```
    if not df.empty:
        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        df = df.dropna(subset=["date"])

    return df

except Exception as e:
    st.error(f"Помилка читання файлу: {e}")

    return pd.DataFrame(
        columns=[
            "date",
            "type",
            "severity",
            "description"
        ]
    )
```

# =========================

# БОКОВЕ МЕНЮ

# =========================

st.sidebar.title("🛡️ Cyber Tracker")

page = st.sidebar.radio(
"Оберіть розділ",
[
"➕ Реєстрація інцидентів",
"📊 Аналітика"
]
)

# =========================

# РЕЄСТРАЦІЯ ІНЦИДЕНТІВ

# =========================

if page == "➕ Реєстрація інцидентів":

```
st.title("➕ Реєстрація кіберінциденту")

with st.form(
    "incident_form",
    clear_on_submit=True
):

    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input(
            "Дата інциденту"
        )

        type_inc = st.selectbox(
            "Тип загрози",
            [
                "Phishing",
                "Malware",
                "DDoS",
                "SQL Injection",
                "Ransomware"
            ]
        )

    with col2:
        severity = st.selectbox(
            "Критичність",
            [
                "low",
                "medium",
                "high"
            ]
        )

    desc = st.text_area(
        "Опис інциденту"
    )

    submit = st.form_submit_button(
        "💾 Зберегти"
    )

    if submit:

        new_row = pd.DataFrame([
            {
                "date": date.strftime("%Y-%m-%d"),
                "type": type_inc,
                "severity": severity,
                "description": desc
            }
        ])

        old_df = load_data()

        result_df = pd.concat(
            [old_df, new_row],
            ignore_index=True
        )

        result_df.to_csv(
            DATA_FILE,
            index=False
        )

        st.success(
            "Інцидент успішно додано!"
        )
```

# =========================

# АНАЛІТИКА

# =========================

elif page == "📊 Аналітика":

```
st.title("📊 Аналітичний дашборд")

df = load_data()

if df.empty:

    st.warning(
        "База даних порожня."
    )

else:

    # -------------------
    # МЕТРИКИ
    # -------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Всього подій",
            len(df)
        )

    with col2:
        st.metric(
            "High",
            len(
                df[
                    df["severity"]
                    == "high"
                ]
            )
        )

    with col3:
        st.metric(
            "Medium",
            len(
                df[
                    df["severity"]
                    == "medium"
                ]
            )
        )

    with col4:
        st.metric(
            "Low",
            len(
                df[
                    df["severity"]
                    == "low"
                ]
            )
        )

    st.divider()

    # -------------------
    # ФІЛЬТРАЦІЯ
    # -------------------
    st.subheader("🔍 Фільтрація")

    c1, c2 = st.columns(2)

    with c1:
        selected_type = st.selectbox(
            "Тип атаки",
            ["Всі"]
            + list(
                df["type"]
                .unique()
            )
        )

    with c2:
        selected_severity = st.selectbox(
            "Критичність",
            ["Всі"]
            + list(
                df["severity"]
                .unique()
            )
        )

    search = st.text_input(
        "Пошук по опису"
    )

    filtered_df = df.copy()

    if selected_type != "Всі":
        filtered_df = filtered_df[
            filtered_df["type"]
            == selected_type
        ]

    if selected_severity != "Всі":
        filtered_df = filtered_df[
            filtered_df["severity"]
            == selected_severity
        ]

    if search:
        filtered_df = filtered_df[
            filtered_df[
                "description"
            ]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # -------------------
    # ГРАФІК ЧАСУ
    # -------------------
    st.subheader(
        "📈 Динаміка інцидентів"
    )

    timeline_df = (
        filtered_df
        .groupby("date")
        .size()
        .reset_index(
            name="Кількість"
        )
        .sort_values("date")
        .set_index("date")
    )

    if not timeline_df.empty:
        st.line_chart(
            timeline_df
        )

    # -------------------
    # ДІАГРАМА ТИПІВ
    # -------------------
    st.subheader(
        "📊 Розподіл за типами"
    )

    st.bar_chart(
        filtered_df[
            "type"
        ].value_counts()
    )

    # -------------------
    # ТАБЛИЦЯ
    # -------------------
    st.subheader(
        "📋 Журнал інцидентів"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    # -------------------
    # ЕКСПОРТ CSV
    # -------------------
    csv = filtered_df.to_csv(
        index=False
    )

    st.download_button(
        "⬇️ Завантажити звіт CSV",
        csv,
        "cyber_report.csv",
        "text/csv"
    )

    # -------------------
    # ОЧИСТКА БАЗИ
    # -------------------
    if st.button(
        "🗑 Очистити базу"
    ):
        pd.DataFrame(
            columns=[
                "date",
                "type",
                "severity",
                "description"
            ]
        ).to_csv(
            DATA_FILE,
            index=False
        )

        st.success(
            "Базу очищено."
        )

        st.rerun()

        st.warning("База даних порожня або містить некоректні дані.")
