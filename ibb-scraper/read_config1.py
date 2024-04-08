import json
from time import sleep
import datetime
import runpy

def read_config(file_path):
    """
    Reads a configuration file and extracts specific settings.

    Parameters:
    - file_path (str): The path to the configuration file.

    Returns:
    - tuple: Contains the extracted tc, password, link, timeslot, plus, and timer settings.
      Returns None for each value if the file cannot be read or parsed.
    """
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        
        tc = config.get('tc', 'default_tc_if_not_found')
        password = config.get('password', 'default_password_if_not_found')
        link = config.get('link', 'https://online.spor.istanbul/uyegiris')
        timeslot = config.get('timeslot', '22:00 - 23:00')
        plus = config.get('plus', 3)
        timer_hms = (config.get('timer_hour', 22), 
                     config.get('timer_minute', 0), 
                     config.get('timer_second', 0))
        bransadi = config.get('bransadi', "TENİS")
        tesisadi = config.get('tesisadi', "MALTEPE SAHİL SPOR TESİSİ")
        salonadi = config.get('salonadi', "KAPALI TENIS KORTU 3")
        return tc, password, link, timeslot, plus, timer_hms, bransadi, tesisadi, salonadi
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
    except json.JSONDecodeError:
        print("Error: There was an issue decoding the JSON file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None, None, None, None, None, None
