"""Trip View Tests"""

# run these tests like:
#
#    FLASK_DEBUG=production python3 -m unittest test_trip_views.py


from app import app
import os
from unittest import TestCase
from models import Trip, Passenger, Baggage, db

from datetime import datetime
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


class TripViewsTestCase(TestCase):
    """TESTS FOR TRIP VIEWS of API"""

    def setUp(self):
        """Create test client and add sample data"""
        db.drop_all()
        db.create_all()
        
        self.client = app.test_client()

        self.testTrip = Trip(**TRIP_DATA)
        self.testTrip.security_time = self.testTrip.get_airport_info()[
            'security_time']
        db.session.add(self.testTrip)
        db.session.commit()
        self.p1 = Passenger(
            **PASSENGER_DATA, trip=self.testTrip, trip_id=self.testTrip.id)
            
        db.session.commit()
        self.b1 = Baggage(**BAGGAGE_DATA, trip=self.testTrip,
                          passenger=self.p1)
        db.session.add_all([self.testTrip, self.p1, self.b1])
        db.session.commit()

    def tearDown(self):
        """Removes mock Trip, Baggage, and Passenger Data"""
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_display_trips(self):
        """Test rendering of the trips page"""
        with self.client as c:

            resp = c.get("/Trips")

            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)

            self.assertIn('<th scope="col">Trip Name</th>', html)

    def test_display_passengers(self):
        """Test rendering of the Passengers page"""
        with self.client as c:

            resp = c.get("/Passengers")

            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)

            self.assertIn(
                '<th scope="col">Remove Passenger from Trip</th>', html)

    def test_display_Baggage(self):
        """Test rendering of the Baggage page"""
        with self.client as c:

            resp = c.get("/Baggage")

            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            brand_photo = Baggage.query.get(1).brand_photo
            self.assertIn(brand_photo, html)

    def test_display_newTrip(self):
        """Test rendering of the new trip form page"""
        with self.client as c:

            resp = c.get('/Trips/new')

            self.assertEqual(resp.status_code, 200)

            html = resp.get_data(as_text=True)
            self.assertIn(
                '<label for="takeoff_time">Takeoff Date/Time</label>', html)

#Test update functions for Trip, Passenger, and Baggage
    
    def test_trip_update(self):
        """Test rendering of the trip udpate page"""
        with self.client as c:

            resp = c.get(f'/Trips/{self.testTrip.id}/update')

            html = resp.get_data(as_text=True)
            self.assertIn('<label for="transport_mode">Transporation Mode</label>', html)

    def test_passenger_update(self):
        """Test rendering of the passenger update page"""

        with self.client as c:
            
            passenger_id = Passenger.query.get(1).id
            resp = c.get(f'/Passenger/{passenger_id}/update')

            html = resp.get_data(as_text=True)
            self.assertIn('<label for="first_name">First Name</label>', html)

    def test_baggage_update(self):
        """Test"""
        with self.client as c:

            baggage_id = Baggage.query.get(1).id

            resp = c.get(f'/Baggage/{baggage_id}/update')
            html = resp.get_data(as_text=True)

            self.assertIn(f"<p>Chad  Spilner 's checked-bag (4.2 lbs)</p>", html)


#Test delete functions for Trip, Passenger, and Baggage   
    
    def test_baggage_delete(self):
        b = Baggage(id=123, brand_photo='https://static.wikia.nocookie.net/shop-titans/images/5/5e/Enchantment-Air.png',bag_type ='carry-on', weight= 9.9, passenger_id=self.p1.id, trip_id=self.testTrip.id)

        db.session.add(b)
        db.session.commit()
       
        with self.client as c:
            resp = c.post(f'/Baggage/{b.id}/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            b = Baggage.query.get(123)
            self.assertIsNone(b)
    
    def test_passenger_delete(self):

        p = Passenger(id=321, first_name= "Boris", last_name= "Bekova", disabled= False, state='NE', zipcode='68502', city='Lincoln', street= "2240 Harrison Ave", trip_id=self.testTrip.id)

        db.session.add(p)
        db.session.commit()
        print(p)
        with self.client as c:
            resp = c.post(f'/Passenger/{p.id}/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            p = Passenger.query.get(321)
            self.assertIsNone(p)


    # def test_trip_delete(self):

    #     with self.client as c:


    
#     def test_submit_newTrip(self):

#         with self.client as c:
          

#             resp = c.post('/Trips/new', data=dict(name="HangoverTrip", takeoff_time=datetime(2023, 4, 26, 14, 0), airport_code="ORD", destination="New Orleans", transport_mode="driving", bags=2), follow_redirects=True)
#             html = resp.get_data(as_text=True)

#             self.assertIn('<label for="street">Street</label>', html)

# # {'name': 'HangoverTrip', 'takeoff_time': datetime.time(21, 45), 'airport_code': 'ORD', 'destination': 'Washington DC', 'bags': 1, 'transport_mode': 'driving', 'csrf_token': 'IjA5ZDI3MzFlMjBlNTYwM2M5NmViYjI5NTM3MzQyODJhZDIyYzdlYjUi.Y2RIVw.zgoudbkNGKqNAeow0456K6x7REQ'}
