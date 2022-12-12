from flask import Flask, redirect, request, render_template, flash
# import requests
from models import db, connect_db, Trip, Passenger, Baggage
from forms import AddTripForm, EditTripForm, AddPassengerForm, EditPassengerForm, AddEditBagsForm
from sqlalchemy.exc import IntegrityError
from API_data import *
import os


app = Flask(__name__)


# if(os.environ.get('DATABASE_URL')):
#     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
# else:
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "postgresql:///airport_buddy")
print(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'victorias')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
with app.app_context():
        db.create_all()





@app.route('/')
def home_page():
    """Renders the home page"""
   
    return render_template('home.html')

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('Error_404.html'), 404

######################
#Optional - Validation of API keys entered by user #
###################

# @app.route('/authorize', methods=["POST"])
# def authorize():
#     """Authorize Developer entry of API Keys"""

#     BING_API_KEY = request.form["BING"]
#     TSA_API_KEY = request.form["TSA"]
#     resp1 = requests.get(BING_TEST_URL+BING_API_KEY)
#     resp2 = requests.get(TSA_TEST_URL+TSA_API_KEY)
    
#     if(("denied" in resp1.text) or ('error' in (resp2.text))):
#         flash('Invalid API KEY')
#        
#         return render_template('instructions.html')
#     else:
#         flash(f'Invalid BING API KEY {BING_API_KEY}')
#         return redirect('/newTrip')


@app.route('/Trips', methods={"GET"})
def get_trips():
    """Retrieves a list of all trips from database"""
    trips = Trip.query.all()

    return render_template('display_trips.html', trips=trips)




@app.route('/Trips/new', methods=["GET", "POST"])
def new_trip():
    """Renders a new trip"""
    
    form = AddTripForm()
    
    
    if form.validate_on_submit():
        print(form.data)
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        name = data['name']
        takeoff_time = f'{datetime.now().month}/{datetime.now().day}/{datetime.now().year} '+ f'{data["takeoff_time"]}'
        airport_code = data['airport_code']
        destination = data['destination']
        bags= data['bags']
        new_trip = Trip(name=name, takeoff_time=takeoff_time, airport_code=airport_code, destination=destination, bags=bags)
        
        new_trip.security_time = new_trip.get_airport_info()['security_time']
        
        db.session.add(new_trip)
        db.session.commit()
        print(new_trip)
        flash(f'Trip {new_trip.name} is underWay')
        return redirect(f'/newPassenger/{new_trip.id}')
    else: 
        return render_template('add_new_trip.html', form=form)




@app.route('/Trips/<int:id>/update', methods=["GET", "POST"])
def update_trip(id):
    """Updates a single trip"""
    form = EditTripForm()
    trip = Trip.query.filter_by(id=id)[0]   
    print(form)
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        trip.name = data['name']
        trip.transport_mode = data['transport_mode']
        db.session.add(trip)
        db.session.commit()
        return redirect("/Trips")
    return render_template('edit_trip.html', trip=trip, form=form) 


@app.route('/Trips/<int:id>/delete', methods=["POST"])
def delete_trip(id):
    """Deletes a single trip"""
    trip = Trip.query.get_or_404(id)
    print(trip)
    db.session.delete(trip)
    db.session.commit()
    return redirect("/Trips")



@app.route('/Passengers')
def all_passengers():
    """Shows all passengers listed in the database"""
    passengers = Passenger.query.all()

    return render_template('display_passengers.html', passengers=passengers)





@app.route('/newPassenger/<int:id>', methods=["GET", "POST"])
def new_passenger(id):
    """Add a new passenger"""
    
    
    form = AddPassengerForm()
    print(form)    
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        first_name = data['first_name']
        last_name = data['last_name']
        if(data['disabled'] == 'yes'):
            disabled=True
        else:
            disabled=False
        city = data['city']
        street = data['street']
        zipcode = data['zipcode']
        state = data['state']
        
        new_passenger = Passenger(first_name=first_name, last_name=last_name, disabled=disabled, city=city, street=street, state=state, zipcode=zipcode, trip_id=id)
        db.session.add(new_passenger)
        db.session.commit()
        flash(f'Passenger {new_passenger.full_name()} has been added')
        return redirect(f'/newBaggage/{new_passenger.id}')
    else:
        return render_template('add_new_passenger.html', form=form)






