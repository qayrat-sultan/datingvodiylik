from db import cursor


def create_database():
    try:
        cursor.execute("CREATE DATABASE dating "
                       "WITH "
                       "OWNER = postgres "
                       "ENCODING = 'UTF8' "
                       "CONNECTION LIMIT = -1; ")
    except Exception as e:
        return e


def create_tables():
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS users_users "
                       "(id bigserial NOT NULL, "
                       "telegram_id bigint NOT NULL, "
                       "username character varying(255), "
                       "checking boolean, "
                       "PRIMARY KEY (id)); ")
    except Exception as e:
        return e


if __name__ == '__main__':
    # create_database()
    create_tables()

