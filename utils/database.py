import sqlite3

def init_db():
    conn = sqlite3.connect('journal_entries.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS entries
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, time TEXT)''')
    conn.commit()
    conn.close()

def entry_exists(title, date, time):
    conn = sqlite3.connect('journal_entries.db')
    c = conn.cursor()
    c.execute("SELECT * FROM entries WHERE title = ? AND date = ? AND time = ?", (title, date, time))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def save_entry(title, date, time):
    conn = sqlite3.connect('journal_entries.db')
    c = conn.cursor()
    c.execute("INSERT INTO entries (title, date, time) VALUES (?, ?, ?)", (title, date, time))
    conn.commit()
    conn.close()
