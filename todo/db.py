import mysql.connector
# importamos click que nos ayudará a ejecutar comandos en la terminal
import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    # cuando llamemos a esta función retornará la bd y el cursor
    return g.db, g.c

# vamos a crear una función que nos permita cerrar la conexión a la base de datos cada vez que realicemos una petición

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)

    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    # aquí vamos a ejecutar la lógica para correr los scripts de bd
    init_db()
    click.echo('Base de datos inicializada')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)