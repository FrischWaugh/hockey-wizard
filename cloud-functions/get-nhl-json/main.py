import requests
import simplejson as json
from google.cloud import storage

def get_schedule(startDate="2021-11-15", endDate="2021-11-17"):
    """
    This function extracts all the NHL games results of games
    played between startDate and endDate.
    
    Args:
        startDate: str
            The start date of the extraction (format must be YYYY-MM-DD).

        endDate: str
            The end date of the extraction (format must be YYYY-MM-DD).

    Returns: A json file containing the requested information.
    """
    response = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?startDate={}&endDate={}'.format(startDate,endDate))
    return response.json()


def get_nhl_json(self):
    """
    This function will create json object in google cloud storage.
    """
    schedule = get_schedule()
    file_name = 'schedule_20211115_20211117.json'
    storage_client = storage.Client()
    # create a blob
    blob = storage_client.get_bucket('nhl-wizard-data').blob(file_name)
    # upload the blob 
    blob.upload_from_string(data=json.dumps(schedule),content_type='application/json')
    return('Success!')