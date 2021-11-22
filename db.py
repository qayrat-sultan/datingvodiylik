import psycopg2
import config

connection = psycopg2.connect(user=config.DB_USER,
                              password=config.DB_PASSWORD,
                              host=config.DB_HOST,
                              port=config.DB_PORT,
                              database=config.DB_DATABASE)

cursor = connection.cursor()
connection.autocommit = True
