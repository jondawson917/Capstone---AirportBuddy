# Capstone---AirportBuddy

The goal of Airport Buddy is to provide a trip management tool for group to plan their trip to the airport. 
Travelers can manage create, edit, and remove trip-info while viewing security wait times and commute-time to the airport.


## Include the API key in API_data.py
### -> API_data.py includes functions get_airport_info, get_data and get_commute_time to retrieve the following:
### -home coordinates (Latitude, Longitude) in following format: [47.640120461583138, -122.72951035116380]
### -airport coordinates (Latitude, Longitude) in following format: [26.640120461583138, -145.12941032116983]
### -commute time in seconds (this is converted to minutes after collected from the BING MAPS API) 
### -----------------------------------------------------
### "flask run" in root folder to run app.py local server
### -----------------------------------------------------

This requires two API keys from the following:

TSA WAIT TIMES API - https://www.tsawaittimes.com/api (7 DAY EXPIRATION)

BING MAPS API - https://www.microsoft.com/en-us/maps/choose-your-bing-maps-api (NO EXPIRATION)
