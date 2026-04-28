import sqlite3
import threading
from datetime import datetime
from config import DATABASE_PATH

class Database:
    def __init__(self, db_name=DATABASE_PATH):
        self.db_name = db_name
        self.conn = None
        self.lock = threading.Lock()
        self._init_connection()

    def _init_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.conn.execute('PRAGMA journal_mode=WAL')
            self.conn.execute('PRAGMA synchronous=NORMAL')
            self.conn.commit()
        self.create_tables()

    async def _get_connection(self):
        async with self.lock:
            if self.conn is None:
                self._init_connection()
            return self.conn

    def create_tables(self):
        with self.lock:
            if not self._table_exists():
                self.conn.execute('''
                    CREATE TABLE users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        selected_language TEXT,
                        translation_count INTEGER DEFAULT 0,
                        joined_at TEXT,
                        last_active TEXT
                    )
                ''')
            else:
                self._migrate_users_table()

            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    source_text TEXT,
                    translated_text TEXT,
                    target_language TEXT,
                    created_at TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            self.conn.commit()

    def _table_exists(self):
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            ('users',)
        )
        return cursor.fetchone() is not None

    def _get_table_columns(self):
        cursor = self.conn.execute(f"PRAGMA table_info(users)")
        return [row[1] for row in cursor.fetchall()]

    def _migrate_users_table(self):
        existing_columns = self._get_table_columns()
        current_columns = {
            'first_name': 'TEXT',
            'selected_language': 'TEXT',
            'translation_count': 'INTEGER DEFAULT 0',
            'joined_at': 'TEXT',
            'last_active': 'TEXT',
        }

        for column_name, definition in current_columns.items():
            if column_name not in existing_columns:
                self.conn.execute(
                    f'ALTER TABLE users ADD COLUMN {column_name} {definition}'
                )

        if 'join_date' in existing_columns and 'joined_at' not in existing_columns:
            self.conn.execute('ALTER TABLE users ADD COLUMN joined_at TEXT')
            self.conn.execute(
                'UPDATE users SET joined_at = join_date WHERE joined_at IS NULL AND join_date IS NOT NULL'
            )

        if 'translation_count' in existing_columns:
            self.conn.execute(
                'UPDATE users SET translation_count = 0 WHERE translation_count IS NULL'
            )

        now = datetime.now().isoformat()
        if 'joined_at' in self._get_table_columns():
            self.conn.execute(
                'UPDATE users SET joined_at = ? WHERE joined_at IS NULL',
                (now,)
            )
        if 'last_active' in self._get_table_columns():
            self.conn.execute(
                'UPDATE users SET last_active = ? WHERE last_active IS NULL',
                (now,)
            )

    def add_user(self, user_id, username=None, first_name=None):
        now = datetime.now().isoformat()
        with self.lock:
            self.conn.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, joined_at, last_active)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, now, now))
            self.conn.commit()

    def update_language(self, user_id, language):
        now = datetime.now().isoformat()
        with self.lock:
            self.conn.execute('''
                UPDATE users SET selected_language = ?, last_active = ? WHERE user_id = ?
            ''', (language, now, user_id))
            self.conn.commit()

    def get_user(self, user_id):
        with self.lock:
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            return cursor.fetchone()

    def get_user_language(self, user_id):
        with self.lock:
            cursor = self.conn.execute('SELECT selected_language FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            return row[0] if row else None

    def add_translation_log(self, user_id, source_text, translated_text, target_language):
        now = datetime.now().isoformat()
        with self.lock:
            self.conn.execute('''
                INSERT INTO logs (user_id, source_text, translated_text, target_language, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, source_text, translated_text, target_language, now))

            self.conn.execute('''
                UPDATE users SET translation_count = translation_count + 1, last_active = ? WHERE user_id = ?
            ''', (now, user_id))
            self.conn.commit()

    def get_all_users(self):
        with self.lock:
            cursor = self.conn.execute('SELECT user_id FROM users')
            return [row[0] for row in cursor.fetchall()]

    def get_total_users(self):
        with self.lock:
            cursor = self.conn.execute('SELECT COUNT(*) FROM users')
            return cursor.fetchone()[0]

    def get_active_users(self):
        with self.lock:
            cursor = self.conn.execute('SELECT COUNT(*) FROM users WHERE selected_language IS NOT NULL')
            return cursor.fetchone()[0]

    def get_total_translations(self):
        with self.lock:
            cursor = conn.execute('SELECT SUM(translation_count) FROM users')
            result = cursor.fetchone()[0]
            return result if result else 0

    def get_language_stats(self):
        with self.lock:
            cursor = self.conn.execute('''
                SELECT selected_language, COUNT(*) as count
                FROM users
                WHERE selected_language IS NOT NULL
                GROUP BY selected_language
            ''')
            return dict(cursor.fetchall())

    def get_today_translations(self):
        from datetime import datetime
        today = datetime.now().date().isoformat()
        with self.lock:
            cursor = self.conn.execute('''
                SELECT COUNT(*) FROM logs
                WHERE DATE(created_at) = ?
            ''', (today,))
            return cursor.fetchone()[0]

    def get_stats(self):
        total_users = self.get_total_users()
        active_users = self.get_active_users()
        total_translations = self.get_total_translations()
        language_stats = self.get_language_stats()
        today_translations = self.get_today_translations()

        return {
            'total_users': total_users,
            'active_users': active_users,
            'total_translations': total_translations,
            'language_stats': language_stats,
            'today_translations': today_translations
        }
