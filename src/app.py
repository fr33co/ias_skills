from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import request
from uuid import uuid4 as uuid

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class FlightSchema(ma.Schema):
    class Meta:
        fields = ('id', 'flight_name')


flight_schema = FlightSchema()
flights_schema = FlightSchema(many=True)


class TicketSchema(ma.Schema):
    class Meta:
        fields = ("id", "ticket", "ticket_code")

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(30), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return f'Username: {self.username}'


class Flight(db.Model):
    __tablename__ = "flight"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_name = db.Column(db.String(30))

    def __init__(self, flight_name):
        self.flight_name = flight_name

    def __repr__(self):
        return f'Flight Name: {self.flight_name}'


class Ticket(db.Model):
    __tablename__ = "ticket"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket = db.Column(db.String(30))
    ticket_code = db.Column(db.String(30), default=str(uuid()))

    def __init__(self, ticket, ticket_code):
        self.ticket = ticket
        self.ticket_code = ticket_code

    def __repr__(self):
        return f'Ticket: {self.ticket}'


class Reservation(db.Model):
    __tablename__ = "reservation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey("user.id"))
    flight_id = db.Column(db.ForeignKey("flight.id"))
    ticket_id = db.Column(db.ForeignKey("ticket.id"))

@app.route("/airline/")
def home():
    return {"msg": "Welcome"}

# USERS ROUTES

@app.route('/airline/users', methods=['GET'])
def get_all_users():
    """
    Get all users from the database and return them as JSON.
    """
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route("/airline/users/create", methods=["POST"])
def create_users():
    """
    A function that creates a new user in the airline system using POST method.
    """
    if request.method == "POST":
        username = request.json['username']
        email = request.json['email']
        new_user = User(username, email)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user)

@app.route('/airline/users/<email>', methods=['GET'])
def get_one_user(email):
    """
    A function to retrieve a single user based on the provided email address.

    Parameters:
    email (str): The email address of the user to retrieve.

    Returns:
    JSON: A JSON object containing the user information.
    """
    user = User.query.filter(User.email == email).first()
    return user_schema.jsonify(user)

@app.route('/airline/users/update/<email>', methods=['PUT'])
def update_one_user(email):
    """
    Update a user's username and email based on the provided email.
    """
    user = User.query.filter(User.email == email).first()
    if user:
        data_username = request.json['username']
        data_email = request.json['email']
        user.username = data_username
        user.email = data_email
        db.session.commit()
        return user_schema.jsonify(user)
    return {}

@app.route('/airline/users/delete/<email>', methods=['DELETE'])
def delete_one_user(email):
    """
    Delete a user by their email address.

    :param email: The email address of the user to be deleted.
    :return: JSON response containing the details of the deleted user.
    """
    user = User.query.filter(User.email == email).first()
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)

# FLIGHTS ROUTES

@app.route('/airline/flights', methods=['GET'])
def get_all_flights():
    """
    A function to retrieve all flights from the database and return them as
    JSON.
    """
    all_flights = Flight.query.all()
    result = flights_schema.dump(all_flights)
    return jsonify(result)

@app.route("/airline/flights/create", methods=["POST"])
def create_flights():
    """
    A function to create a new flight in the airline system.
    This function takes no parameters.
    Returns a JSON response with the details of the newly created flight.
    """
    if request.method == "POST":
        new_flight = request.json['flight_name']
        new_flight = Flight(new_flight)
        db.session.add(new_flight)
        db.session.commit()
        return flight_schema.jsonify(new_flight)

@app.route('/airline/flights/<flight_name>', methods=['GET'])
def get_one_flight(flight_name):
    """
    A function to retrieve a single flight by its name from the database.

    Parameters:
    flight_name (str): The name of the flight to retrieve.

    Returns:
    JSON: A JSON object containing the details of the retrieved flight.
    """
    get_flight = Flight.query.filter(Flight.flight_name == flight_name).first()
    return flight_schema.jsonify(get_flight)

@app.route('/airline/flights/update/<flight_name>', methods=['PUT'])
def update_one_flight(flight_name):
    """
    Update a specific flight by its name using a PUT request.

    Parameters:
    flight_name (str): The name of the flight to be updated.

    Returns:
    jsonify: JSON response with the updated flight information.
    """
    flight = Flight.query.filter(Flight.flight_name == flight_name).first()
    if flight:
        data_flight_name = request.json['flight_name']
        flight.email = data_flight_name
        db.session.commit()
        return flight_schema.jsonify(flight)
    return {}

@app.route('/airline/flights/delete/<flight_name>', methods=['DELETE'])
def delete_one_flight(flight_name):
    """
    A function to delete a specific flight by its name.

    Parameters:
    flight_name (str): The name of the flight to be deleted.

    Returns:
    jsonify: Returns a JSON representation of the deleted flight.
    """
    flight = Flight.query.filter(Flight.flight_name == flight_name).first()
    db.session.delete(flight)
    db.session.commit()
    return flight_schema.jsonify(flight)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8085, debug=True, host="0.0.0.0")
