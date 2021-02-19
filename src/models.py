from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


association_table = Table('association', Base.metadata,
Column("user_id", Integer, ForeignKey("User.id"), primary_key=True),
Column("event_id", Integer, ForeignKey("Event.id"), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nick_name = db.Column(db.String(50), unqie=True, nullable=False)
    addresses = db.relationship(db.String(50), nullable=False)
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
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    events = relationship("Events",secondary=association_table, back_="users", nullable=True)
    lat= db.Column(db.String(), unique=False, nullable=True)
    lng= db.Column(db.String(), unique=False, nullable=True)
    
    

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
    id = db.Column(db.Integer, primary_key=True)
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
    text = db.column(db.String(50), nullable=False)
    user = db.Column(db.String, db.ForeignKey('user.email'), lazy=True, nullable=False)
    Datestamp = db.Column(db.String, db.ForeignKey('user.email'), lazy=True, nullable = False )

    event_eventname = db.Column(db.String, db.ForeignKey('event.eventname')
        nullable=False)

    def __repr__(self):
        return '<Invite {self.eventname}>'

    def serialize(self):
        return {
            "user_email": self.user_email,
            "statusofinvite": self.statusofinvite,
            "event_eventname": self.eventstreetaddress,
            
        }

association_table = Table('association', Base.metadata,
Column("sister_id", Integer, ForeignKey("Sister.id")),
Column("brother_id", Integer, ForeignKey("Brother.id"))
)

class Sister(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(80), nullable=False)
    brothers = relationship("Brother",
                    secondary=association_table
                    back_populates="sisters") # this line is so it updates the field when Sister is updated
                    
    def __ref__(self):
        return f'<Sister {self.name}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "brothers": list(map(lambda x: x.serialize(), self.brothers))
        }

class Brother(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(80), nullable=False)
    sisters = relationship("Sister",
                    secondary=association_table
                    back_populates="brothers")
                    
    def __ref__(self):
        return f'<Brother {self.name}>'
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "sisters": list(map(lambda x: x.serialize(), self.sisters))
        }