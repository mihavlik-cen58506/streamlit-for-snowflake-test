import streamlit as st
from snowflake.snowpark import Session

st.title("Connecting to Snowflake")
st.header("Snowpark")


@st.cache_resource(max_entries=10)
def getSession(connection_name="snowflake"):
    section = st.secrets[f"connections_{connection_name}"]
    pars = {
        "account": section["account"],
        "user": section["user"],
        "password": section["password"],
        "database": section["database"],
        "schema": section["schema"],
        "role": section["role"],
        "warehouse": section["warehouse"],
    }
    return Session.builder.configs(pars).create()


@st.cache_data(ttl=3600, show_spinner="Running query...")
def runQuery(_session, query):
    df = _session.sql(query)
    df.collect()
    return df.to_pandas()


session = getSession()
df = runQuery(session, "select * from employees")
st.dataframe(df)
