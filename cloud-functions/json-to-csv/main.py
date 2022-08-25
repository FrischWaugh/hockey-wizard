import simplejson as json
from google.cloud import storage

def list_blobs(bucket_name):
    """
    Lists all the blobs in the bucket.
    """
    storage_client = storage.Client()
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)
    blob_list = []
    for blob in blobs:
        blob_list.append(blob.name)
    return blob_list

def get_json(filename, bucket_name):
    """
    This function will get the json object from google cloud storage bucket.
    """
    # get the blob
    storage_client = storage.Client()
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
      homeScore = str(games['teams']['home']['score'])
      homeTeamID = str(games['teams']['home']['team']['id'])
      awayScore = str(games['teams']['away']['score'])
      awayTeamID = str(games['teams']['away']['team']['id'])
      string = season + ',' + gameDate + ',' + gameID + ',' + gameType + ',' + homeScore + ',' + homeTeamID + ',' + awayScore + ',' + awayTeamID
      game_list.append(string)
  return '\n'.join(game_list)

def json_to_csv(self):
  storage_client = storage.Client()
  # list of files in bucket
  files = list_blobs('nhl-wizard-landing')
  for file in files:
    schedule = get_json(file, 'nhl-wizard-landing')
    content = schedule_to_csv(schedule)
    file_name = 'tmp.csv'
    storage_client.get_bucket('nhl-wizard-schedule').blob(file_name).upload_from_string(content)
  return 'Success!'