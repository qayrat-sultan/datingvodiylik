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
                   "name character varying(15), "
                   "PRIMARY KEY (id));")
    return True


def insert_data_to_yonalish_table():
    cursor.execute("INSERT INTO users_yonalish (name) VALUES ('Qizlar');")
    cursor.execute("INSERT INTO users_yonalish (name) VALUES ('Yigitlar');")
    cursor.execute("INSERT INTO users_yonalish (name) VALUES ('Farqi yoʻq');")

    return True


def create_tables():
    cursor.execute("CREATE TABLE IF NOT EXISTS users_users "
                   "(id bigserial NOT NULL, "
                   "telegram_id bigint NOT NULL, "
                   "username character varying(255), "
                   "checking boolean, "
                   "user_fullname character varying(255), "
                   "user_photo character varying(255), "
                   "user_yonalish numeric(1), "
                   "created_at timestamp without time zone, "
                   "PRIMARY KEY (id), "
                   "CONSTRAINT fk_yonalish FOREIGN KEY (user_yonalish) "
                   "REFERENCES users_yonalish (id) MATCH SIMPLE "
                   "ON UPDATE CASCADE "
                   "ON DELETE CASCADE);")
    cursor.execute("CREATE TABLE IF NOT EXISTS users_chats "
                   "(id serial NOT NULL, "
                   "left_user bigint, "
                   "right_user bigint, "
                   "active boolean, "
                   "created_at timestamp without time zone, "
                   "PRIMARY KEY (id));")
    cursor.execute("CREATE TABLE IF NOT EXISTS users_temp "
                   "(id bigserial NOT NULL, "
                   "message_id bigint NOT NULL, "
                   "telegram_id bigint NOT NULL, "
                   "message_text character varying(1000), "
                   "message_file character varying(255), "
                   "PRIMARY KEY (id));")
    cursor.execute("CREATE TABLE IF NOT EXISTS users_chats_temp "
                   "(id bigint NOT NULL, "
                   "chats_id integer NOT NULL, "
                   "temp_id bigint NOT NULL, "
                   "PRIMARY KEY (id), "
                   "CONSTRAINT users_chats_temp_chats_id_fk_users_chats_id FOREIGN KEY (chats_id) "
                   "REFERENCES users_chats (id) MATCH SIMPLE "
                   "ON UPDATE CASCADE "
                   "ON DELETE CASCADE, "
                   "CONSTRAINT users_chats_temp_temp_id_fk_users_temp_id FOREIGN KEY (temp_id) "
                   "REFERENCES users_temp (id) MATCH SIMPLE "
                   "ON UPDATE CASCADE "
                   "ON DELETE CASCADE);")
    return True


if __name__ == '__main__':
    # create_database()
    create_tables()
