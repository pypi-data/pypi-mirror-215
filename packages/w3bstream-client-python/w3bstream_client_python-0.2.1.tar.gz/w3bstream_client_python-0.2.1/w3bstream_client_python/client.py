import json
import requests
import datetime


class Client:
    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.api_key = api_key

    # TODO: support push_data non-blocking, which can send data async in batch
    # TODO: make push_data non-panic
    def push_data(self, deviceID, data, event_type="DEFAULT"):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_key,
        }
        body = {
            'device_id': deviceID,
            'event_type': event_type,
            'payload': data,
            'timestamp':  datetime.datetime.now().isoformat(),
        }
        response = requests.post(
            self.endpoint, data=json.dumps(body), headers=headers)
        print(f"Hello, {self.endpoint}, {self.api_key}, {body}!")
        print(response)
        return response
