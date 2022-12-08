"""Trip View Tests"""

# run these tests like:
#
#    FLASK_DEBUG=production python3 -m unittest test_trip_views.py


from app import app
import os
from unittest import TestCase
from models import Trip, Passenger, Baggage, db


os.environ['DATABASE_URL'] = 'postgresql:///airport_buddy_test'



db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

TRIP_DATA = {
    "name": "Dude-Bro's Trip",
    "takeoff_time": "04/20/2023 09:00:00",
    "airport_code": "SAN",
    "destination": "Cancun",
    "bags": 3,
    "transport_mode": 'transit'
}

PASSENGER_DATA = {
    "first_name": "Chad",
    "last_name": "Spilner",
    "disabled": False,
    "state": 'CA',
    "zipcode": '92116',
    "city": 'San Diego',
    "street": "9380 Judicial Dr"
}

BAGGAGE_DATA = {
    "brand_photo": 'https://assets.awaytravel.com/spree/products/26311/original/PDP_Aluminum_Silver_BCO_01.jpg',
    "bag_type": 'checked-bag',
    "weight": 4.2
}


class TripModelsTestCase(TestCase):
    """TESTS FOR TRIP VIEWS of API"""

    def setUp(self):
        
        db.drop_all()
        db.create_all()

       
        self.uid = 1234
        self.testTrip = Trip(**TRIP_DATA)
        self.testTrip.security_time = self.testTrip.get_airport_info()['security_time']
        
        self.testTrip.id = self.uid

        db.session.add(self.testTrip)
        db.session.commit()
        self.t1 = Trip.query.get(self.uid)
        
        self.client = app.test_client()
       
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    

    def test_trip_model(self):
        """Trip model works"""

        t2 = Trip(id=8989, name="Ticket to Paradise", takeoff_time="11/29/2022 09:00:00", airport_code="LAX", destination="Vancouver", bags=2, transport_mode="driving")

        db.session.add(t2)
        db.session.commit()
        trips = Trip.query.all()
        self.assertEqual(len(trips), 2)


    def test_passenger_model(self):
        """Passenger model works"""
        p1 = Passenger(**PASSENGER_DATA, trip_id=self.uid)
        
        db.session.add(p1)
        db.session.commit()

        self.assertEqual(len(self.t1.passenger), 1)
        self.assertEqual(self.t1.passenger[0].zipcode, "92116" )


    def test_baggage_model(self):
        """Baggage model works"""
        self.p2 = Passenger(**PASSENGER_DATA, id=8989, trip_id=self.uid)
        self.b1 = Baggage(**BAGGAGE_DATA, trip_id=self.uid, passenger_id=self.p2.id)
        db.session.add_all([self.p2, self.b1])
        db.session.commit()

        self.assertEqual(len(self.p2.baggage), 1)
        self.assertEqual(self.p2.baggage[0].weight, 4.2)
        
        