import keyring
from snowflake.snowpark import Session

password = keyring.get_password("snowflake", "MULTIHUNTER")


def getSession():
    return Session.builder.configs(
        {
            "account": "LKVEZZQ-EP40008",
            "user": "MULTIHUNTER",
            "password": password,
            "schema": "PUBLIC",
            "database": "TEST",
        }
    ).create()
