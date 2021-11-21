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


def create_yonalish_table():
    cursor.execute("CREATE TABLE IF NOT EXISTS users_yonalish "
                   "(id smallserial, "
                   "name character varying(15),"
                   "PRIMARY KEY (id));")
    return True


def insert_data_to_yonalish_table():
    cursor.execute("INSERT INTO users_yonalish (name) VALUES ('Qizlar');")
    cursor.execute("INSERT INTO users_yonalish (name) VALUES ('Yigitlar');")
    cursor.execute("INSERT INTO users_yonalish (name) VALUES ('Farqi yoʻq');")


def create_tables():
    cursor.execute("CREATE TABLE users_users "
                   "(id bigserial NOT NULL, "
                   "telegram_id bigint NOT NULL, "
                   "username character varying(255), "
                   "checking boolean, "
                   "user_fullname character varying(255), "
                   "user_photo character varying(255), "
                   "user_yonalish numeric(1), "
                   "PRIMARY KEY (id), "
                   "CONSTRAINT fk_yonalish FOREIGN KEY (user_yonalish) "
                   "REFERENCES users_yonalish (id) MATCH SIMPLE "
                   "ON UPDATE CASCADE "
                   "ON DELETE CASCADE);")
    return True


if __name__ == '__main__':
    # create_database()
    create_tables()
