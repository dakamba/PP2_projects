import psycopg2
from config import DB_CONFIG

class Database:
    def __init__(self):
        # Параметры подключения берутся из config.py
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.conn.autocommit = True
        self.create_tables()

    def create_tables(self):
        """Создание таблиц, если они еще не существуют"""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id       SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id            SERIAL PRIMARY KEY,
                    player_id     INTEGER REFERENCES players(id),
                    score         INTEGER   NOT NULL,
                    level_reached INTEGER   NOT NULL,
                    played_at     TIMESTAMP DEFAULT NOW()
                );
            """)

    def get_or_create_player(self, username):
        """Возвращает id игрока. Если его нет — создает."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT id FROM players WHERE username = %s", (username,))
            row = cur.fetchone()
            if row:
                return row[0]
            else:
                cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
                return cur.fetchone()[0]

    def save_score(self, player_id, score, level):
        """Сохраняет данные о завершенной игре"""
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO game_sessions (player_id, score, level_reached)
                VALUES (%s, %s, %s)
            """, (player_id, score, level))

    def get_personal_best(self, player_id):
        """Возвращает лучший счет игрока за всё время"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (player_id,))
            res = cur.fetchone()[0]
            return res if res is not None else 0

    def get_top_scores(self):
        """Возвращает Top-10 результатов: имя, счет, уровень и дату"""
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT p.username, gs.score, gs.level_reached, gs.played_at
                FROM game_sessions gs
                JOIN players p ON gs.player_id = p.id
                ORDER BY gs.score DESC, gs.played_at DESC
                LIMIT 10
            """)
            return cur.fetchall()

    def __del__(self):
        # Закрываем соединение при удалении объекта
        if hasattr(self, 'conn'):
            self.conn.close()