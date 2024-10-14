from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import validates

db = SQLAlchemy()
ma = Marshmallow()

class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    @validates('number')
    def validate_number(self, key, number):
        if number <= 0:
            raise ValueError("Episode number must be greater than 0")
        return number

    @validates('date')
    def validate_date(self, key, date):
        # Here you can add a more sophisticated date validation
        if not date:
            raise ValueError("Date must not be empty")
        return date

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name must not be empty")
        return name

    @validates('occupation')
    def validate_occupation(self, key, occupation):
        if not occupation:
            raise ValueError("Occupation must not be empty")
        return occupation

class Appearance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)

    episode = db.relationship('Episode', backref=db.backref('appearances', cascade="all, delete-orphan"))
    guest = db.relationship('Guest', backref=db.backref('appearances', cascade="all, delete-orphan"))

    @validates('rating')
    def validate_rating(self, key, rating):
        if rating is None or not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return rating

