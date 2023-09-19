import sqlite3

bank = sqlite3.connect('bank.db')
cursor = bank.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS clients '
               '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
               'full_name TEXT, phone_number TEXT, balance REAL DEFAULT 0)')
bank.commit()


def register_client(full_name, phone_number):
    cursor.execute('INSERT INTO clients (full_name, phone_number) VALUES (?, ?)', (full_name, phone_number))
    bank.commit()


def find_client(search_query):
    cursor.execute('SELECT * FROM clients WHERE full_name LIKE ? OR phone_number LIKE ?',
                   ('%' + search_query + '%', '%' + search_query + '%'))
    return cursor.fetchall()


def deposit(client_id, amount):
    cursor.execute('UPDATE clients SET balance = balance + ? WHERE id = ?', (amount, client_id))
    bank.commit()


def withdraw(client_id, amount):
    cursor.execute('UPDATE clients SET balance = balance - ? WHERE id = ?', (amount, client_id))
    bank.commit()


def get_balance(client_id):
    cursor.execute('SELECT balance FROM clients WHERE id = ?', (client_id,))
    return cursor.fetchone()[0]


def calculate_deposit(client_id, months):
    interest_rate = 0.01
    balance = get_balance(client_id)
    total_amount = balance * (1 + interest_rate) ** (months / 12)
    return total_amount


def client_dashboard(client_id):
    cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
    return cursor.fetchone()
