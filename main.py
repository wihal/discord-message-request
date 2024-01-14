import requests
from random import randint
import os
import sys
import json
from time import sleep
import re


print("""

-----------------------------------------------------------------------------

   (  )   /\   _                 (     
    \ |  (  \ ( \.(               )                      _____
  \  \ \  `  `   ) \             (  ___                 / _   \\
 (_`    \+   . x  ( .\            \/   \____-----------/ (o)   \_
- .-               \+  ;          (  O                           \____
                          )        \_____________  `              \  /
(__                +- .( -'.- <. - _  VVVVVVV VV V\                 \/
(_____            ._._: <_ - <- _  (--  _AAAAAAA__A_/                  |
  .    /./.+-  . .- /  +--  - .     \______________//_              \_______
  (__ ' /x  / x _/ (                                  \___'          \     /
 , x / ( '  . / .  /                                      |           \   /
    /  /  _/ /    +                                      /              \/
   '  (__/                 von Max und Willi           /                  \\
      
-----------------------------------------------------------------------------
""")

# Funktioniert einfach keine ahnung wie. Danke Bro https://stackoverflow.com/a/31966932/16335953
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2 # Noch nie davon gehört
    except Exception:
        base_path = os.path.abspath(".")

    result = os.path.join(base_path, relative_path)
    return result 

def main(selected_group_profile, time_interval, header_content):
    file_path = resource_path("src/saves.json")
    
    with open(file_path, "r") as file:
        data = json.load(file)

    groups = data["groups"][selected_group_profile]
    ids = [int(id) for id in groups]
    print(groups)

    runs = 0
    messages_sent = 0

    while True:
        with open(resource_path("src/message_content.txt"), "r") as file: # Im while look das message_content.txt bearbeitet werden kann
                message_content = file.read()
        for i in ids:
            print("try sending message to " + str(i))
            random_zahl = randint(1,1000000000) # Don't touch this it works don't ask why

            url = f"https://discord.com/api/v9/channels/{i}//messages"

            payload = {
                "mobile_network_type": "unknown",
                "content": f"{message_content}",
                "nonce": random_zahl,
                "tts": False,
                "flags": 0
            }

            headers = header_content

            print(headers)

            response = requests.request("POST", url, json=payload, headers=headers)

            runs += 1
            print("total messages: " + str(runs))

            if response.status_code == 200:
                messages_sent += 1
                print("messages sent: " + str(messages_sent))
                print("successfully sent message to " + str(i))
                print("next message in " + str(time_interval) + " seconds")
                sleep(time_interval)
            elif response.status_code == 429:
                print("Rate limited. Waiting 5 seconds...")
                sleep(5)
            elif response.status_code == 404:
                print("not found")
                print(response.content)


def group_choice():
    file_path = resource_path("src/saves.json")
    
    with open(file_path, "r") as file:
            data = json.load(file)

    os.system('cls' if os.name == 'nt' else 'clear')
              
    print("\n Choose able groups: ")
    console_line()
    a = 0
    for i in data["groups"]:
        a += 1
        print(i)

    if a==0:
        print("No groups found. Please add some.")
        console_line()
        sleep(2)
        load()
    console_line()
    return data, file_path

def add():
    file_path = resource_path("src/saves.json")
    
    with open(file_path, "r") as file:
            data = json.load(file)
    
    os.system('cls' if os.name == 'nt' else 'clear')

    new_group_name = input("\nEnter the name of the new group: ")
    console_line()

    if new_group_name == "z":
        return None

    if new_group_name in data["groups"]:
        print("Group already exists.")
    else:
        new_group_ids = input(f"\nEnter the IDs for the group '{new_group_name}' (comma-separated): ")
        new_group_ids_list = [int(id.strip()) for id in new_group_ids.split(',')]
        
        data["groups"][new_group_name] = new_group_ids_list
        
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        
        print(f"Group '{new_group_name}' added successfully with IDs {new_group_ids_list}.")
    console_line()
    
def update():
    data, file_path = group_choice()
    
    existing_group_name = input("\nEnter the name of the existing group: ")
    console_line()

    if existing_group_name == "z":
        return None

    if existing_group_name not in data["groups"]:
        print(f"Group '{existing_group_name}' does not exist.")
    else:
        existing_group = data["groups"][existing_group_name]
        
        new_group_ids = input(f"Enter the new IDs for the group '{existing_group_name}' (comma-separated): ")
        new_group_ids_list = [int(id.strip()) for id in new_group_ids.split(',')]
        
        data["groups"][existing_group_name] = new_group_ids_list
        
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        
        print(f"Group '{existing_group_name}' updated successfully with new IDs {new_group_ids_list}.")
    console_line()

