import keyring
import snowflake.connector

password = keyring.get_password("snowflake", "MULTIHUNTER")

conn = snowflake.connector.connect(
    user="MULTIHUNTER",
    password=password,
    account="LKVEZZQ-EP40008",
    database="TEST",
    schema="PUBLIC",
)

# cursor is a python object that allows you to interact with the database
cur = conn.cursor()
cur.execute("SELECT * FROM employees")
# for row in cur:
#     print(row)

df = cur.fetch_pandas_all()
print(df)
