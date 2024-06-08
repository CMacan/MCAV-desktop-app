import psycopg2

conn = psycopg2.connect(host="localhost", dbname="MCAV", user="postgres", 
                        password="1234", port=5432)

cur = conn.cursor()


cur.execute("""CREATE TABLE IF NOT EXISTS USERS (
            USER_ID INT PRIMARY KEY,
            USER_FNAME VARCHAR(50) NOT NULL,
            USER_LNAME VARCHAR(50) NOT NULL,
            AGE INT NOT NULL,
            GENDER CHAR NOT NULL        
            );
""")

conn.commit()


cur.close()
conn.close()



