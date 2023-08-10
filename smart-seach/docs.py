import json

def jsonContext():

    dataResult = {'keys': {}, 'topics': None}

    # Specify the path to your JSON file
    data = 'document.json'

    # Load the JSON file
    with open(data, 'r') as file:
        json_data = json.load(file)
        dataResult['topics'] = json_data

        # Get the primary keys
        primary_keys = list(json_data.keys())

        # Print the primary keys
        for index, key in enumerate(primary_keys):
            dataResult['keys'][index] = key

    return dataResult
