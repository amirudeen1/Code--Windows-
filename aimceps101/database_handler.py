import sqlite3
import hashlib

class DatabaseHandler:
    def __init__(self, db_name='game_data.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
        ''')
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS high_scores (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            game_mode TEXT,
            score INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        self.conn.commit()

    def add_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username already exists

    def verify_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        return self.cursor.fetchone() is not None

    def get_users(self):
        self.cursor.execute("SELECT username FROM users")
        return [row[0] for row in self.cursor.fetchall()]

    def add_score(self, username, game_mode, score):
        self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_id = self.cursor.fetchone()[0]
        self.cursor.execute("INSERT INTO high_scores (user_id, game_mode, score) VALUES (?, ?, ?)",
                            (user_id, game_mode, score))
        self.conn.commit()

    def get_high_scores(self, game_mode, limit=5):
        self.cursor.execute('''
        SELECT users.username, high_scores.score
        FROM high_scores
        JOIN users ON high_scores.user_id = users.id
        WHERE high_scores.game_mode = ?
        ORDER BY high_scores.score DESC
        LIMIT ?
        ''', (game_mode, limit))
        return self.cursor.fetchall()

    def get_user_high_score(self, username, game_mode):
        self.cursor.execute('''
        SELECT MAX(high_scores.score)
        FROM high_scores
        JOIN users ON high_scores.user_id = users.id
        WHERE users.username = ? AND high_scores.game_mode = ?
        ''', (username, game_mode))
        result = self.cursor.fetchone()[0]
        return result if result is not None else 0

    def close(self):
        self.conn.close()