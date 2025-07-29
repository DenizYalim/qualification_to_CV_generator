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


def add_qualification_to_db(qualifications, essentiality=False, conn=None, cursor=None):
    should_close = False
    if conn is None or cursor is None:
        conn, cursor = pre_req()
        should_close = True

    if not isinstance(qualifications, list):
        qualifications = [qualifications]

    for qualification in qualifications:
        cursor.execute(
            """
            INSERT INTO qualifications (text, essential, dateAdded)
            VALUES (?, ?, ?)
            """,
            (qualification, essentiality, datetime.now().strftime("%Y-%m-%d")),
        )

    if should_close:
        conn.commit()
        conn.close()


# TODO: Maybe instead of passing down conn and cursor like this (horrible) I can just drop the table below, commit and close connection then call the addToDB again where it request connection again and sets up the table again
def set_qualification_table(new_list):
    conn, cursor = pre_req()

    cursor.execute(  # Deletes every row
        """
        DELETE FROM qualifications
        """
    )

    add_qualification_to_db(
        new_list, cursor=cursor, conn=conn
    )  # This is nice and all but this makes it impossible to add essential qualities.

    conn.commit()
    conn.close()


""" returns all qualifications for a specific date or site

Keyword arguments:
date : DATE
website : String

Return: String[]
"""


def get_qualifications(include_date_info = True):
    conn, cursor = pre_req()

    statement = "SELECT text, essential FROM qualifications"
    if include_date_info:
        statement = "SELECT text, essential, dateAdded FROM qualifications"

    cursor.execute(
        statement,
    )

    qualifications = cursor.fetchall()
    conn.close()

    qualifications = [
        row for row in qualifications
    ]  # Turns the weird [(headline,),(headline,)] to [headline]

    return qualifications
