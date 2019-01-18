# Picking From Airport

## Project Idea:
To determine when one should leave home to go pick up family and friends from the airport. 

## Tech Stack
- S3
- Airflow: scheduler 
- Spark: data processing
- (TBA): database
- Flask: dashboard

## Data Source
Data Needed:
- Flight Arrival Times
- Airpot Satistics (such as size and terminals)
- Traffic data

Bureau of Transportation: https://www.bts.gov/topics/airlines-and-airports-0
- csv files 
- size: ~10 GB

Using some Maps Api to determine time of travel to airport.

## Engineering Challenge
1. Combining data sets
2. Maintaining and updating airlines data 
3. Stimulating as real-time streaming 
4. Processing user requests 

## Business Value
This platform will tell you when to leave for the airport to pick-up your party, so that you are not cirling the airport waiting for them to walk-out.

## MVP
Store data in S3. 
Given any flight info and current location of user, determine when to leave for the airport. (Does not take into account any temporal factors)

## Stretch Goals
Create notifications telling user that it is time to leave for the airport. 
Using the similar idea, determine when to get drop-off people at the airport, by taking into account time to checkin bags and got through security check. 