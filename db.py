import psycopg2

connection = psycopg2.connect(user="postgres",
                              password="1234",
                              host="localhost",
                              port="5432",
                              database="dating")

cursor = connection.cursor()
connection.autocommit = True
