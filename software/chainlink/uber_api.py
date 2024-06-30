
from dataclasses import dataclass
import requests
import json

url = "https://api.uber.com/v1/guests/trips/estimates"

@dataclass
class Coordinates:
    latitude: int
    longitude: int

HOME_COORDINATES = Coordinates(36.223364, -86.763699)
BROADWAY_COORDINATES = Coordinates(36.163181, -86.780613)



def get_estimate_to_broadway():
    payload =  f"""{
        "pickup":{
            "latitude":{HOME_COORDINATES.latitude},
            "longitude":{HOME_COORDINATES.longitude}
            },
        "dropoff":{
                "latitude":{HOME_COORDINATES.latitude},
                "longitude":{HOME_COORDINATES.longitude}
            }
        }"""
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def get_auth_token():
    pass


get_estimate_to_broadway()
