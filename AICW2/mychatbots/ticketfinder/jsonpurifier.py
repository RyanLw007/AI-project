import _json


def purify_json(file_path):
    """
    Clears all data from a JSON file by overwriting it with a empty list.

    Args:
    file_path (str): The path to the JSON file to clear.
    """
    with open(file_path, 'w') as file:
        json.dump([], file)  


