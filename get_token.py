import requests
from dotenv import load_dotenv
from os import environ

load_dotenv()

def get_token():

    url = "https://acc2-oc.hospitality-api.us-ashburn-1.ocs.oraclecloud.com/oauth/v1/tokens"

    payload = {'username': environ['OHIP_USER'],
               'password': environ['OHIP_PASS'],
               'grant_type': 'password'}

    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'x-app-key': environ['OHIP_APP_KEY'],
    'Authorization': 'Basic QUNDT1JBVF9DbGllbnQ6eWJRWDV4by1iS1dKVFhYcHBVamZULWxS'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.ok:

        return response.json()['access_token']
    else:
        print(response.text)
        return None
