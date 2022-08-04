from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from db import db
from sqlalchemy.dialects.postgresql import UUID



"""
Question

"""
class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    difficulty = Column(Integer)
    category = Column(Integer, ForeignKey('categories.id'))
    ownership = Column(Integer, ForeignKey('users.id'), default=0)
    
    
    user = db.relationship('User', back_populates='questions') # with user

    ratings = db.relationship('Rating', backref='questions', lazy=True) # many to many with ratings


    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
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
Category

"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    ownership = Column(Integer, ForeignKey('users.id'), default='0')
    
    questions = db.relationship("Question", backref="categories") # one to many with question

    def __init__(self, type):
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
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

    questions = db.relationship('Question', backref='users') # one to many with question
    categories = db.relationship('Category', backref='users') # one to many with category

    ratings = db.relationship('Rating', backref='users', lazy=True) # many to many with ratings

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


"""
Rating
"""
class Rating(db.Model):
    __tablename__ = 'ratings'

    question = Column(Integer, ForeignKey('questions.id'), primary_key=True)
    user = Column(Integer, ForeignKey('users.id'), primary_key=True)
    rating = Column(Integer)



    def __init__(self, question, user, rating):
        self.question = question
        self.user = user
        self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'question': self.question,
            'user': self.user,
            'rating': self.rating
        }