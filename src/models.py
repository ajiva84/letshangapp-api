from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    addresses = db.relationship('Address', backref='person', lazy=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(50), nullable=False)
    bday = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    email = db.relationship('Event', backref='User', lazy=true, uselist=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "email": list(map(lambda x: x.serialize(), self.user))
            "firstname": self.firstname,
            "lastname": self.lastname,
            "address": self.address,
            "city": self.address,
            "state": self.address,
            "zipcode": self.address,
            "bday": self.address,
            "gender": self.address,

            # do not serialize the password, its a security breach
        }
class Event(db.Model):
    invitees = db.relationship('Invite', backref='event', lazy=True)
    eventname= db.column(db.String(50), primary_key=True)
    eventstreetaddress = db.Column(db.String(50), nullable=False)
    eventunitno = db.Column(db.String(50), nullable=False)
    eventstate = db.Column(db.String(50), nullable=False)
    eventcity = db.Column(db.String(50), nullable=False)
    eventzipcode = db.Column(db.String(50), nullable=False)
    eventdescription = db.Column(db.String(50), nullable=False)
    # eventpicture = db.Column(db.String(50), nullable=False)
    eventstatus = db.Column(db.String(50), nullable=False)
    eventcomments = db.relationship('comment'), backref'event', lazy=True)

    def __repr__(self):
        return '<Event {self.eventname}>'

    def serialize(self):
        return {
            "invitees": list(map(lambda x: x.serialize(), self.invitees))
            "eventname":list(map(lambda x: x.serrialze(), self.eventname))
            "eventstreetaddress": self.eventstreetaddress,
            "eventunitno": self.eventunitno,
            "eventstate": self.eventstate,
            "eventcity": self.eventcity,
            "eventzipcode": self.eventzipccode,
            "eventdescription": self.eventdescription,
            "eventstatus": self.eventstatus,
            "eventcomments": list(map(lambda x: x.serial(), self.invitees))
        }


class Invite(db.Model):
    user_email = db.Column(db.String, db.ForeignKey('user.email'), primary_key=True )
    statusofinvite = db.Column(db.String(50), nullable=False)
    event_eventname = db.Column(db.String, db.ForeignKey('event.eventname')
        nullable=False)


    def __repr__(self):
        return '<Invite {self.eventname}>'

    def serialize(self):
        return {
            "eventunitno": self.eventunitno,
            "invitees": list(map(lambda x: x.serialize(), self.invitees))
            "eventstreetaddress": self.eventstreetaddress,
            "eventunitno": self.eventunitno,
            
        }
