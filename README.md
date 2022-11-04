# Capstone---AirportBuddy

The goal of Airport Buddy is to provide a trip management tool for group to plan their trip to the airport. 
Travelers can manage create, edit, and remove trip-info while viewing security wait times and commute-time to the airport.

This requires two API keys from the following:

TSA WAIT TIMES API - https://www.tsawaittimes.com/api (7 DAY EXPIRATION)

BING MAPS API - https://www.microsoft.com/en-us/maps/choose-your-bing-maps-api (NO EXPIRATION)

##Include the API key in data.py
###-> data.py includes functions get_airport_info, get_data and get_commute_time to retrieve the following:
###-home coordinates
###-airport coordinates
###-commute time in seconds
###-----------------------------------------------------
###"flask run" in root folder to run app.py local server
###-----------------------------------------------------
