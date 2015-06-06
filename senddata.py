__author__ = 'nii236'

import requests, json
from pprint import pprint as pp


DB_WRITE_URL = "http://127.0.0.1:64210/api/v1/write"
DB_QUERY_URL = "http://127.0.0.1:64210/api/v1/query/gremlin"
DB_WRITE_HEADERS = {'Content-type': 'application/json'}


def process_data_to_string(data):
    for dict in data:
        for key in dict:
            dict[key] = str(dict[key])
    return data


def send_data(data):
    data = process_data_to_string(data)
    r = requests.post(DB_WRITE_URL, data=json.dumps(data), headers=DB_WRITE_HEADERS)
    pp(r)
    pp(r.text)