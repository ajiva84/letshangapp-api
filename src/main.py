"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from models import db, User, Event, Comment
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['POST', 'GET'])
def handle_user():
    """
    Create user and retrieve all users
    """

    # POST request
    # if request.method == 'POST':
    #     body = request.get_json()

    #     if body is None:
    #         raise APIException("You need to specify the request body as a json object", status_code=400)

    #     if 'email' not in body:
    #         raise APIException('You need to specify the email', status_code=400)
    #     if 'password' not in body:
    #         raise APIException('You need to specify the password', status_code=400)    

    #     user1 = User(email=body['email'], password=body['password'])
    #     db.session.add(user1)
    #     db.session.commit()
    #     return "ok", 200

    # GET request
    if request.method == 'GET':
        all_people = User.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200

    return "Invalid Method", 404

@app.route('/signup', methods=['POST'])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    nick_name= request.json.get("nick_name", None)  
    first_name= request.json.get("first_name", None)
    last_name = request.json.get("last_name", None)
    address = request.json.get("address", None)
    city = request.json.get("city", None)
    state= request.json.get("state", None)
    zipcode = request.json.get("zipcode", None)
    birthday = request.json.get("birthday", None)
    gender= request.json.get("gender", None)


    if not email:
        return jsonify({"msg": "Email is required"}), 400
    if not password:
        return jsonify({"msg": "Password is required"}), 400  

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"msg": "Email  already exists"}), 400 

    user = User(email=email, 
    password=generate_password_hash(password), 
    is_active=True,
    nick_name= nick_name,
    first_name=first_name, 
    last_name = last_name,
    address = address,
    city = city,
    state = state,
    zipcode = zipcode,
    birthday = birthday,
    gender = gender,
    )

    db.session.add(user)
    db.session.commit()    
    
    return jsonify({"msg": "User successfully registered"}),200

@app.route('/user/<int:id>', methods=['PUT'])
def user_update(id):
    body = request.get_json()
    user = User.query.get(id)
    if user is None:
        raise APIException('User not found', status_code=404)    
    if "last_name" in body:
        user.last_name = body["last_name"]
    if "address" in body:
        user.address = body["address"]
    if "birthday" in body:
        user.birthday = body["birthday"]
    if "email" in body:
        user.email = body["email"]
    if "password" in body:
        user.password = generate_password_hash(body["password"])
    if "first_name" in body:
        user.first_name = body["first_name"]
    if "nick_name" in body:
        user.nick_name = body["nick_name"]
    if "zipcode" in body:
        user.zipcode = body["zipcode"]
    if "state" in body:
        user.state = body["state"]
    if "lat" in body:
        user.lat = body["lat"]
    if "lng" in body:
        user.lng = body["lng"]

    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route('/user/<int:id>', methods=['GET'])
def user_get(id):
    user = User.query.get(id)
    return jsonify(user.serialize()), 200

@app.route('/events/all', methods=['GET'])
def event_getall():
    events = Event.query.all()
    all_events = list(map(lambda x: x.serialize(),events))
    return jsonify(all_events), 200
# def user_get(id):
#     users = User.query.filter_by(id = id).first()
#     seri_users = []
#     for user in users:
#         seri_users.append(user.serialize())
#     return jsonify(seri_users), 200

@app.route('/user/<int:id>', methods=['DELETE'])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return jsonify( {
        
        "msg": "User successfully deleted"
        }), 200
@app.route('/event', methods=['POST'])
def event():
    invitees = request.json.get("invitees", None)
    event_organizer = request.json.get("event_organizer", None)
    event_name = request.json.get("event_name", None)
    event_address= request.json.get("event_address", None)
    event_location= request.json.get("event_location", None)
    event_description = request.json.get("event_description", None)

    if not invitees:
        return jsonify({"msg": "Invitees are required"}), 400
    if not event_name:
        return jsonify({"msg": "Event name is required"}), 400  

    event = Event.query.filter_by(event_name=event_name).first()
    if event is not None:
        return jsonify({"msg": "Event is already exist"}), 400 

    event = Event(invitees=invitees,
    event_organizer=event_organizer,
    event_name= event_name,
    event_location = event_location,
    event_address= event_address,
    event_description = event_description
    )

    db.session.add(event)
    db.session.commit()    
    
    return jsonify({"msg": "Event has been created successfully"}),200



@app.route('/event/<int:id>', methods=['PUT'])
def event_update(id):
    body = request.get_json()
    event = Event.query.get(id)
    if event is None:
        raise APIException('Event not found', status_code=404)
    if "users" != None:
        event.users = body["users"]    
    if "invitees" in body:
        event.invitees = body["invitees"]
    if "event_organizer" in body:
        event.event_organizer = body["event_organizer"]
    if "event_name" in body:
        event.event_name = body["event_name"]
    if "event_address" in body:
        event.event_address = body["event_address"]
    if "event_suiteno" in body:
        event.event_suiteno = body["event_suiteno"]
    if "event_city" in body:
        event.event_city = body["event_city"]
    if "event_zipcode" in body:
        event.event_zipcode = body["event_zipcode"]
    if "event_state" in body:
        event.event_state = body["event_state"]
    if "event_description" in body:
        event.event_description = body["event_description"]
    
    db.session.commit()
    return jsonify(event.serialize()), 200

@app.route('/event/<int:id>', methods=['GET'])
def event_get(id):
    event = Event.query.get(id)
    return jsonify(event.serialize()), 200

@app.route('/event/<int:id>', methods=['DELETE'])
def event_delete(id):
    event = Event.query.get(id)
    db.session.delete(event)
    db.session.commit()

    return jsonify( {
        
        "msg": "Event successfully deleted"
        }), 200

# Handle/serialize errors like a JSON object
@app.route("/login", methods=["POST"])
def login():

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

        
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    lat = request.json.get("lat", None)
    lng = request.json.get("lng", None)
    

    if not email:
        return jsonify({"msg": "Missing email paramter"}), 400
    if not password:
        return jsonify({"msg": "Missing password paramter"}), 400
    if not lat:
        return jsonify({"msg": "Missing lat paramter"}), 400
    if not lng:
        return jsonify({"msg": "Missing lng paramter"}), 400


    try:
        user = User.query.filter_by(email=email).first()
        if user.validate(password):
            user.lat = lat
            user.lng = lng
            db.session.commit()
            expires = datetime.timedelta(days=7)
            response_msg = {
                "user":user.serialize(),
                'token':create_access_token(identity=email, expires_delta=expires),
                "expires_at": expires.total_seconds()*1000
            }
            status_code = 200
        else:
            raise Exception("Failed to login. Check your email and password.")

    except Exception as e:
        response_msg = {
            "msg": str(e),
            "status": 401
        }
        status_code = 401


    return jsonify(response_msg), status_code


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify( {
        
        "logged_in_as": current_user,
        "msg": "Access Granted to protected route"
        }), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
