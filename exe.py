import requests


# 2.1  send serial 1 and 2 and receive json

# function to get json by serial id
def get_json_by_serial(serial):
    url = f"https://resttest10.herokuapp.com/api/responses?serial={serial}"
    response = requests.get(url)

    # check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"error getting json for serial={serial}. status code: {response.status_code}")
        return None


json_serial_1 = get_json_by_serial(1)
json_serial_2 = get_json_by_serial(2)


# 2.2 send json for processing

# function to send json for processing
def send_json_for_processing(json_data):
    url = "https://resttest10.herokuapp.com/api/process"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=json_data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"error sending json for processing. status code: {response.status_code}")
        return None


if json_serial_1 is not None and json_serial_2 is not None:

    # get max quantities from json responses
    quantities_first = max(json_serial_1['message']['subset']['general']['quantities']['first'],
                           json_serial_2['message']['subset']['general']['quantities']['first'])

    quantities_second = max(json_serial_1['message']['subset']['general']['quantities']['second'],
                            json_serial_2['message']['subset']['general']['quantities']['second'])

    quantities_third = max(json_serial_1['message']['subset']['general']['quantities']['third'],
                           json_serial_2['message']['subset']['general']['quantities']['third'])
    # create the json to process
    json_to_process = {
        "serial": 3,
        "message": {
            "subset": {
                "general": {
                    "information": {
                        "date": "1-2-2021",
                        "version": "3.00"
                    },
                    "quantities": {
                        "first": quantities_first,
                        "second": quantities_second,
                        "third": quantities_third
                    }
                }
            }
        }
    }

    # Send json for processing
    response = send_json_for_processing(json_to_process)

    # Check if processing was successful
    if response.get("message") == "correct":
        print("Processing successful")
    else:
        print("Processing failed")
else:
    print("error retrieving json. Please check the logs for details.")
