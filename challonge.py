import os
import urllib3
from urllib.parse import urlencode

MATCH_UPDATE_URL = "https://api.challonge.com/v1/tournaments/3133599/matches/{}.json"

def getUpdateUrl(match_id):
    return MATCH_UPDATE_URL.format(match_id)

"""
record is match record db row tuple
"""
def updateMatchRecord(record):
    if 'BADR_CHALLONGE_KEY' not in os.environ:
        return False

    http = urllib3.PoolManager()
    encoded_args = urlencode(
        {
            'api_key': os.environ['BADR_CHALLONGE_KEY'],
            'match[scores_csv]': '{}-{}'.format(record[3], record[4]),
            'match[winner_id]': record[5]
        })
    url = getUpdateUrl(record[0]) + '?' + encoded_args
    response = http.request('PUT', url)
    print("Update to challonge:", response.status)
    return response.status == 200
