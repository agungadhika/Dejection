import sqlite3

# Membuat koneksi dengan database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Membuat tabel
# cursor.execute('''CREATE TABLE IF NOT EXISTS users
                #   (username TEXT, password TEXT)''')

# Menambahkan data ke tabel
# cursor.execute("INSERT INTO tools_xxeinjection VALUES ('user1', 'password1')")
# cursor.execute("INSERT INTO users VALUES ('user2', 'password2')")
# cursor.execute("INSERT INTO users VALUES ('user3', 'password3')")

# Menyimpan perubahan dan menutup koneksi
conn.commit()
conn.close()