def delete():
    data, file_path = group_choice()
    
    group_to_delete = input("\nEnter the name of the group to delete: ")

    if group_to_delete == "z":
        return None
    
    if group_to_delete not in data["groups"]:
        print(f"group '{group_to_delete}' does not exist.")
    else:
        del data["groups"][group_to_delete]
        
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        
        print(f"group '{group_to_delete}' deleted successfully.")
    console_line()

def append():
    data, file_path = group_choice()

    group_to_append = input("\nEnter the name of the group to append to: ")
    if group_to_append == "z":
        return None

    if group_to_append not in data["groups"]:
        print(f"Group '{group_to_append}' does not exist.")
    else:
        existing_group = data["groups"][group_to_append]
        
        new_group_ids = input(f"Enter the new IDs to append to the group '{group_to_append}' (comma-separated): ")
        new_group_ids_list = [int(id.strip()) for id in new_group_ids.split(',')]
        
        existing_group.extend(new_group_ids_list)
        
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        
        print(f"IDs appended to group '{group_to_append}' successfully: {new_group_ids_list}.")
    console_line()

def load_headers(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read the cURL command from the file
            curl_command = file.read()

            # Search for the authorization token in the cURL command
            match = re.search(r"-H 'authorization: (.*?)'", curl_command)

            # Check if a match is found
            if match:
                # Extract the authorization token
                authorization_token = match.group(1)
                return {"authorization": authorization_token}
            else:
                print(f'Authorization token not found in file {file_path}')
                return None
    except FileNotFoundError:
        print(f'Datei nicht gefunden: {file_path}')
        return None

        return None

def header_files():
    folder_path = resource_path('src')  # Replace with the actual folder path

    os.system('cls' if os.name == 'nt' else 'clear')
              
    print("\n Chooseable Accounts: ")
    console_line()
    
    a = 0
    for filename in os.listdir(folder_path):
        if not filename == "message_content.txt":
            if filename.endswith(".txt"):
                a += 1
                # Remove the ".txt" extension
                print(os.path.splitext(filename)[0])

    if a==0:
        print("No Accounts found. Drop them in the src folder.")
        console_line()
        sleep(4)
        load()
    console_line()
    return None

def console_line(länge: int = 22):
    bindestriche = "".join("-" for _ in range(länge))
    print(bindestriche)

def start():
    data, file_path = group_choice()

    group_name = input("\nEnter the name of the group: ")
    if group_name == "z":
        return None

    time_interval = float(input("\nTime Interval: "))

    console_line()

    header_files()

    headers_file_name = input("\nEnter the name of the Account: ")

    if headers_file_name == "z":
        return None

    header_content = load_headers(resource_path("src\\" + headers_file_name + ".txt"))

    main(group_name, time_interval, header_content)
    
def load():
    sleep(1.5) # Unnötig aber sieht cool aus
    while True:
        sleep(0.5) # Unnötig aber sieht cool aus
        os.system('cls' if os.name == 'nt' else 'clear')
        
        to = str(input("""\nUse the following commands: \n 
                       start script: (start/s)
                       add group: (add/a)
                       update group: (update/u)
                       delete group: (delete/d)
                       append group: (append/ap) 
                       how to add a new account: (account/ac)

                       you can always type "z" to go back to the main menu

                       type here:
                       """))
        console_line()

        print(to)
        if to == "start" or to == "s":
            start()
        elif to == "add" or to == "a":
            add()
        elif to == "update" or to == "u":
            update()
        elif to == "delete" or to == "d":
            delete()
        elif to == "append" or to == "ap":
            append()
        elif to == "account" or to == "ac":
            append()
        else:
            print("invalid input")
            pass

def account():
    print("how to add a new account")
    console_line()
    print("1. create a new .txt file in the src folder (the name of the file is also the name of the account)")
    print("2. copy a message request using the network tool of your browser")
    
def check():
    # Prüfung ob src/ Vorhanden ist
    folder_path = resource_path("src")
    try:
        os.makedirs(folder_path)
    except FileExistsError:
        pass

    # Prüfung ob src/saves.json Vorhanden ist
    message_content_path = resource_path("src/message_content.txt")
    if not os.path.exists(message_content_path):
        with open(message_content_path, "w") as file:
            file.write("Default message content")

    # Prüft ob src/saves.json Vorhanden ist
    saves_path = resource_path("src/saves.json")
    if not os.path.exists(saves_path):
        default_data = {
            "groups": {}
        }
        with open(saves_path, "w") as file:
            json.dump(default_data, file, indent=4)

if __name__ == '__main__':
    check()
    load()