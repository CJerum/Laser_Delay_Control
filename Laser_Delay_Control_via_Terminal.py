import numpy as np
import json
import os
import pyvisa
rm = pyvisa.ResourceManager()

class LaserDelayControl:
    def __init__(self): # intializes all of the varables as having no value. __init__ is the first thing that happens in a class.
        self.max_delay_SDG = None
        self.min_delay = None
        self.num_photos_per_cycle = None
        self.delay_increment = None

    def push_SDG2000x_delay(self,channel,delay): #(channel,delay)
        sdg = rm.open_resource('USB0::0xF4EC::0xEE38::SDG2XCAC1R0015::INSTR')
        sdg.write(f"C{channel}:BSWV DLY,{delay}")
        print(f'successfully pushed delay of {delay} to SDG2000x.')
        print()
        return
    
    def push_DG535_delay(target_channel,reference_channel,delay):
        dg535 = rm.open_resource("GPIB0::GPIB_ADDRESS::INSTR")
        dg535.write(f'DT {target_channel},{reference_channel},{delay}')
        print(f'successfully pushed delay of {delay} to DG535.')
        print()
        return
    
    def set_parameters(self):
        self.num_photos_per_cycle = self.get_int_input("Enter desired number of photos per cycle:")
        self.delay_increment = self.get_int_input("Enter desired delay increment:")
        self.min_delay = self.get_int_input("Enter desired minimum delay:")
        self.max_delay_SDG = self.get_int_input("Enter desired starting delay for SDG2000x:")
        print('-'*50, "PARAMETERS SUCCESSFULLY INITIALIZED", '-'*50)
        self.print_current_parameters()
        return self.max_delay_SDG, self.min_delay, self.num_photos_per_cycle, self.delay_increment
    
    def get_int_input(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print(self.error_msg)
                print()

    def begin_data_collection(self):
        sdg = rm.open_resource('USB0::0xF4EC::0xEE38::SDG2XCAC1R0015::INSTR')
        dg535 = rm.open_resource("GPIB0::GPIB_ADDRESS::INSTR") #PLACEHOLDER ADDRESS FOR NOW!
        rm = pyvisa.ResourceManager()
        if not all([self.max_delay_SDG, self.min_delay, self.num_photos_per_cycle, self.delay_increment]):
            print("Error: Try again after you've set the parameters or loaded one of the profiles.")
            return 

        delay_array = np.linspace(self.min_delay, self.max_delay_SDG, self.delay_increment)
        #value in the line below is only a placeholder! Take note of this!
        delay_difference = 10 #PLACEHOLDER VALUE
        total_photos = int(len(delay_array))
        current_delay = self.max_delay_SDG
        is_automatic = input("automatic data collection? (y/n):")
        if is_automatic == 'y':
            while current_delay > self.min_delay: # looping process
                ### all of the logic for delays and taking photos will go here!!! ###
                current_delay = current_delay - self.delay_increment
                self.push_SDG2000x_delay(1, current_delay) #(channel,delay)
                self.push_DG535_delay(2,3,current_delay + delay_difference) #2=A, 3=B
        else:
            while current_delay > self.min_delay: # looping process

                go_next = input("input anything to continue to next shot. Type 'exit' to terminate program.")
                if go_next == "exit":
                    return
                else:
                    current_delay = current_delay - self.delay_increment
                    self.push_SDG2000x_delay(1, current_delay) #(channel,delay)
                    self.push_DG535_delay(2,3,current_delay + np.abs(delay_difference)) #(target_channel, reference_channel, delay (in sec)). 2=A, 3=B
   
        sdg.close()
        dg535.close()
        print("Data Collection Complete!")
        return

    def save_profile(self):
        if not all([self.max_delay_SDG, self.min_delay, self.num_photos_per_cycle, self.delay_increment]):
            print("Error: Try again after you've set the parameters or loaded one of the profiles.")
            return

        self.print_current_parameters()
        
        while True:
            yn = input("Save This Profile? (y/n): ").lower()
            if yn in ['y', 'yes', 'n', 'no']:
                break
            print("Invalid Input. Please enter 'y' or 'n'.")
        
        if yn in ['y', 'yes']:
            profile_name = input("Enter desired profile name: ")
            profile_data = {
                "name": profile_name,
                "data": [self.max_delay_SDG, self.min_delay, self.num_photos_per_cycle, self.delay_increment]
            }
            
            with open('profiles.txt', 'a') as file:
                file.write(json.dumps(profile_data) + '\n')
            
            print('-'*50)
            print(f'PROFILE "{profile_name}" SUCCESSFULLY SAVED')
            print('-'*50)
        else:
            print('-'*50)
            print("SAVE PROFILE OPERATION CANCELLED")
            print('-'*50)

    def load_profile(self):
        try:
            with open('profiles.txt', 'r') as file:
                lines = file.readlines()
            
            print("PROFILES:")
            for index, line in enumerate(lines):
                profile = json.loads(line.strip())
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
            self.max_delay_SDG, self.min_delay, self.num_photos_per_cycle, self.delay_increment = selected_profile['data']
            
            print(f"Loaded profile: {selected_profile['name']}")
            self.print_current_parameters()
            
        except FileNotFoundError:
            print("profiles.txt file not found.")
        except json.JSONDecodeError:
            print("Error decoding JSON from the file. Make sure the file is properly formatted.")

    def print_current_parameters(self):
        print("Current Parameters:")
        print(f"Initial Delay of SDG2000x: {self.max_delay_SDG}")
        print(f"Minimum Delay of SDG2000x: {self.min_delay}")
        print(f"Number of Photos Per Cycle: {self.num_photos_per_cycle}")
        print(f"Delay Increment: {self.delay_increment}")
        print()

    def run(self):
        self.error_msg = "Error: Please Try Again"

        print("Welcome to the laser delay-line control program!")
        print("Please follow the directions below.")
        print()

        while True:
            print('-'*50, "MAIN MENU", '-'*50)
            print("(1) SET PARAMETERS")
            print("(2) BEGIN DATA COLLECTION")
            print("(3) SAVE PROFILE")
            print("(4) LOAD PROFILE")
            print("(5) PRINT CURRENT PARAMETERS")
            print("(6) EXIT")

            token = self.get_int_input("Enter Token:")
            
            if token == 1:
                self.set_parameters()
            elif token == 2:
                self.begin_data_collection()
            elif token == 3:
                self.save_profile()
            elif token == 4:
                self.load_profile()
            elif token == 5:
                self.print_current_parameters()
            elif token == 6:
                print("Exiting program")
                break
            else:
                print("Invalid token. Please try again.")

begin_script = LaserDelayControl()
begin_script.run()
