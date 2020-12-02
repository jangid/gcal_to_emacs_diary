#!/usr/bin/env python3

from __future__ import print_function
from datetime import datetime, timezone, timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Export Google Calendar to an .ics file.
    Prints the start and name of the events for next 30 days from the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    today = datetime.now(timezone.utc)
    one_week = timedelta(weeks=1)
    four_weeks = timedelta(weeks=4)
    timeFrom = (today - one_week).isoformat()
    timeTo = (today + four_weeks).isoformat()
    events_result = service.events().list(calendarId='primary',
                                          timeMin=timeFrom,
                                          timeMax=timeTo,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    for event in events:
        start = datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date')))
        end = datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date')))
                
        print(f"{start.strftime('%m/%d/%Y')} {start.strftime('%H:%M')}-{end.strftime('%H:%M')} {event['summary']}")


if __name__ == '__main__':
    main()
