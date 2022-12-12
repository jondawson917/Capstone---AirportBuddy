from models import Trip, Passenger, Baggage, db
from app import app
from API_data import *

db.drop_all()

db.create_all()


t1 = Trip(name="Dude's Trip", takeoff_time="04/20/2023 09:00:00", airport_code="SAN", destination="Cancun", bags=3, transport_mode='transit')
t2 = Trip(name="Girl's Trip", takeoff_time="06/09/2023 18:00:00", airport_code="LAX", destination="Jamaica", bags=4)

t1.security_time = t1.get_airport_info()['security_time']
t2.security_time = t2.get_airport_info()['security_time']

db.session.add_all([t1,t2])
db.session.commit()

p1 = Passenger(first_name="Chad", last_name="Spilner", disabled=False, trip=t1, state= 'CA', zipcode='92116', city='San Diego', street="4545 Arizona St")

p2 = Passenger(first_name="Doug", last_name="Wright", disabled=False, trip=t1, 
state= 'CA',
zipcode= '92121',
city= 'San Diego',
street= "9380 Judicial Dr")
p3 = Passenger(first_name="Finchie", last_name="McGee", disabled=True, trip=t1,
state= 'CA',
zipcode= '92154',
city= 'San Diego',
street= "4026 Coleman Dr")

p5 = Passenger(first_name="Cinder", last_name="Ella", disabled=False, trip=t2, 
state= 'CA',
zipcode= '92128',
city= 'San Diego', street= "18543 Caminito Pasadero")

p6 = Passenger(first_name="Zoe", last_name="Zinfandel", disabled=False, trip=t2,
state= 'CA',
zipcode= '92128',
city= 'San Diego', street= "18543 Caminito Pasadero")


db.session.add_all([p1, p2, p3, p5, p6])
db.session.commit()


print("\n \n \n")

b1 = Baggage(brand_photo='https://assets.awaytravel.com/spree/products/26311/original/PDP_Aluminum_Silver_BCO_01.jpg', bag_type='checked-bag', weight=4.2, passenger=p5, trip=t2)
b2 = Baggage(brand_photo='https://i.pinimg.com/originals/a5/bb/d9/a5bbd93afc67f588aaecd7e0c9eabd29.jpg', bag_type='checked-bag', weight=22.5, passenger=p5, trip=t1)
b3 = Baggage(brand_photo='https://assets.mgimgs.com/mgimgs/ab/images/dp/wcm/202120/0003/terminal-1-carry-on-luggage-o.jpg', bag_type='checked-bag', weight=15, passenger=p6, trip=t1)
b4 = Baggage(brand_photo='https://i.pinimg.com/736x/70/a5/1f/70a51f10e5023db28ac09d65ed0f8988.jpg', bag_type='carry-on', weight=19, passenger=p3, trip=t1)
b5 = Baggage(brand_photo='https://assets.weimgs.com/weimgs/ab/images/wcm/products/202115/0315/rei-co-op-outward-padded-bench-1-z.jpg', bag_type='carry-on', weight=49.2, passenger=p2, trip=t2)
b6 = Baggage(brand_photo='https://i.pinimg.com/originals/77/2e/5c/772e5c21ff6207b01328bcaa24c480fb.jpg', bag_type='carry-on', weight=16.3, passenger=p1, trip=t2)


db.session.rollback()

db.session.add_all([b1, b2, b3, b4, b5, b6])

db.session.commit()

