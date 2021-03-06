from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

association = db.Table('association', 
db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
db.Column("event_id", db.Integer, db.ForeignKey("event.id"), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    friends = db.Column(db.String(50), nullable=True)
    unitno = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    events = db.relationship("Event",secondary=association, lazy='subquery', 
        backref=db.backref('user', lazy=True))
    lat= db.Column(db.String(50), unique=False, nullable=True)
    lng= db.Column(db.String(50), unique=False, nullable=True)
    
        
    def __repr__(self):
        return '<User %r>' % self.email 

    def validate(self, password):
        if not check_password_hash(self.password,password):
            return False
        
        return True

    def serialize(self):
        return {
            "id": self.id,
            "nick_name": self.nick_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "unitno": self.unitno,
            "friends": self.friends,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "birthday": self.birthday,
            "gender": self.gender,
            "email": self.email,
            "events":list(map(lambda x: x.serialize(), self.events)),
            "lat":self.lat,
            "lng":self.lng
            
            }

            # do not serialize the password, its a security breach

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invitees = db.Column(db.String(50), nullable=False)
    event_organizer = db.Column(db.String(50), nullable=False)
    event_name= db.Column(db.String(50), nullable=False)
    event_address = db.Column(db.String(50), nullable=False)
    event_location = db.Column(db.String(50), nullable=False)
    event_description = db.Column(db.String(50), nullable=False)
    users = db.relationship("User",secondary=association, lazy='subquery', 
        backref=db.backref('event', lazy=True))
    comments = db.relationship('Comment', backref='Event', lazy=True)

    def __repr__(self):
        return '<Event {self.eventname}>'

    def serialize(self):
        return {
            "id": self.id,
            "invitees": self.invitees,
            "event_name":self.event_name,
            "event_location": self.event_location,
            "event_address":self.event_address,
            "event_organizer":self.event_organizer,
            "event_description": self.event_description,
            # "eventstatus": self.eventstatus,
            "users":list(map(lambda x: x.serialize(), self.users)),
            "comments": list(map(lambda x: x.serialize(), self.comments))
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50), nullable=False)
    datestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'),
        nullable=False)

    def __repr__(self):
        return '<Invite {self.eventname}>'

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "datestamp": self.datestamp,
            "user_id": list(map(lambda x:x.serialize(),self.user_id)),
            "event_id": list(map(lambda x:x.serialize(),self.event_id))
            
        }

