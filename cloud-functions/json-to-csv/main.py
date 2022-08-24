import simplejson as json
from google.cloud import storage

def get_json(filename):
    """
    This function will get the json object from google cloud storage bucket.
    """
    # get the blob
    blob = storage_client.get_bucket('nhl-wizard-data').get_blob(filename)
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
  schedule = get_json('schedule_20211115_20211117.json')
  content = schedule_to_csv(schedule)
  file_name = 'schedule_20211115_20211117.csv'
  storage_client = storage.Client()
  storage_client.get_bucket('nhl-wizard-data').blob(file_name).upload_from_string(content)
  return 'Success!'