from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('itinerary.sqlite')

class User(UserMixin, Model):
    username=CharField(unique=True)
    email=CharField(unique=True)
    password=CharField()
    first_name=CharField()
    last_name=CharField()
    join_date= DateTimeField()

    class Meta:
        database = DATABASE


class Destination(Model):
    name=CharField()

    class Meta:
        database = DATABASE


class Activity(Model):
    name=CharField()
    description=TextField()

    class Meta:
        database = DATABASE


class Trip(Model):
    title=CharField()
    author=ForeignKeyField(User, backref='trips')
    created_at = DateTimeField(default=datetime.datetime.now)
    destination=ForeignKeyField(Destination, backref='trips')
    activities=ForeignKeyField(Activity, backref='trips')
    comment=ForeignKeyField(Comment, backref='trips')
    trip_length=IntegerField()

    class Meta:
        database = DATABASE


class Comment(Model):
    user = ForeignKeyField(User, backref='comments')
    trip = ForeignKeyField(Trip, backref='comments')
    body = TextField()
    send_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class Relationship(BaseModel):
    from_user=ForeignKeyField(User, backref='relationships')
    to_user=ForeignKeyField(User, backref='related_to')

    class Meta:
        database = DATABASE
        indexes = ((('from_user', 'to_user'), True),)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Trip, Destination, Activity, Comment, Relationship], safe=True)
    print("TABLES Created")
    DATABASE.close()
