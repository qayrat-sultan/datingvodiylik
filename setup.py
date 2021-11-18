import psycopg2

connection = psycopg2.connect(user="postgres",
                              password="1234",
                              host="localhost",
                              port="5432",
                              database="dating")

cursor = connection.cursor()


def create_database():
    try:
        x = cursor.execute("CREATE DATABASE dating "
                           "WITH "
                           "OWNER = postgres "
                           "ENCODING = 'UTF8' "
                           "CONNECTION LIMIT = -1; ")
        return x
    except Exception as e:
        return e


def create_tables():
    print("YES")
    x = cursor.execute("CREATE TABLE users_users "
                       "(id bigserial NOT NULL, "
                       "telegram_id bigint NOT NULL, "
                       "username character varying(255), "
                       "checking boolean, "
                       "user_fullname character varying(255), "
                       "user_photo character varying(255), "
                       "user_yonalish character varying(15), "
                       "PRIMARY KEY (id)); ")
    return x


if __name__ == '__main__':
    # create_database()
    create_tables()

