import pickle
from datetime import datetime, timedelta

import datefinder
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

def init_credentials():
    #####Configuring credentials
    valid = True
    credentials = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            credentials = pickle.load(token)
        if not credentials.valid:
            valid = False
    if not credentials or valid==False:
        scopes = ['https://www.googleapis.com/auth/calendar']
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=scopes)
        credentials = flow.run_console()
        pickle.dump(credentials, open("token.pkl", "wb"))

def new_event(start, summary, end):
    credentials = pickle.load(open("token.pkl", "rb"))
    #service = build("calendar", "v3", credentials=credentials) # EDIT
    
    #####Creating a service
    #pylint: disable=maybe-no-member
    #result = service.calendarList().list().execute() # EDIT
    calendar_id = 'primary'

    #####Create and event
    event = create_event(credentials,calendar_id,start, summary, end_time_str=end)
    print ('Event created: %s'%(event.get('htmlLink')))

def create_event(credentials,calendar_id,start_time_str, summary, duration=1,end_time_str = None, description=None, location=None):
    service = build("calendar", "v3", credentials=credentials)
    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(hours=duration)

    if(end_time_str):
        matches = list(datefinder.find_dates(end_time_str))
        if len(matches):
            end_time = matches[0]
    print('Datefinder output', datefinder.find_dates(start_time_str))
    print('Start time: ',start_time)
    print('End time: ',end_time)
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Europe/Madrid',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Europe/Madrid',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    #pylint: disable=maybe-no-member
    return service.events().insert(calendarId=calendar_id, body=event).execute()
