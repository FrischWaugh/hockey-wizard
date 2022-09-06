import simplejson as json
from google.cloud import storage

def inst_storage_client(path_key, local=True):
    """
    This function instantiate the storage object from gcp. It can be used locally or not.
    """
    if local==True:
      storage_client = storage.Client.from_service_account_json(path_key)
    else:
      storage_client = storage.Client()
    return storage_client

def list_blobs(bucket_name, storage_client):
    """
    Lists all the blobs in the bucket.
    """
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)
    blob_list = []
    for blob in blobs:
        blob_list.append(blob.name)
    return blob_list

def get_json(filename, bucket_name, storage_client):
    """
    This function will get the json object from google cloud storage bucket.
    """
    blob = storage_client.get_bucket(bucket_name).get_blob(filename)
    # load blob using json
    file_data = json.loads(blob.download_as_string())
    return file_data

def schedule_to_csv(schedule):
  """
  This function gets the schedule json and transforms it to a csv file.
  Args:
        schedule: json file
            JSON file containing .

    Returns: A json file containing the requested information.
  """
  game_list = []
  for date in schedule['dates']:
    gameDate = date['date']
    for games in date['games']:
      gameID = str(games['gamePk'])
      gameType = games['gameType']
      season = str(games['season'])
      homeTeamID = str(games['teams']['home']['team']['id'])
      awayTeamID = str(games['teams']['away']['team']['id'])
      string = season + ',' + gameDate + ',' + gameID + ',' + gameType + ',' + homeTeamID + ',' + awayTeamID
      game_list.append(string)
  return '\n'.join(game_list)

def json_to_csv(self):
  storage_client = inst_storage_client(path_key='gcloud_private_key.json', local=True)
  # Get schedule files
  files = list_blobs('nhl-wizard-landing', storage_client)
  for file in files:
    if 'schedule' in file:
      schedule = get_json(file, 'nhl-wizard-landing', storage_client)
      content = schedule_to_csv(schedule)
      file_name = 'schedule/schedule.csv'
      storage_client.get_bucket('nhl-wizard-bd').blob(file_name).upload_from_string(content)
    elif 'boxscore' in file:
      print('boxscore')
  # Get boxscore files
#  boxscore_files = list_blobs('nhl-wizard-landing/boxscore', storage_client)
#  for file in schedule_files:
#    boxscore = get_json(file, 'nhl-wizard-landing', storage_client)
#    content = schedule_to_csv(boxscore)
#    file_name = 'boxscore/boxscore.csv'
#    storage_client.get_bucket('nhl-wizard-schedule').blob(file_name).upload_from_string(content)
  return 'Success!'