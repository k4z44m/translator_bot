import sqlite3


def create_history_table():
    database = sqlite3.connect('bot.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id TEXT,
        original_text TEXT,
        translated_text TEXT,
        lang TEXT    
    );
    ''')
    database.commit()
    database.close()


def insert_into_history(chat_id, original_text, translated_text, lang):
    database = sqlite3.connect('bot.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO history(chat_id, original_text, translated_text, lang) VALUES (?,?,?,?)
    ''', (chat_id, original_text, translated_text, lang))
    database.commit()
    database.close()
