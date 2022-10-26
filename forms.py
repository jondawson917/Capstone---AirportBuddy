from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, URLField, SelectField, FloatField
from wtforms.validators import InputRequired, URL, NumberRange, Length, ValidationError
from wtforms_components import DateRange
from wtforms.fields import TimeField
from models import Passenger, Trip, Baggage, db, connect_db
from datetime import datetime

#Hard coded values
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN" "TX", "UT", "VT", "WA", "WV", "WI", "WY"]

colors = ["Red", "Yellow", "Green", "Blue", "Orange", "Black", "White", "Purple", "Brown", "Tan", "Maroon"]

class AddTripForm(FlaskForm):
    """Form for entering flight check-in information"""
    
    name = StringField("Trip Name", validators=[Length(min=5, max=30, message="Enter a trip name between 5 and 30 characters")])

    takeoff_time = TimeField("Takeoff Date/Time", validators=[DateRange(min=datetime.now().time(), message="Enter a proper time")], format='%H:%M')

    airport_code = StringField("Airport Code", validators=[InputRequired(message="Enter departure airport code"), Length(max=3, message="Enter 3 letter airport code")])

    destination = StringField("Destination(City)", validators=[InputRequired(message="Enter a destination city"), Length(min=4, max=30, message="City should be between 6 and 25 characters long")])    

    bags = IntegerField("Number of Bags", validators=[NumberRange(min=0, message="Number of bags must be 0 or greater")])

    transport_mode = SelectField("Transporation Mode", choices=[('driving', 'Driving'), ('transit', 'Transit')])

class EditTripForm(FlaskForm):
    """Form for updating the flight information"""

    name = StringField("Trip Name", validators=[Length(min=5, max=30, message="Enter a trip name between 5 and 30 characters")])

    transport_mode = SelectField("Transporation Mode", choices=[('driving', 'Driving'), ('transit', 'Transit')])

class AddPassengerForm(FlaskForm):
    """Form for adding passenger info"""

    def validate_zipcode(form, field):
        if ((type(field.data) != 'int') and (len(str(field.data)) != 5)):
            raise ValidationError(f'Zip code must be a 5 digit number')


    first_name = StringField("First Name", validators=[InputRequired(message="Enter a first name"),Length(min=1, max=20, message="Name must be between 1 an 20 characters")])

    last_name = StringField("Last Name", validators=[InputRequired(message="Enter a last name"),Length(min=1, max=20, message="Name must be between 1 an 20 characters")])

    disabled = SelectField("Wheelchair needed", choices=[('yes', 'YES'), ('no', 'NO')])

    street = StringField("Street", validators=[InputRequired(message="Enter a street address"),Length(min=5, max=35, message="Name must be between 5 and 35 characters")])

    city = StringField("City", validators=[InputRequired(message="Enter a city"),Length(min=5, max=15, message="Name must be between 5 and 15 characters")])

    zipcode = StringField("Zip Code", validators=[InputRequired(message="Enter a zipcode "), validate_zipcode])

    state=SelectField("State", choices=[(st, st) for st in states])

class EditPassengerForm(FlaskForm):

    """Form for editing passenger info"""

    first_name = StringField("First Name", validators=[InputRequired(message="Enter a first name"),Length(min=1, max=20, message="Name must be between 1 an 20 characters")])

    last_name = StringField("Last Name", validators=[InputRequired(message="Enter a last name"),Length(min=1, max=20, message="Name must be between 1 an 20 characters")])

    disabled = SelectField("Wheelchair needed", choices=[('yes', 'YES'), ('no', 'NO')])

class AddEditBagsForm(FlaskForm): 
    """Form for adding/editing baggage"""
        

    brand_photo = URLField("Brand Photo", validators=[URL(require_tld=True, message="Enter URL in proper format")])

    bag_type = SelectField("Bag Type", choices=[('Carry-on', 'Carry-On Bag'), ('Checkedbag', 'Checked-Bag')])
    
    weight = FloatField("Weight (lbs)", validators=[NumberRange(min=0, max=50, message="Enter a weight (lbs) between 0 and 50 pounds")])
    



