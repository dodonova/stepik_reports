# Run with Python 3
# Saves all step sources into foldered structure
import os
import json
import requests
import datetime

from courses import COURSES, CLIENT_ID, CLIENT_SECRET

# Enter parameters below:
# 1. Get your keys at https://stepik.org/oauth2/applications/
# (client type = confidential, authorization grant type = client credentials)
client_id = CLIENT_ID
client_secret = CLIENT_SECRET
api_host = 'https://stepik.org'
course_id = 122709
# courses_id = COURSES
coursed_id = (
    122709,
    122710,
)

# 2. Get a token
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
response = requests.post('https://stepik.org/oauth2/token/',
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
token = response.json().get('access_token', None)
print(f'Token  {token}')
if not token:
    print('Unable to authorize with provided credentials')
    exit(1)


# 3. Call API (https://stepik.org/api/docs/) using this token.
# Example:
def get_course_period_statistics(course_id, from_datetime, to_datetime, current_token):
    """
    :param from_n: starting lesson id
    :param to_m: finish lesson id
    :param current_token: token given by API
    :return: json object with all existing lessons with id from from_n to to_m
    """
    # api_url = 'https://stepik.org/api//api/course-period-statistics/'

    api_url = f'https://stepik.org/api/course-period-statistics/{course_id}'

    try:
        current_answer = requests.get(
            api_url,
            headers={'Authorization': 'Bearer ' + current_token},
            params={
                "page": 1,
                "page_size": 100,
                "schedule_type": 1,
                "course": 122709
                # "from_date": from_datetime,
                # "to_date": to_datetime,
            }
        ).json()
    except Exception as err:
        current_answer= f'/{"error": "{err}","course_id": {course_id}/}'
        print(f"Failure on course {course_id}")
    return current_answer

if __name__ == '__main__':
    from_dt = datetime.datetime(year=2022, month=9, day=25, hour=0, minute=0, second=0)
    to_dt = datetime.datetime(year=2022, month=9, day=30, hour=0, minute=0, second=0)
    stat = get_course_period_statistics(course_id, from_dt, to_dt, token)
    print(stat)
