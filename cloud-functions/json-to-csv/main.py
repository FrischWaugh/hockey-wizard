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

def boxscore_to_csv(boxscore):
  game_list = []
  for game in boxscore.keys():
    gameID = str(game)
    for team in boxscore[game]:
      teamID = str(boxscore[game][team]['teamID'])
      homeAway = team
      goals = str(boxscore[game][team]['teamStats']['goals'])
      pim = str(boxscore[game][team]['teamStats']['pim'])
      shots = str(boxscore[game][team]['teamStats']['shots'])
      powerPlayPercentage = str(boxscore[game][team]['teamStats']['powerPlayPercentage'])
      powerPlayGoals = str(round(boxscore[game][team]['teamStats']['powerPlayGoals']))
      powerPlayOpportunities = str(round(boxscore[game][team]['teamStats']['powerPlayOpportunities']))
      faceOffWinPercentage = str(boxscore[game][team]['teamStats']['faceOffWinPercentage'])
      blocked = str(boxscore[game][team]['teamStats']['blocked'])
      takeaways = str(boxscore[game][team]['teamStats']['takeaways'])
      giveaways = str(boxscore[game][team]['teamStats']['giveaways'])
      hits = str(boxscore[game][team]['teamStats']['hits'])
      string = gameID + ',' + teamID + ',' +  homeAway + ',' + goals + ',' + pim + ',' + shots + ',' + powerPlayPercentage + ',' + powerPlayGoals + ',' + powerPlayOpportunities + ',' + faceOffWinPercentage + ',' + blocked + ',' + takeaways + ',' + giveaways + ',' + hits
      game_list.append(string)
  return '\n'.join(game_list)

def json_to_csv(self):
  storage_client = inst_storage_client(path_key='gcloud_private_key.json', local=True)
  # Get schedule files
  files = list_blobs('nhl-wizard-landing', storage_client)
  # Iterate through files
  for file in files:
    if 'schedule' in file:
      schedule = get_json(file, 'nhl-wizard-landing', storage_client)
      content = schedule_to_csv(schedule)
      file_name = 'schedule/schedule_20200801_20220731.csv'
      storage_client.get_bucket('nhl-wizard-bd').blob(file_name).upload_from_string(content)
    elif 'boxscore' in file:
      boxscore = get_json(file, 'nhl-wizard-landing', storage_client)
      content = boxscore_to_csv(boxscore)
      file_name = 'boxscore/boxscore_20200801_20220731.csv'
      storage_client.get_bucket('nhl-wizard-bd').blob(file_name).upload_from_string(content)
  return 'Success!'
