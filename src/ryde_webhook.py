from datetime import datetime

import requests
import json
import pytz

SCHEDULE_URL = "https://ryde-schedule.s3.us-west-2.amazonaws.com/schedule.json"

def get_current_time():
  now = datetime.now(pytz.timezone('America/Denver'))
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
  
def process(body):
  now = get_current_time()
  today = datetime.now(pytz.timezone('America/Denver'))

  if today.weekday() in [5,6] or today.month in range(5, 9):
    return 'No services today'

  schedule = requests.get(SCHEDULE_URL).json()

  results = body.lower().split("%3a")
  station, route = results[0].strip(), None if len(results) < 2 else results[1].strip()

  if station not in schedule:
    out = 'Invalid station name. Please try again using one of the stations below:\n'
    out += '\n'.join(['- ' + key for key in schedule])
    return out

  stationSchedule = schedule[station]

  departures = {}
  out = 'Next departure times at this station:\n'
  for _route in stationSchedule:
    departures[_route] = find_next_hour(stationSchedule[_route], now)
    out += f"- {_route}: {departures[_route]}\n"

  if route:
    return departures[route]

  return out

def lambda_handler(event, context):
  body = event['Body'].replace("+", " ").strip()
  reply = process(body)
  return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"\
          f"<Response><Message><Body>{reply}</Body></Message></Response>"