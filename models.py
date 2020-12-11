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
    join_date= DateTimeField(default=datetime.datetime.now)

    def following(self):
        return (User.select().join(Relationship, on=Relationship.to_user).where(Relationship.from_user == self).order_by(User.username))

    def followers(self):
        return (User.select().join(Relationship, on=Relationship.from_user).where(Relationship.to_user == self).order_by(User.username))

    def is_following(self, user):
        return (Relationship.select().where((Relationship.from_user == self) & (Relationship.to_user == user)).exists())

    class Meta:
        database = DATABASE

class Trip(Model):
    title=CharField()
    author=ForeignKeyField(User, backref='trips')
    created_at = DateTimeField(default=datetime.datetime.now)
    trip_length=CharField()
    image=CharField()

    class Meta:
        database = DATABASE

class Destination(Model):
    name=CharField()
    trip=ForeignKeyField(Trip, backref='destinations')

    class Meta:
        database = DATABASE


class Activity(Model):
    name=CharField()
    description=TextField()
    trip=ForeignKeyField(Trip, backref='activities')

    class Meta:
        database = DATABASE


class Comment(Model):
    user = ForeignKeyField(User, backref='comments')
    body = TextField()
    send_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

class Relationship(Model):
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
