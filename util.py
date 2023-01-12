import json
from requests import Session
import io
import base64

API_KEY = 'AIzaSyBmvLkfgQ_ZgTtp_Ub1Flt2ul1WUnvEcCM' # Update your own API key here

def encode_image_from_file(file_name):
    with io.open(file_name, 'rb') as image_file:
        return base64.b64encode(image_file.read())


def callAPI(image_base64, mode='default'):

    req_data = {
        "requests": [
            {
                "features": [
                    {
                        "maxResults": 10,
                        "type": "OBJECT_LOCALIZATION"
                    },
                    {
                        "maxResults": 10,
                        "type": "LOGO_DETECTION"
                    },
                    {
                        "maxResults": 10,
                        "type": "LABEL_DETECTION"
                    },
                    {
                        "maxResults": 10,
                        "type": "IMAGE_PROPERTIES"
                    },
                    {
                        "maxResults": 10,
                        "type": "TEXT_DETECTION"
                    },
                ],
                "image": {
                    "content": image_base64.decode('utf-8')
                }
            }
        ]
    }

    if mode == 'LOC':
        req_data = {
            "requests": [
                {
                    "features": [
                        {
                            "maxResults": 50,
                            "type": "OBJECT_LOCALIZATION"
                        }
                    ],
                    "image": {
                        "content": image_base64.decode('utf-8')
                    }
                }
            ]
        }
    if mode == 'LABEL':
        req_data = {
            "requests": [
                {
                    "features": [
                        {
                            "maxResults": 10,
                            "type": "LABEL_DETECTION"
                        }
                    ],
                    "image": {
                        "content": image_base64.decode('utf-8')
                    }
                }
            ]
        }

    req_data_json_obj = json.dumps(req_data)
    req_data_json_obj_size = len(req_data_json_obj)

    # set hearders
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(req_data_json_obj_size)
    }

    # set api key
    api_key = API_KEY

    parameters = {
        'key': api_key
    }

    # set endpoint
    url = "https://vision.googleapis.com/v1/images:annotate"

    # send request
    session = Session()
    session.headers.update(headers)
    response = session.post(url, params=parameters, data=req_data_json_obj)

    data = json.loads(response.text)

    return data
