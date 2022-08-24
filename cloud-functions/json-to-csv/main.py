import requests
import simplejson as json
from google.cloud import storage



def fetch_and_write(self):
	"""This function gets the schedule json and transforms it to a csv file"""
    yesterday = datetime.now() - timedelta(days=1, hours=5)
    day = yesterday.strftime("%Y-%m-%d")
    hockey = get_schedule(day)
    game_list = []
    for games in hockey:
        game_id = str(games['gamePk'])
        game_date = str(games['gameDate'][0:10])
        game_type = games['gameType']
        season = str(games['season'])
        for team in games['teams']:
            if team=='home':
                home_away=str(1)
            else:
                home_away=str(0)
            team_id = str(games['teams'][team]['team']['id'])
            team_score = str(games['teams'][team]['score'])
            string = game_id + ',' + game_date + ',' + game_type + ',' + season + ',' + home_away + ',' + team_id + ',' + team_score
            game_list.append(string)

    content = '\n'.join(game_list)
    file_name = 'nhl-schedule-daily.csv'
    storage_client = storage.Client()
    storage_client.get_bucket('nhl-wizard-data').blob(file_name).upload_from_string(content)
    return 'Success!'