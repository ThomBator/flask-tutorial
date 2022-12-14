import sqlite3
import click
from flask import current_app, g 
'''
g is a special objet that is unique to heach db request, the connection is stored if get_db is called a second time in the same request. current_app pointds to the flash application handling the request. 

'''

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES

        )
        g.db.row_factory = sqlite3.Row 

    return g.db 

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close() 

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f: 
        db.executescript(f.read().decode('utf8'))
@click.command('init-db')
def init_db_command():
    #clears existing data and creates new tables 
    init_db()
    click.echo('Initialized the database')

def init_app(app):
    app.teardown_appcontext(close_db) 
    app.cli.add_command(init_db_command)