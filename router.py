import subprocess
import sys
import time
import select

from simulation import read_hardware_state, write_hardware_state, calculate_f, mutate_hardware, mutate_database, create_hardware_file, file_path

def print_cli_history(history):
    for entry in history:
        print(entry)

def process_cli_input(file_path, history, t):
    # Process CLI input here
    try:
        print("Enter CLI command: ")
        user_input = select.select([sys.stdin], [], [], 1)[0]
        if user_input:
            user_input = sys.stdin.readline().strip()
        else:
            return
        command, *args = user_input.split()
        if command == "set":
            index = int(args[0]) - 1
            value = int(args[1])
            if index < 0 or index >3 :
                print(f"Invalid Input - Error: {index}")
            else:
                mutate_database(file_path, index, value)
                history.append(f"{t} set {index} {value}")
    except Exception as e:
        print(f"Invalid Input - Error: {str(e)}")
    time.sleep(1)

#Use case 2: Handling Control Traffic
def switch_control(signal_values):
    # check for signal values and valid index
    if signal_values and (signal_values[0] - 1) >= 0 and (signal_values[0] - 1) <= 3:
        # get index and value from signal
        index = signal_values[0] - 1
        value = signal_values[1]
        # make change to hardware
        mutate_hardware(file_path, index, value)
    return signal_values

#Use case 4: Handling Cron Jobs
def handle_inactivity(t, history, state_values):
    # check time requirement
    if t % 10 == 0:
        # add swap to history
        history.append(f"{t} swap {state_values[0]} {state_values[1]}")
        # swap values
        state_values[0], state_values[1] = state_values[1], state_values[0]
        # swap in database
        mutate_database(file_path, 0, state_values[0])
        mutate_database(file_path, 1, state_values[1])
        
    return state_values

def main():
    history = []
    t = 0


    while t < 20:
        state_values, control_values, signal_values = read_hardware_state(file_path)
        t += 1

        # Write Your Code Here Start

        # handle control traffic (case 2)
        signal_values = switch_control(signal_values)

        # handle management functionality (case 3)
        # process_cli_input(file_path, history, t)

        # handle cron job (case 4)
        state_values = handle_inactivity(t, history, state_values)

        # Write Your Code Here End
        time.sleep(1)  # Wait for 1 second before polling again
    # recovery and documentation (case 5)
    print(history)

if __name__ == '__main__':
    main()




