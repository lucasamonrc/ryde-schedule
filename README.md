# 🚌 The Ryde Schedule

A serverless function triggered by an SMS that scrapes BYU student movement website and returns the departure time of the next BYU Ryde shuttle for a particular route.

This project is still under development. For more detailed information on what still needs to be done, please visit the [issues](https://github.com/lucasamonrc/ryde-schedule/issues) tab.

## 🎯 Justification

[BYU](https://www.byu.edu) has a great free shuttle service that can transport students efficiently across campus and/or on-campus housing. It connects BYU grounds through 7 different routes as describe in their [website](https://studentmovement.byu.edu). Being a frequent user of the BYU Ryde (the name of the shuttle service), I wasted a lot of time opening up an internet browser on my phone, typing the URL, navigating to my route's page, and then parsing with my eyes a fairly long list with all of the times listed to try to figure out when the next shuttle was departing.

Inspired by the transit system of Porto and Lisbon from the time I lived in Portugal, I decided to write a simple service that can scrape the Ryde's website and then simply inform the time the next shuttle will depart each time I text the service my current stop and route.

## 💻 Project Demo

The Screenshots below are simply concepts and do not represent the final design of the service:

<p float="left" align="center">
  <img src="https://iili.io/HIu0O2j.png" width="35%" />
  <img src="https://iili.io/HIu0wrb.png" width="35%" /> 
</p>

## 🚀 Technology Stack

- [Python](https://www.python.org/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Twilio](https://www.twilio.com/)

Python is the language of choice for writing these scripts and the cloud functions that will be hosted on AWS Lambda. BeautifulSoup is ebough for parsing a simple HTML document and extracting the needed data. Twilio was the obvious choice for a simple and flexible communication service and API.

### Trade-offs Considered

Choosing BeautifulSoup over Selenium was the right choice for this project because the scraped webpages are fairly simple and the scraper itself does not need to interact with the UI of the website. Selenium is powerful, but adds the overhead of configuring volumes with AWS lambda to store the necessary browser drivers, which wasn't needed for this use-case.

## ⚙️ Setup Instructions
 
Setup instructions are still under development.

## 🧑‍💻 Authors

- Lucas Castro ([@lucasamonrc](https://github.com/lucasamonrc)) | [lucasamonrc.dev](https://lucasamonrc.dev) 
