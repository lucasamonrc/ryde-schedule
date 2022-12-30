import requests
import json
import boto3
from bs4 import BeautifulSoup

def lambda_handler(event, context):
  ROUTES = {
    "branbury": "https://studentmovement.byu.edu/branbury-route",
    "wyview": "https://studentmovement.byu.edu/wyview-route",
    "joaquin": "https://studentmovement.byu.edu/joaquin-route",
    "king henry": "https://studentmovement.byu.edu/king-henry-route",
    "rec center": "https://studentmovement.byu.edu/west-route",
    "wymount": "https://studentmovement.byu.edu/wymount-route",
    "byu west": "https://studentmovement.byu.edu/byu-west-campus"
  }

  scrapedData = {}

  for route in ROUTES:
    response = requests.get(ROUTES[route])
    html = BeautifulSoup(response.content, "html.parser")
    rows = html.find("table").find("tbody").find_all("tr")
    data = []

    for row in rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      data.append([ele if ele else '-' for ele in cols])

    scrapedData[route] = {}
    for i in range(len(data)):
      for j in range(len(data[i])):
        if i == 0:
          scrapedData[route][data[i][j]] = []
        else:
          scrapedData[route][data[0][j]].append(data[i][j])

  schedule = {}
  for route in scrapedData:
    for point in scrapedData[route]:
      station = point.lower().split('to')[0].strip()
      
      if station not in schedule:
        schedule[station] = {}

      schedule[station][route] = scrapedData[route][point]  

  json_data = json.dumps(schedule, indent = 4)

  s3 = boto3.client("s3")
  s3.put_object(Body=json_data, Bucket="ryde-schedule", Key="schedule.json", ACL="public-read")
  
  return {
    'statusCode': 200,
    'body': json.dumps('Scraped successfully')
  }

lambda_handler(None, None)