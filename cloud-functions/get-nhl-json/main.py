import requests
import simplejson as json

def get_schedule(startDate="2021-11-15", endDate="2021-11-17"):
    """This function extracts all the NHL games results of games
    played between startDate and endDate.
    
    Args:
        startDate: str
            The start date of the extraction (format must be YYYY-MM-DD).

        endDate: str
            The end date of the extraction (format must be YYYY-MM-DD).

    Returns: A json file containing the requested information.

    """
    response = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?date={}&{}'.format(startDate,endDate))
    return response.json()


if __name__ == '__main__':
    schedule = get_schedule()
    file_name = 'schedule_20211115_20211117.json'
    storage_client = storage.Client()
    storage_client.get_bucket('nhl-wizard-data').blob(file_name).upload_from_string(schedule)
    return 'Success!'
