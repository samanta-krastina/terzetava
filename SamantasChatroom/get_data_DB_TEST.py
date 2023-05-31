import sqlite3

conn = sqlite3.connect('chatroom_data.db')
c = conn.cursor()

# Ievieto manuali DB useri un paroli
# c.execute("INSERT INTO users (username, password) VALUES ('Samanta', '123')")

# Parada usera paroli
# c.execute("SELECT * FROM users WHERE username='Samanta")

# Parada usera rakstito pedejo zinu
c.execute("SELECT * FROM chat WHERE username='Samanta'")

data_all = c.fetchone()
print(data_all)

conn.commit()
conn.close()