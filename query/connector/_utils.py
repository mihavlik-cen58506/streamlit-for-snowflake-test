import keyring
import snowflake.connector

password = keyring.get_password("snowflake", "MULTIHUNTER")


def getConnection():
    return snowflake.connector.connect(
        user="MULTIHUNTER",
        password=password,
        account="LKVEZZQ-EP40008",
        database="TEST",
        schema="PUBLIC",
    )
