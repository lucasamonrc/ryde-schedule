from datetime import datetime

import requests
import json

SCHEDULE_URL = "https://ryde-schedule.s3.us-west-2.amazonaws.com/schedule.json"

def get_current_time():
  now = datetime.now()
  return now.strftime("%I:%M %p").lower()

def find_next_hour(hours, current_hour):
  current_hour = current_hour.lower()
  next_hour = None
  
  for hour in hours:
    hour = hour.lower()

    if hour > current_hour:
        next_hour = hour
        break
        
  return next_hour

def lambda_handler(event, context):
  schedule = requests.get(SCHEDULE_URL).json()

  results = event["body"].lower().split(":")
  station, route = results[0], None if len(results) < 2 else results[1]

  if station not in schedule:
    print('Invalid station name. Please try again using one of the stations below:')
    out = '\n'.join(['- ' + key for key in schedule])
    print(out)  
    return

  stationSchedule = schedule[station]
  now = get_current_time()

  departures = {}
  for route in stationSchedule:
    departures[route] = find_next_hour(stationSchedule[route], now)

  print(departures)

  

  
event = {}
event["body"] = "moa"


lambda_handler(event, None)