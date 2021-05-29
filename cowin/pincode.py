import requests
import time

pincode = 560066
date = '30-05-2021'

pincodeUrl = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={date}'

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

#file = open("pincodeSlots.txt", "w")
#file.write(date)

# Insert Function Here


def findVaccineSlots():
    counter = 0
    response = requests.get(pincodeUrl, headers=hdr)
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

        else:
            print('No Slots at ' + session['name'])
            time.sleep(3)
            #return False

while(findVaccineSlots() != True):
    time.sleep(6)
    findVaccineSlots()

#findVaccineSlots()
        
