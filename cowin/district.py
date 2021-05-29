import requests
import time
import playsound

state = 16
district = 294
date = '30-05-2021'

findByDistrictUrl = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={district}&date={date}'

#print(findByDistrictUrl)

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}


def findVaccineSlots():

    counter = 0

    response = requests.get(findByDistrictUrl, headers=hdr)

    resultSet = response.json()
    
    sessions = resultSet['sessions']

    for session in sessions:
        if((session['available_capacity'] > 0) and (session['min_age_limit']==18)):
            counter += 1
            print('Centre Name: ' + session['name'])
            print(session['pincode'])
            print('Date: ' + session['date'])
            print('Vaccine: ' + session['vaccine'])
            print(session['available_capacity_dose1']),
            print(session['available_capacity_dose2'])
            print(session['available_capacity'])
            return True

        if(counter == 0):
            print('No Slots at ' + session['name'])
            time.sleep(3)
            #return False

while(findVaccineSlots() != True):
    time.sleep(6)
    findVaccineSlots()



