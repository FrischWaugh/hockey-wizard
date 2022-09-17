import requests
import simplejson as json
from google.cloud import storage

def get_schedule(startDate="2020-08-01", endDate="2022-07-31"):
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

def get_boxscore(schedule_json):
    """
    This function gets boxscore json.
    """
    dict_nhl = {}
    for date in schedule_json['dates']:
        for game in date['games']:
            response = requests.get(url='https://statsapi.web.nhl.com/api/v1/game/{}/boxscore'.format(game['gamePk']))
            dict_nhl[game['gamePk']] = {'home': {'teamID' : response.json()['teams']['home']['team']['id'], 
                                                 'teamStats': response.json()['teams']['home']['teamStats']['teamSkaterStats']},
                                        'away': {'teamID' : response.json()['teams']['away']['team']['id'], 
                                                 'teamStats': response.json()['teams']['away']['teamStats']['teamSkaterStats']}}
    return dict_nhl

def inst_storage_client(path_key, local=True):
    """
    This function instantiate the storage object from gcp. It can be used locally or not.
    """
    if local==True:
      storage_client = storage.Client.from_service_account_json(path_key)
    else:
      storage_client = storage.Client()
    return storage_client


def get_nhl_json(self):
    """
    This function will create json object in google cloud storage.
    """
    # Get schedule
    schedule = get_schedule()
    # Get boxscore
    boxscore = get_boxscore(schedule)
    # Instantiate the storage client
    storage_client = inst_storage_client(path_key='gcloud_private_key.json', local=True)
    # Create a blobs
    blob_schedule = storage_client.get_bucket('nhl-wizard-landing').blob('schedule/schedule_20200801_20220731.json')
    blob_boxscore = storage_client.get_bucket('nhl-wizard-landing').blob('boxscore/boxscore_20200801_20220731.json')
    # Upload the blob 
    blob_schedule.upload_from_string(data=json.dumps(schedule), content_type='application/json')
    blob_boxscore.upload_from_string(data=json.dumps(boxscore), content_type='application/json')
    return('Success!')