@app.route('/Passenger/<int:id>/update', methods=["GET", "POST"])
def update_passenger(id):
    """Update a passenger's info"""
    passenger = Passenger.query.filter_by(id=id)[0]
    
    form = EditPassengerForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        first_name = data['first_name']
        last_name = data['last_name']
        if(data['disabled'] == 'Yes'):
            disabled=True
        else:
            disabled=False
        passenger.first_name = first_name 
        passenger.last_name = last_name 
        passenger.disabled = disabled
        db.session.add(passenger)
        db.session.commit()
        flash(f'Passenger {passenger.full_name()} has been changed')
        return redirect('/Passengers')
    else:
        return render_template('edit_passenger.html', form=form, passenger=passenger)

@app.route('/Passenger/<int:id>/delete', methods=["POST"])
def delete_passenger(id):
    """Removes a passenger from the data base and its baggage"""

    passenger = Passenger.query.get_or_404(id)
    db.session.delete(passenger)
    Baggage.query.filter_by(passenger_id=id).delete()
    db.session.commit()
    return redirect('/Passengers')


@app.route('/newBaggage/<int:id>', methods=["GET", "POST"])
def add_baggage(id):
    """Adds a bag for a given passenger id"""
    passenger = Passenger.query.get_or_404(id)
    passenger_choices = Passenger.query.filter(Passenger.id!=passenger.id).all()
    
    form = AddEditBagsForm()
    print(passenger )
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        brand_photo = data['brand_photo']
        bag_type = data['bag_type']
        weight = data['weight']

        new_baggage = Baggage(brand_photo=brand_photo, bag_type=bag_type, weight=weight, passenger=passenger, trip=passenger.trip)
        
        db.session.add(new_baggage)
        if (not passenger.check_bags()):
            passenger.trip.bags+=1
            db.session.commit()
            return redirect(f'/Baggage/{id}')
        else:
            db.session.commit()
            
            return redirect(f'/newBaggage/{id}')            
    else:
        return render_template('add_bags.html', form=form, passenger=passenger, passengers=passenger_choices)





@app.route('/Baggage', methods={"GET"})
def get_bags():
    """Retrieve a list of all bags from a database"""
    
    baggage = Baggage.query.all()
    
    return render_template('display_baggage.html', baggage=baggage)





@app.route('/Baggage/<int:id>', methods={"GET"})
def get_bag_by_id(id):
    """Retrieves a list of all bags belonging to passenger"""
   
    baggage = Baggage.query.filter_by(passenger_id=id).all()
    return render_template('/baggage/display_baggage.html', baggage=baggage, passenger=baggage[0].passenger)





@app.route('/Baggage/<int:id>/update', methods = ["GET", "POST"])
def update_baggage(id):
    """Update baggage info"""
    passenger_bags = Baggage.query.filter_by(passenger_id=id)
    
    
    form = AddEditBagsForm()
    if form.validate_on_submit():
        
        
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        
        bag_id = request.form['bag_select']
        
        bag_edit = Baggage.query.get(bag_id)
        
        bag_edit.brand_photo = data['brand_photo']
        
        bag_edit.bag_type = data['bag_type']
        
        bag_edit.weight = data['weight']

        db.session.add(bag_edit)
        db.session.commit()

        return redirect(f'/Baggage/{bag_id}')
   
    return render_template('edit_bags.html', form=form, baggage=passenger_bags)

@app.route('/Baggage/<int:id>/delete', methods=["POST"])
def delete_bag(id):
    """Removes a bag from the database"""
    bag = Baggage.query.get(id)
    db.session.delete(bag)
    bag.passenger.trip.bags-=1
    db.session.commit()
    return redirect('/Baggage')

@app.route('/Instructions')
def instructions():
    """Display instructions for creating a new trip"""
    return render_template('instructions.html')

