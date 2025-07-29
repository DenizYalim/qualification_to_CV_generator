import sqlite3
from datetime import datetime


def pre_req():
    conn = sqlite3.connect("qualifications.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS qualifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            essential BOOLEAN,
            dateAdded DATE NOT NULL
        )
        """
    )

    conn.commit()
    return conn, cursor


def add_qualification_to_db(date, qualifications, essentiality=False):
    conn, cursor = pre_req()

    for qualification in qualifications:
        cursor.execute(
            """
            INSERT INTO qualifications (text, essential, date)
            VALUES (?, ?, ?)
            """,
            (
                qualification,
                essentiality,
                datetime.now,
            ),  # datetime.now might return a weird digit instead of ddmmyyyy, this might clash with sql's date
        )

    conn.commit()
    conn.close()


""" returns all qualifications for a specific date or site

Keyword arguments:
date : DATE
website : String

Return: String[]
"""
def get_qualifications():
    conn, cursor = pre_req()

    statement = "SELECT text, essential FROM qualifications"
    cursor.execute(
        statement,
    )

    qualifications = cursor.fetchall()
    conn.close()

    qualifications = [
        row[0] for row in qualifications
    ]  # Turns the weird [(headline,),(headline,)] to [headline]

    return qualifications
