from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from db import db
from sqlalchemy.dialects.postgresql import UUID


"""
Category

"""

class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    ownership = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), default='0')

    user = db.relationship(
        'User', primaryjoin='Category.ownership == User.id', backref='categories')

    def __init__(self, type: str, ownership: int):
        self.type = type
        self.ownership = ownership

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'type': self.type,
            'ownership': self.ownership
        }


"""
Question

"""

class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    difficulty = Column(Integer)
    category = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))
    ownership = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), default=0)

    category1 = db.relationship(
        'Category', primaryjoin='Question.category == Category.id', backref='questions')
    user = db.relationship(
        'User', primaryjoin='Question.ownership == User.id', backref='questions')

    def __init__(self, question, answer, category, difficulty, ownership):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty
        self.ownership = ownership

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }


"""
Rating
"""

class Rating(db.Model):
    __tablename__ = 'ratings'

    question = Column(Integer, ForeignKey(
        'questions.id', ondelete="CASCADE"), primary_key=True)
    user = Column(Integer, ForeignKey(
        'users.id', ondelete="CASCADE"), primary_key=True)
    rating = Column(Integer)

    question_ = db.relationship(
        'Question', primaryjoin='Rating.question == Question.id', backref='ratings')
    user_ = db.relationship(
        'User', primaryjoin='Rating.user == User.id', backref='ratings')

    def __init__(self, question, user, rating):
        self.question = question
        self.user = user
        self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def format(self):
        return {
            'question': self.question,
            'user': self.user,
            'rating': self.rating
        }


"""
Users
"""

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    public_id = db.Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=str(datetime.now()))
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)


    def __init__(self, username, password, public_id):
        self.username = username
        self.password = password
        self.public_id = public_id

    def format(self):
        return {
            'id': self.id,
            'username': self.username,
            'wins': self.wins,
            'losses': self.losses
        }
