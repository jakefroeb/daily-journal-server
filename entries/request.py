import sqlite3
import json
from models import Entry, Mood, Tag

def get_all_entries():
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
        e.id,
        e.concept,
        e.entry,
        e.date,
        e.mood_id,
        m.label
        FROM entry e
        JOIN mood m ON e.mood_id = m.id
        """)
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entryid = row['id']
            db_cursor.execute("""
            SELECT
            e.id,
            e.tag_id,
            e.entry_id,
            t.name
            FROM entry_tag e
            JOIN tag t ON e.tag_id = t.id
            WHERE e.entry_id = ?
            """,(entryid,))
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['mood_id'])
            mood = Mood(row['mood_id'], row['label'])
            entry.mood = mood.__dict__
            dataset2 = db_cursor.fetchall()
            tags = []
            for row in dataset2:
                tag = Tag(row['tag_id'], row['name'])
                tags.append(tag.__dict__)
            entry.tags = tags
            entries.append(entry.__dict__)
    return json.dumps(entries)
def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
        e.id,
        e.concept,
        e.entry,
        e.date,
        e.mood_id
        FROM entry e
        WHERE e.id = ?
        """,(id,))
        data = db_cursor.fetchone()
        entry = Entry(data['id'], data['concept'], data['entry'], data['date'], data['mood_id'])   
    return json.dumps(entry.__dict__)
def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM entry
        WHERE id = ?
        """, (id, ))
def get_entries_by_searchterm(searchterm):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
        e.id,
        e.concept,
        e.entry,
        e.date,
        e.mood_id
        FROM entry e
        WHERE e.entry LIKE ?
        """,(f"%{searchterm}%", ))
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['mood_id'])
            entries.append(entry.__dict__)
    return json.dumps(entries)
def create_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        INSERT INTO entry
            ( concept, entry, date, mood_id )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['date'], new_entry['mood_id'])
        )
        id = db_cursor.lastrowid
        new_entry['id'] = id
        for tag_id in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO entry_tag
                ( tag_id, entry_id )
            VALUES
                (?,?)
            """,(tag_id, new_entry['id']))
    return json.dumps(new_entry)
def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entry
            SET
                concept = ?,
                entry = ?,
                date = ?,
                mood_id = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
              new_entry['date'], new_entry['mood_id'],
                id, ))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True