import pandas as pd
import streamlit as st
from keboola_api import KeboolaStreamlit

# Inicializace Keboola Streamlit SDK
kbc = KeboolaStreamlit(
    "https://connection.north-europe.azure.keboola.com/", st.secrets["API_TOKEN"]
)

# Načtení dat z tabulky
if "data" not in st.session_state:
    st.session_state["data"] = kbc.read_table("in.c-demo_bucket.DEMO_TABLE")

df = st.session_state["data"].copy()  # Pracujeme s kopií, aby se předešlo chybám

# Kontrola, že sloupce existují, jinak vytvoříme prázdný dataframe
required_columns = [
    "EMPLOYEE_NAME",
    "MANAGER_NAME",
    "EMPLOYEE_ID",
    "MANAGER_ID",
    "PHONE_NUMBER",
    "HIRE_DATE",
    "SALARY",
    "JOB",
    "DEPARTMENT",
]

if not all(col in df.columns for col in required_columns):
    df = pd.DataFrame(columns=required_columns)

# Unikátní hodnoty pro dropdowny
existing_managers = df["EMPLOYEE_NAME"].dropna().unique().tolist()
existing_departments = df["DEPARTMENT"].dropna().unique().tolist()

# Automatické přiřazení nového EMPLOYEE_ID
new_employee_id = (df["EMPLOYEE_ID"].max() or 0) + 1

# FORMULÁŘ PRO PŘIDÁNÍ NOVÉHO ZAMĚSTNANCE
st.header("Přidat nového zaměstnance")

employee_name = st.text_input("Jméno zaměstnance")
manager_name = st.selectbox("Manažer", [""] + existing_managers)
department = st.selectbox("Oddělení", [""] + existing_departments)

# Automatické přiřazení MANAGER_ID podle jména
manager_id = (
    df.loc[df["EMPLOYEE_NAME"] == manager_name, "EMPLOYEE_ID"].iloc[0]
    if not df[df["EMPLOYEE_NAME"] == manager_name].empty
    else 0
)

phone_number = st.text_input("Telefonní číslo")
hire_date = st.date_input("Datum nástupu", pd.Timestamp.now())
salary = st.number_input("Plat", min_value=0, step=100)
job = st.text_input("Pozice")

if st.button("Přidat zaměstnance"):
    new_row = pd.DataFrame(
        [
            [
                employee_name,
                manager_name,
                new_employee_id,
                manager_id,
                phone_number,
                hire_date,
                salary,
                job,
                department,
            ]
        ],
        columns=required_columns,
    )

    st.session_state["data"] = pd.concat(
        [st.session_state["data"], new_row], ignore_index=True
    )

    # Uložení do Keboola
    kbc.write_table("in.c-demo_bucket.DEMO_TABLE", st.session_state["data"])

    st.success("Zaměstnanec přidán!")

# Zobrazení tabulky
st.write(st.session_state["data"])
