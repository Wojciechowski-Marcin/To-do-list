import sqlite3
import click
from flask import g, current_app
from flask.cli import with_appcontext

DATABASE = 'tasks.db'

def get_db():
    """Opens connection to database"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def close_db(e=None):
    """Closes connection to database"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_fetchall_db(query, args=(), one=False):
    """Query db with given args"""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    get_db().commit()
    return (rv[0] if rv else None) if one else rv


def query_edit_db(query, args=(), one=False):
    """Edit row in db"""
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    cur.close()
    return cur


def init_db():
    with current_app.app_context():
        db = get_db()
        with current_app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
