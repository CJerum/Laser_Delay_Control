import numpy as np
import PySimpleGUI as sg
import json
import os
""" General Outline:

INITIALIZATION (on startup)
/ set photo number to 0001
/ connect to camera
/ connect to DG535
/ connect to SDG2000x
/ open camera api (?)
-----------------------------

LOOPING
/ update photo number
/ trigger camera (x10)
/ update DG535 delay
/ update SDG2000x delay
/ return
"""
disappointed_dad_error_msg = "You either can't type correctly or maybe you just can't read directions. I expected better from you and honestly, I'm disappointed in you. Try again"


# arbitrary initial values
num_tokens = 2 #adjust this manually to correspond with the number of commands available for the user to select

#num_photos_per_cycle, delay_increment, min_delay, max_delay_SDG
num_photos_per_cycle = 100
delay_increment = 1
min_delay = 10
max_delay_SDG = 1000

# FUNCTIONS
def collect_data(num_photos_per_cycle, delay_increment, min_delay, max_delay_SDG):


    #SCRIPT TO DO EVERYTHING HERE
    #camera trigger
    #update photo number

    layout = [  [sg.Text(f"Initial Delay of SDG2000x: {max_delay_SDG}")],
                [sg.Text(f"Minimum Delay of SDG2000x: {min_delay}")],
                [sg.Text(f"Number of Photos Per Cycle: {num_photos_per_cycle}")],
                [sg.Text(f"Delay Increment: {delay_increment}")]]
    print("beep boop collecting data :)")
    window = sg.Window('Current Job Information', layout)
    event, values = window.read()

    return

