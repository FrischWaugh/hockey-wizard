import requests
import simplejson as json

def get_schedule(startDate, endDate):
    response = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?date={}'.format(date))
    return response.json()
