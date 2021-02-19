from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

association = db.Table('association', 
db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
db.Column("event_id", db.Integer, db.ForeignKey("event.id"), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # nick_name = db.Column(db.String(50), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(50), nullable=False)
    bday = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)
    events = db.relationship("Event",secondary=association, lazy='subquery', 
        backref=db.backref('user', lazy=True))
    lat= db.Column(db.String(50), unique=False, nullable=True)
    lng= db.Column(db.String(50), unique=False, nullable=True)
    
    def __init__(self, email, password, firstname, lastname, address, city, state, zipcode, bday, gender, lat, lng, is_active ):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.bday = bday
        self.gender = gender
        self.lat = lat
        self.lng = lng
        self.is_active = is_active
        

    def __repr__(self):
        return '<User %r>' % self.email 

    def serialize(self):
        return {
            "id": self.id,
            "nick_name": self.nick_name,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "bday": self.bday,
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
    eventname= db.Column(db.String(50), nullable=False)
    eventstreetaddress = db.Column(db.String(50), nullable=False)
    eventunitno = db.Column(db.String(50), nullable=False)
    eventstate = db.Column(db.String(50), nullable=False)
    eventcity = db.Column(db.String(50), nullable=False)
    eventzipcode = db.Column(db.String(50), nullable=False)
    eventdescription = db.Column(db.String(50), nullable=False)
    # eventpicture = db.Column(db.String(50), nullable=False)
    eventstatus = db.Column(db.String(50), nullable=False)
    users = db.relationship("User",secondary=association, lazy='subquery', 
        backref=db.backref('event', lazy=True))
    comments = db.relationship('Comment', backref='Event', lazy=True)

    def __repr__(self):
        return '<Event {self.eventname}>'

    def serialize(self):
        return {
            "id": self.id,
            "invitees": self.invitees,
            "eventname":self.eventname,
            "eventstreetaddress": self.eventstreetaddress,
            "eventunitno": self.eventunitno,
            "eventstate": self.eventstate,
            "eventcity": self.eventcity,
            "eventzipcode": self.eventzipccode,
            "eventdescription": self.eventdescription,
            "eventstatus": self.eventstatus,
            "users":list(map(lambda x: x.serialize(), self.users)),
            "comments": list(map(lambda x: x.serialize(), self.comments))
        }



# class Invite(db.Model):
#     user_email = db.Column(db.String, db.ForeignKey('user.email'), primary_key=True )
#     statusofinvite = db.Column(db.String(50), nullable=False)
#     event_eventname = db.Column(db.String, db.ForeignKey('event.eventname')
#         nullable=False)


#     def __repr__(self):
#         return '<Invite {self.eventname}>'

#     def serialize(self):
#         return {
#             "user_email": self.user_email,
#             "statusofinvite": self.statusofinvite,
#             "event_eventname": self.eventstreetaddress,
            
#         }

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

