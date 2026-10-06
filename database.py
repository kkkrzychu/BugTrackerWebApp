import sqlite3
from datetime import datetime

create_table_sql = """
    CREATE TABLE IF NOT EXISTS bugs (
        id INTEGER PRIMARY KEY,
        title TEXT,
        description TEXT,
        priority TEXT,
        status TEXT,
        created_at datetime,
        updated_at datetime
                        );
                    """

insert_into_table_sql = """
                INSERT INTO bugs(
                title,
                description,
                priority,
                status,
                created_at,
                updated_at)
                VALUES (
                ?,
                ?,
                ?,
                'Proposed',
                ?,
                ?);
                    """

update_bug_sql = """
        UPDATE bugs
        SET title = ?,
            description = ?,
            priority = ?,
            updated_at = ?
        WHERE id = ?;
            """

delete_bug_sql = """
            DELETE FROM bugs WHERE id = ?
"""

# conn = sqlite3.connect("bugtracker.db")
# conn.execute(create_table_sql)


# conn.execute(insert_into_table,(now, now))
# conn.commit()

# cursor = conn.execute(delete_bug, (2,))
# conn.commit()
# print(cursor.rowcount)

# # cursor = conn.execute(update_bug, ('In Progress', now, 1))
# # conn.commit()
# # print(cursor.rowcount)

# cursor = conn.execute("""SELECT * FROM bugs;""")
# wynik = cursor.fetchall()
# print(wynik)

# conn.close()

def get_bugs():
    conn = sqlite3.connect("bugtracker.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.execute("""SELECT * FROM bugs;""")
    wynik = cursor.fetchall()
    
    conn.close()
    return wynik

def get_bug(id: int):

    conn = sqlite3.connect("bugtracker.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.execute("""SELECT * FROM bugs WHERE id = ?""", (id,))
    wynik = cursor.fetchone()

    conn.close()
    return wynik

def create_bug(title: str, description: str, priority: str):
    conn = sqlite3.connect("bugtracker.db")

    now = datetime.now()

    cursor = conn.execute(insert_into_table_sql, (title, description, priority, now, now))
    new_id = cursor.lastrowid
    conn.commit()

    conn.close()

    return get_bug(new_id)

def update_bug(id: int , title: str | None = None, description: str | None = None, priority: str | None = None):

    old_bug = get_bug(id)

    if old_bug is None:
        return None

    conn = sqlite3.connect("bugtracker.db")
    now = datetime.now()

    if title is None:
        title = old_bug["title"]

    if description is None:
        description = old_bug["description"]

    if priority is None:
        priority = old_bug["priority"]
    
    conn.execute(update_bug_sql,(title, description, priority, now, id))
    conn.commit()
    
    conn.close()

    return get_bug(id)

def delete_bug(id: int):
    conn = sqlite3.connect("bugtracker.db")

    cursor = conn.execute(delete_bug_sql, (id,))
    conn.commit()

    count = cursor.rowcount

    conn.close()

    return count > 0

#get_bugs()
#get_bug(5)
#bug = update_bug(5, "tylkotytulmasiezmienic")
#print(dict(bug))