def load_profile():
    try:
        with open('profiles.txt', 'r') as file:
            lines = file.readlines() #print(lines) returns ['{"name": "profile1", "data": [100, 17, 10, 10]}\n']        
        print("PROFILES:")
        for index, line in enumerate(lines): #enumerate—goes over each line in profiles.txt
            profile = json.loads(line.strip()) #print(profile) returns {'name': 'profile1', 'data': [100, 17, 10, 10]}
            #^json.loads converts the string into a dictionary
            print(profile)
            print("INDEX PROFILE [num_photos_per_cycle, delay_increment, min_delay, initial_delay_SDG]")
            print(f"{index}: {profile['name']} - {profile['data']}")
        
        while True:
            try:
                which_profile = int(input("Select Profile to Load (enter index): "))
                if 0 <= which_profile < len(lines):
                    break
                else:
                    print("Invalid index. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        selected_profile = json.loads(lines[which_profile].strip())
        a, b, c, d = selected_profile['data']
        
        print(f"Loaded profile: {selected_profile['name']}")
        print(f"max_delay_SDG = {a}, min_delay = {b}, num_photos_per_cycle = {c}, delay_increment = {d}")
        
        return a, b, c, d
    
    except FileNotFoundError:
        print("profiles.txt file not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the file. Make sure the file is properly formatted.")

def save_profile(max_delay_SDG, min_delay, num_photos_per_cycle, delay_increment):
    try:
        print("Current Parameters:")
        print(f"Initial Delay of SDG2000x: {max_delay_SDG}")
        print(f"Minimum Delay of SDG2000x: {min_delay}")
        print(f"Number of Photos Per Cycle: {num_photos_per_cycle}")
        print(f"Delay Increment: {delay_increment}")
        
        while True:
            yn = input("Save This Profile? (y/n): ").lower()
            if yn in ['y', 'yes', 'n', 'no']:
                break
            print("Invalid Input. Please enter 'y' or 'n'.")
        
        if yn in ['y', 'yes']:
            profile_name = input("Enter desired profile name: ")
            profile_data = {
                "name": profile_name,
                "data": [max_delay_SDG, min_delay, num_photos_per_cycle, delay_increment]
            }
            
            # Convert the profile data to a JSON string
            profile_json = json.dumps(profile_data)
            
            # Write the JSON string to a file
            with open('profiles.txt', 'a') as file:
                file.write(profile_json + '\n')  # Add a newline to separate entries
            
            print('-'*50)
            print(f'PROFILE "{profile_name}" SUCCESSFULLY SAVED')
            print('-'*50)
        else:
            print('-'*50)
            print("SAVE PROFILE OPERATION CANCELLED")
            print('-'*50)
    
    except ValueError:
        print("VALUE ERROR—Do you have any parameters currently set?")
# command line output to user upon intialization of code
def set_token():
    print('-'*50, "MAIN MENU", '-'*50)
    print("(1) SET PARAMETERS")
    print("(2) BEGIN DATA COLLECTION")
    print("(3) SAVE PROFILE")
    print("(4) LOAD PROFILE")
    print("(5) PRINT CURRENT PARAMETERS")

    while True:
        try:
            token = int(input("Enter Token:"))
            print("Valid token")
            print()
            break
        except ValueError:
            print(disappointed_dad_error_msg)
            print()
    return token

print("Welcome to the 'Junction Activated Mechanism with Electronic Setup and Interface Support to Accomplish Completely Autonomous Triggering (JAMES IS A CAT)' program; Please follow the directions below.")
print()
print("Please select one of the following tokens by inputting the number it corresponds to:")
print()
print() #blank space

# get token—input from user
token = set_token()
# actual commands
if token == 1: # (1) collect_data
    def collect_data():
    while True:
        try:
            num_photos_per_cycle = int(input("Enter desired number of photos per cycle:"))
            break
        except ValueError:
            print(disappointed_dad_error_msg)
            print()

    while True:
        try:
            delay_increment = int(input("Enter desired delay increment:"))
            break
        except ValueError:
            print(disappointed_dad_error_msg) 
            print()

    while True:
        try:
            min_delay = int(input("Enter desired minimum delay:"))
            break
        except ValueError:
            print(disappointed_dad_error_msg) 
            print()

    while True:
        try:
            max_delay_SDG = int(input("Enter desired starting delay for SDG2000x:"))
            break
        except ValueError:
            print(disappointed_dad_error_msg) 
            print()
    print('-'*50, "PARAMETERS SUCCESSFULLY INTIALIZED", '-'*50)
    print()
    set_token()
    #collect_data(num_photos_per_cycle, delay_increment, min_delay, max_delay_SDG)
    

elif token == 2: # (2) BEGIN DATA COLLECTION
    #collect_data(num_photos_per_cycle, delay_increment, min_delay, max_delay_SDG)
    delay_array = np.linspace(min_delay, max_delay_SDG, delay_increment)
    total_photos = int(len(delay_array))
    current_delay = max_delay_SDG
    while current_delay>min_delay:
        try:
            #take a photo
            #repeat for however many photos per cycle (num_photos_per_cycle)
            current_delay -= delay_increment #increment delay =
            
            #repeat
        except ValueError:
            print(disappointed_dad_error_msg) 
            print()
    set_token()

elif token == 3:  # (3) SAVE PROFILE
    save_profile(max_delay_SDG, min_delay, num_photos_per_cycle, delay_increment)
    set_token()
elif token == 4:  # (4) load profiles
def load_profiles():    
    max_delay_SDG, min_delay, num_photos_per_cycle, delay_increment = load_profile()
    print('-'*50, "PROFILE SUCCESSFULLY LOADED", '-'*50)
    print(f'Max Delay: {max_delay_SDG}')
    print(f'Minimum Delay: {min_delay}')
    print(f'Delay Increment: {delay_increment}')
    print(f'# Photos per Cycle: {num_photos_per_cycle}')
    print()
    set_token()

elif token == 5: # (5) Print Current Parameters
    print("Current Parameters:")
    print(f"Initial Delay of SDG2000x: {max_delay_SDG}")
    print(f"Minimum Delay of SDG2000x: {min_delay}")
    print(f"Number of Photos Per Cycle: {num_photos_per_cycle}")
    print(f"Delay Increment: {delay_increment}")
    print()
    set_token()
#num_photos_per_cycle, delay_increment, min_delay, max_delay_SDG
