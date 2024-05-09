import _json


def purify_json(file_path):
    """
    Resets the JSON file to a default state with predefined keys and values.

    Args:
    file_path (str): The path to the JSON file to clear.
    """
    default_data = {
        "chosen_origin_str": "Norwich",
        "chosen_dest_str": None,
        "arrive_date_str": None,
        "arrive_time_str": None,
        "leave_date_str": None,
        "leave_time_str": None,
        "ticket_type": None,
        "leave_arrive": None,
        "origin_code": "NRW",
        "dest_code": None,
        "chosen_intention": None
    }

    try:
        with open(file_path, 'w') as file:
            json.dump(default_data, file, indent=4)  
        print("JSON file has been reset to default.")
    except Exception as e:
        print(f"An error occurred: {e}")


