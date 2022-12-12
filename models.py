import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from data import *
DEFAULT_PIC = 'http://www.clipartbest.com/cliparts/9cp/oq6/9cpoq6BBi.png'

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Trip(db.Model):

    __tablename__ = 'trip'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, nullable=True, unique=True)

    transport_mode = db.Column(db.Text, nullable=False, default="driving")

    security_time = db.Column(db.Integer, nullable=True)

    bags = db.Column(db.Integer, nullable=False, default=0)
    
    destination = db.Column(db.Text, nullable=True, default="Timbuktu")

    takeoff_time = db.Column(db.DateTime, nullable=False)
    
    airport_code = db.Column(db.Text, nullable=False)
    
    passenger = db.relationship('Passenger', backref='trip', cascade="all, delete-orphan")

    baggage = db.relationship('Baggage', backref='trip', cascade="all, delete-orphan")


    @classmethod
    def get_trip_by_dest(cls, destination):
        """Returns trip info by destination"""
        return cls.query.filter_by(destination=destination).all()

    @classmethod
    def get_trip_by_id(cls, id):
        """Returns trip by id"""
        return cls.query.filter_by(id=id).all()

    def __repr__(self):
        t = self
        return f"<Trip Id = {t.id} called {t.name} takeoff_time = {t.takeoff_time} transport_mode = {t.transport_mode} Departure airport ={t.airport_code} TSA Security Wait time = {t.security_time}>"

    def get_airport_info(self):
        t = self
        
        resp = requests.get(f'{TSA_BASE_URL}/{TSA_API_KEY}/{t.airport_code}').json()
        print(resp)
        return {"latitude": resp['latitude'], "longitude": resp['longitude'], "alerts": resp['faa_alerts'], "security_time": resp['rightnow']} 

    def get_passenger_count(self):
        t=self
        
        return len(Passenger.query.filter_by(trip_id=t.id).all())

    def get_baggage(self):
        t=self

        return Baggage.query.filter_by(trip_id=t.id).all()
    

class Passenger(db.Model):
    
    __tablename__ = 'passenger'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.Text, nullable=False, unique=False)

    last_name = db.Column(db.Text, nullable=False, unique=True)

    disabled = db.Column(db.Boolean, nullable=True, default=False)

    street = db.Column(db.Text, nullable=False)
    
    city = db.Column(db.Text, nullable=False)
    
    state = db.Column(db.Text, nullable=False)
    
    zipcode = db.Column(db.Text, nullable=False)

    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
    
    baggage = db.relationship('Baggage', backref='passenger', cascade="all, delete-orphan" )


    @classmethod
    def get_passenger(cls, last_name):
        return cls.query.filter(last_name=last_name).all()
    

    def __repr__(self):

        p = self
        return f"<Passenger = {p.id} First Name={p.first_name} Last Name= {p.last_name} Disabled = {p.disabled} Trip Id = {p.trip_id}>"

    def full_name(self):

        p = self
        return f"{p.first_name}  {p.last_name} "

   
    
    def get_home_coords(self):
        """Get Bing Maps coordinates for starting point"""
        p = self
    
        resp = requests.get(f'{BING_BASE_URL}', params={"countryRegion": "US", "adminDistrict": f"{p.state}", "locality": f"{p.city}", "postalCode": f"{p.zipcode}", "addressLine": f"{p.street}", "key": f"{BING_API_KEY}"}).json()
        coords =  (resp['resourceSets'][0]['resources'][0]['point']['coordinates'])
        coordinates = ','.join(str(i) for i in coords)
        return coordinates
        
    def commute_time(self):
        p=self
        avoid = 'tolls'
        #Get Home Coordinates
        home_coords = p.get_home_coords()
        
        print(home_coords)
        #Get Airport Coordinates
        arpt_coords = p.trip.get_airport_info()['latitude'] + ',' + p.trip.get_airport_info()['longitude']
        
        print(arpt_coords)
        
        commute = get_commute_time(home_coords, p.trip.transport_mode, avoid, arpt_coords)
        calculated_commute_time = round(int(commute.split(" ")[0])/60)
        # Add 20 minutes to commute time if the passenger is wheelchair-bound
        if(p.disabled):
            calculated_commute_time+=20 
        return f'{calculated_commute_time} Minutes'
    
    def check_bags(self):
        p = self
        bags_to_check_in = p.trip.bags
        bags_on_hand = p.num_bags
        return bags_to_check_in - bags_on_hand
    def bag_count(self):
        p = self
        return Baggage.query.filter_by(passenger_id=p.id).all()

class Baggage(db.Model):

    __tablename__ = 'baggage'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    brand_photo = db.Column(db.Text, nullable=True, default=DEFAULT_PIC)

    bag_type = db.Column(db.Text, nullable=False)
    
    weight = db.Column(db.Float, nullable=True)

    passenger_id = db.Column(db.Integer, db.ForeignKey('passenger.id'))

    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))

    @classmethod
    def get_bag_by_id(cls, id):
        return cls.query.filter(id=id).all()
    
    def __repr__(self):
        b = self
        return f"<Bag id = {b.id} Bag Type = {b.bag_type} Weight = {b.weight} Passenger's Id = {b.passenger_id} Brand Photo URL = {b.brand_photo}  Trip ID= ={b.trip_id} Passenger ID = {b.passenger_id}"
        
    def connect_db(app):
        """Connect this database to provided Flask app"""

        db.app = app
        db.init_app(app)
