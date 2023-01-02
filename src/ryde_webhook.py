from datetime import datetime

import requests
import json

SCHEDULE_URL = "https://ryde-schedule.s3.us-west-2.amazonaws.com/schedule.json"

def get_current_time():
  now = datetime.now()
  return now.strftime("%H:%M").lower()

def find_next_hour(hours, current_hour):
  for hour in hours:
    if hour == '-':
      continue

    if hour[1] == ':':
      hour = '0' + hour

    if hour > current_hour:
      return hour

  return 'There are no buses coming.'
  
def lambda_handler(event, context):
  now = get_current_time()
  today = datetime.today()

  if today.weekday() in [5,6] or today.month in range(5, 9):
    return 'No services today'

  schedule = requests.get(SCHEDULE_URL).json()

  results = event["body"].lower().split(":")
  station, route = results[0], None if len(results) < 2 else results[1]

  if station not in schedule:
    print('Invalid station name. Please try again using one of the stations below:')
    out = '\n'.join(['- ' + key for key in schedule])
    return out

  stationSchedule = schedule[station]

  departures = {}
  for _route in stationSchedule:
    departures[_route] = find_next_hour(stationSchedule[_route], now)

  if route:
    return departures[route]

  return departures

event = {}
event["body"] = "moa"

res = lambda_handler(event, None)
print(res)