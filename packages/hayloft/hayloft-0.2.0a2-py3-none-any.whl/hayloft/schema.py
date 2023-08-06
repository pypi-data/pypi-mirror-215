from peewee import SqliteDatabase, CharField, IntegerField, Model, ForeignKeyField
from pathlib import Path

# todo: add Windows paths support
# abs = Path(__file__).parent.resolve() 
# var = Path("../../../../var/hayloft")
# path = abs.joinpath(var)
# path.mkdir(parents=True, exist_ok=True)
# db = SqliteDatabase(f'{str(path.resolve())}/store.db')
path = str(Path(__file__).parent.resolve()) 
db = SqliteDatabase(f'{path}/store.db')

class Session(Model):
    name = CharField(unique=True)
    created_at = IntegerField()

    class Meta:
        database = db
        table_name = 'sessions'

class Event(Model):
    session = ForeignKeyField(Session, backref='events')
    title = CharField()
    message = CharField()
    type = CharField()

    class Meta:
        database = db
        table_name = 'events'

