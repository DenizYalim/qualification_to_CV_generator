import sqlite3
from datetime import datetime


# Returns connection obj and cursor obj
def pre_req():
    conn = sqlite3.connect("qualifications.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS qualifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL, 
            dateAdded DATE NOT NULL
        )
        """
    )

    conn.commit()
    return conn, cursor


def add_qualification_to_db(qualifications): 
    conn, cursor = pre_req()

    if not isinstance(qualifications, list):
        qualifications = [qualifications]

    for qualification in qualifications:
        cursor.execute(
            """
            INSERT INTO qualifications (text, dateAdded)
            VALUES (?, ?, ?)
            """,
            (qualification, datetime.now().strftime("%Y-%m-%d")),
        )

    conn.commit()
    conn.close()


def truncate_table(table:str):
    conn, cursor = pre_req()

    cursor.execute(  # Deletes every row
        f"TRUNCATE TABLE {table}"
    )

    conn.commit()
    conn.close()


# TODO: Maybe instead of passing down conn and cursor like this (horrible) I can just drop the table below, commit and close connection then call the addToDB again where it request connection again and sets up the table again
def set_qualification_table(new_list):
    truncate_table("qualifications")
    add_qualification_to_db(new_list)


def get_qualifications(include_date_info=True, justQualifications=False):
    conn, cursor = pre_req()

    statement = "SELECT text FROM qualifications"
    if include_date_info:
        statement = "SELECT text, dateAdded FROM qualifications"
    if justQualifications:
        statement = "SELECT text FROM qualifications"

    cursor.execute(
        statement,
    )

    qualifications = cursor.fetchall()
    conn.close()

    qualifications = [
        row for row in qualifications
    ]  # Turns the weird [(headline,),(headline,)] to [headline]

    return qualifications

def doQuery(query : str):
    conn, cursor = pre_req()
    cursor.execute(query)
    print(f"done query: {query}")
    conn.commit()
    conn.close()



if __name__ == "__main__": 
    doQuery("DROP TABLE qualifications")
