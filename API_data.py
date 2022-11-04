import requests
from datetime import datetime
TSA_BASE_URL = 'https://www.tsawaittimes.com/api/airport'
BING_BASE_URL = 'http://dev.virtualearth.net/REST/v1/Locations'
BING_API_KEY = 'AqV4ejSx_6XyytxEkL1hNy_EFj81zdzy8mgkhf6jt69EYRAc6q9hcW3M-t8nztgJ'
TSA_API_KEY = "unWIUmZNisXUWquFwzrSPGT5p5VGn3g8"
BING_TEST_URL = f'http://dev.virtualearth.net/REST/v1/Locations/US/WA/98052/Redmond/1%20Microsoft%20Way?&key='
TSA_TEST_URL = f'https://www.tsawaittimes.com/api/airports/'


#Section to call API Data
# def get_home_coords(country, state, zipcode, city, address):
#     """Get Bing Maps coordinates for starting point"""
#     resp = requests.get(f'{BING_BASE_URL}', params={"countryRegion": f"{country}", "adminDistrict": f"{state}", "locality": f"{city}", "postalCode": f"{zipcode}", "addressLine": f"{address}", "key": f"{BING_API_KEY}"}).json()
#     coords =  (resp['resourceSets'][0]['resources'][0]['point']['coordinates'])
#     coordinates = ','.join(str(i) for i in coords)
#     return {'coordinates': coordinates}



def get_airport_info(CODE):

    resp = requests.get(f'{TSA_BASE_URL}/{TSA_API_KEY}/{CODE}').json()
    return {"latitude": resp['latitude'], "longitude": resp['longitude'], "alerts": resp['faa_alerts']}
    
def get_data(code): 
    home_coords = get_home_coords(country, state, zipcode, city, address)
    arpt_coords = get_airport_info(code)['latitude']+','+ get_airport_info(code)['longitude']
    return {home_coords, arpt_coords }

travelMode = 'driving'



def get_commute_time(home_coords, travelMode, avoid, arpt_coords):
    timeType = 'Arrival'
    format = "%m/%d/%Y %H:%M:%S"
    dateTime = datetime.now().strftime(format)
    print(travelMode, home_coords, arpt_coords, avoid, timeType, dateTime)
    resp = requests.get(f'http://dev.virtualearth.net/REST/V1/Routes/{travelMode}', params= 
    {"wayPoint.1": f'{home_coords}', 
    "wayPoint.2": f'{arpt_coords}', "avoid": f'{avoid}', 
    "routeAttributes": 'transitStops', "timeType": f'{timeType}', 
    "dateTime": f'{dateTime}', "distanceUnit": 'mi', "key": f'{BING_API_KEY}'
    })
 
    unit_of_time = resp.json()['resourceSets'][0]['resources'][0]['durationUnit']
    time_of_travel = resp.json()['resourceSets'][0]['resources'][0]['travelDuration']
    return f'{time_of_travel} {unit_of_time}'
