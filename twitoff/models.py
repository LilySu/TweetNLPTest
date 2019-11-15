"""from twitoff.models import *

dir()#to see everything

DB.drop_all()
DB.create_all()

u1=User(name='austen')
t1=Tweet(text='lambda rules')
u1.tweets
"""

"""These are my database models"""

from flask_sqlalchemy import SQLAlchemy

#import database. capital for global scope
DB = SQLAlchemy()

class User(DB.Model):
    """Twitter users that we analyze"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Tweet(DB.Model):
    """The user's tweets from twitter"""
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    embedding = DB.Column(DB.PickleType, nullable=False)

    def __repr__(self):
        return '<Tweet {}>'.format(self.text)
#we turn this into a relational database, we probably want one to many
# class User(DB.Model):
#     """Twitter users that we analyze"""
#     id = DB.Column(DB.Integer, primary_key=True)
#     name = DB.Column(DB.String(15), nullable=False)
#
# class Tweet(DB.Model):
#     """The user's tweets from twitter"""
#     id = DB.Column(DB.Integer, primary_key=True)
#     text = DB.Column(DB.Unicode(280))