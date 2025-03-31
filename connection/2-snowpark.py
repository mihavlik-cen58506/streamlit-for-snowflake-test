import keyring
from snowflake.snowpark import Session

password = keyring.get_password("snowflake", "MULTIHUNTER")


pars = {
    "account": "LKVEZZQ-EP40008",
    "user": "MULTIHUNTER",
    "password": password,
    "schema": "PUBLIC",
    "database": "TEST",
}

session = Session.builder.configs(pars).create()

df = session.sql("SELECT * FROM employees")

# rows = df.collect()
# for row in rows:
#     print(row)

dfp = df.to_pandas()
print(dfp)
