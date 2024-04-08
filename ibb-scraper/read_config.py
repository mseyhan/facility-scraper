import json
# Define the path to your config file
config_file_path = 'data/config.json'

# Function to read the config file and return the tc and password
def read_config(file_path):
    try:
        # Open the config file
        with open(file_path, 'r') as file:
            # Parse the JSON data
            config = json.load(file)
        
        # Extract the tc and password values
        tc = config.get('tc', 'default_tc_if_not_found')
        password = config.get('password', 'default_password_if_not_found')
        link = config.get('link', 'https://online.spor.istanbul/uyegiris')
        timeslot = config.get('timeslot', '22:00 - 23:00')
        plus = config.get('plus', 3)
        timer_hms = (config.get('timer_hour', 22), 
                     config.get('timer_minute',0), 
                     config.get('timer_second',0))
        return tc, password, link, timeslot, plus, timer_hms
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None, None
    except json.JSONDecodeError:
        print("Error: There was an issue decoding the JSON file.")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

# Use the function and print the results
tc, password, link, timeslot, plus, timer_hms = read_config(config_file_path)
print(timer_hms)