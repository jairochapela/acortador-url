import sqlite3
from flask import abort, g
import os


LISTA_PALABRAS = [
    'sol', 'pan', 'luz', 'mar', 'cielo', 'flor', 'voz', 'piel', 'ley', 'pato', 
    'rio', 'sal', 'luna', 'noche', 'calle', 'mesa', 'peso', 'oro', 'lago'
]

LETRAS = "adefiklmnopqrstwxyz"

DB_PATH = os.environ.get('DB_PATH', 'urls.db')


def get_db_connection():
    con = getattr(g, '_database', None)
    if not con:
        con = g._database = sqlite3.connect(DB_PATH)
    return con



class Ruta:

    def __init__(self, ruta_corta, url_original):
        self.ruta_corta = ruta_corta
        self.url_original = url_original

    def __str__(self):
        return f'Ruta: {self.ruta_corta}'
    
    @property
    def ruta_words(self):
        corresponding_words = {k: v for k, v in zip(LETRAS, LISTA_PALABRAS)}
        return f'{"-".join(corresponding_words[c] for c in self.ruta_corta)}'

    
    @staticmethod
    def create_db():
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # Load schema and execute SQL commands
            with open('schema.sql', 'r') as f:
                cursor.executescript(f.read())

    
    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO rutas (ruta_corta, url_original)
                VALUES (?, ?)
            """, (self.ruta_corta, self.url_original))
            conn.commit()

    @staticmethod
    def get(ruta_corta):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.row_factory = lambda _, row: Ruta(ruta_corta=row[0], url_original=row[1])
            cursor.execute("""
                SELECT ruta_corta,url_original FROM rutas WHERE ruta_corta = ?;
            """, (ruta_corta,))
            return cursor.fetchone()

    @staticmethod
    def find_by_words(ruta_words):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            words = ruta_words.split('-')
            if all(w in LISTA_PALABRAS for w in words):
                ruta_corta = "".join(LETRAS[LISTA_PALABRAS.index(w)] for w in words)
                cursor.row_factory = lambda _, row: Ruta(ruta_corta=row[0], url_original=row[1])
                cursor.execute("""
                    SELECT ruta_corta,url_original FROM rutas WHERE ruta_corta = ?;
                """, (ruta_corta,))
                return cursor.fetchone()
            else:
                return None

    
    def delete(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM rutas WHERE ruta_corta = ?;
            """, (self.ruta_corta,))
            conn.commit()


