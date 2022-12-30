import requests
import json
import boto3
from bs4 import BeautifulSoup

routes = {
  "branbury": "https://studentmovement.byu.edu/branbury-route",
  "wyview": "https://studentmovement.byu.edu/wyview-route",
  "joaquin": "https://studentmovement.byu.edu/joaquin-route",
  "king henry": "https://studentmovement.byu.edu/king-henry-route",
  "rec center": "https://studentmovement.byu.edu/west-route",
  "wymount": "https://studentmovement.byu.edu/wymount-route",
  "byu west": "https://studentmovement.byu.edu/byu-west-campus"
}

schedule = {}

def lambda_handler(event, context):
  for route in routes:
    response = requests.get(routes[route])
    html = BeautifulSoup(response.content, "html.parser")
    rows = html.find("table").find("tbody").find_all("tr")
    data = []

    for row in rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      data.append([ele for ele in cols if ele])

    schedule[route] = {}

    for i in range(len(data)):
      for j in range(len(data[i])):
        if i == 0:
          schedule[route][data[i][j]] = []
        else:
          schedule[route][data[0][j]].append(data[i][j])
        
  json_data = json.dumps(schedule, indent = 4)

  with open("temp/data.json", "w") as outfile:
    outfile.write(json_data)

  s3 = boto3.client("s3")
  s3.upload_file(Filename="data.json", Bucket="ryde-schedule", Key="schedule.json", ExtraArgs={'ACL':'public-read'})

  return {
    'statusCode': 200,
    'body': json.dumps('Scraped successfully')
  }