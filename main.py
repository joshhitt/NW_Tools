#!/usr/local/bin/python3.9
# Network Tools
# Some text files will be needed in the scripts sub folder, this is designed to be symlinked into a users home
# folder ~/scripts/  Five device lists were needed in our deployment but can be altered easily.  
# the device text file only needs to be readable by the script and can also be symlinked into the users ~/scripts location
# if the hosts_file.py is used to create and edit the custom_devices.txt, it will need to be writable by the user.

# import modules needed

import datetime
import socket
import time
import paramiko
import os
import getpass
# import io

# print("\n   ***Device Credentials Needed***\n")  # Commented out credentials, admin user needs to be elevated to 15
user = input("Enter Username: ")
from getpass import getpass
secret = getpass( 'Enter Password: ' )
port = 22
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# define variables
time_now = datetime.datetime.now().strftime('%H:%M:%S %m/%d/%Y')
infilepath = os.path.expanduser('~/scripts/')  # UNIX Pathing
# infilepath = os.path.expanduser('~\\scripts\\')  # Windows Pathing
print("Using: ", infilepath)
# outfilepath = os.path.expanduser('~/')  # Used if writing output to a file

# Set initial device list and present menu

devicelist = "all_devices.txt\n"  # Set devicelist default

device_prompt = ("\n    1. All Devices\n"  # All Network Devices
                 "    2. Main Campus Devices\n"  # Main Network Devices
                 "    3. North Campus Devices\n"  # North Network Devices
                 "    4. Core Devices\n"  # Core Switches at both campuses
                 "    5. Custom Device List\n"  # Custom Device List created with host_file.py
                 "    Q. Exit to Command Shell\n\n"
                 "    >>>  ")
while True:
    device = input(device_prompt).lower().strip()
    if device == '1':
        devicelist = "all_devices.txt"
        print(" Selected:", devicelist)
    elif device == '2':
        devicelist = "main_devices.txt"
        print(" Selected:", devicelist)
    elif device == '3':
        devicelist = "north_devices.txt"
        print(" Selected:", devicelist)
    elif device == '4':
        devicelist = "core_devices.txt"
        print(" Selected:", devicelist)
    elif device == '5':
        devicelist = "custom_devices.txt"
        print(" Selected:", devicelist)
    elif device == 'q':
        break  # Exit to shell
    else:
        print('    ***Unrecognized Entry***')

    # Use the device list and present tools menu

    input_file = open(infilepath + devicelist, "r")
    iplist = input_file.readlines()
    input_file.close()
    menu_prompt = ("\n    1. Device Uptime\n"  # Check Uptime
                   "    2. Check Versions\n"  # Check Versions
                   "    3. Find Variable\n"  # Find matching string
                   "    4. Find MAC Address\n"  # Parse CAM Tables for MAC
                   "    5. Inventory Search\n"  # Parse Inventory for Serial Match
                   "    6. ARP Search *Sets Device List to Core Devices*\n"  # Parse ARP Cache for Match
                   "    B. Back to Device List Selection\n\n"
                   "    >>>  ")

    while True:  # keep asking for input until break
        command = input(menu_prompt).lower().strip()
        if command == '1':
            print("\n    Uptime Checks Running Using: ", devicelist, "\n")
            print("_" * 108, "\n")
            try:
                for ip in iplist:
                    try:
                        ipaddr = ip.strip()
                        ssh.connect(hostname=ipaddr, username=user, password=secret, port=port)
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("show version")
                        response = ssh_stdout.readlines()
                        err_response = ssh_stderr.readlines()
                        find_string = "uptime"
                        for line in response:
                            if find_string in line:
                                print(f" Trying: {ipaddr:<20} {line:>80}")
                        ssh.close()
                        ssh_stdin.close()
                    except paramiko.AuthenticationException:
                        print(f" Authentication Failed: {ipaddr}\n")
                        pass
                    except socket.gaierror:
                        print(f" Hostname Not Found: {ipaddr}\n") 
                        pass
                    except Exception as ex:
                        print(f" {ipaddr} <<< Failed to Respond >>> ", ex, "\n")
                        pass
                    finally:
                        pass
            finally:
                print("_" * 108, "\n")
                print("    Script completed", time_now, "\n")

        elif command == '2':
            print("    Opening: ", devicelist, "\n")
            try:
                for ip in iplist:
                    try:
                        ipaddr = ip.strip()
                        ssh.connect(hostname=ipaddr, username=user, password=secret, port=port)
                        print("_" * 108)
                        print("\n    ", ipaddr, " Running  Software Versions\n")
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('show version')
                        response = ssh_stdout.readlines()
                        err_response = ssh_stderr.readlines()
                        find_string = 'ersion'
                        for line in response:
                            if find_string in line:
                                print(f"  {line}")
                        time.sleep(1)
                        ssh.close()
                        ssh_stdin.close()
                    except paramiko.AuthenticationException:
                        print(f" Authentication Failed: {ipaddr}\n")
                        pass
                    except socket.gaierror:
                        print(f" Hostname Not Found: {ipaddr}\n") 
                        pass
                    except Exception as ex:
                        print(f" {ipaddr} <<< Failed to Respond >>> ", ex, "\n")
                        pass
                    finally:
                        pass
            finally:
                print("\n\n    Script completed", time_now, "\n\n")

        elif command == '3':
            print("    Opening: ", devicelist, "\n")
            find_string = input('    Enter the string to match: ').strip()
            try:
                for ip in iplist:
                    try:
                        ipaddr = ip.strip()
                        ssh.connect(hostname=ipaddr, username=user, password=secret, port=port)
                        print("_" * 100)
                        print(f"\n Checking: {ipaddr} for \'{find_string}\'\n")
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('show run')
                        response = ssh_stdout.readlines()
                        err_response = ssh_stderr.readlines()
                        for index, line in enumerate(response):
                            if find_string in line:
                                print("".join(response[max(0, index - 1):index + 2]))
                                # print(f"".join(response[max(0, index - 1):index + 2]))
                        ssh.close()
                        ssh_stdin.close()
                    except paramiko.AuthenticationException:
                        print(f" Authentication Failed: {ipaddr}\n")
                        pass
                    except socket.gaierror:
                        print(f" Hostname Not Found: {ipaddr}\n") 
                        pass
                    except Exception as ex:
                        print(f" {ipaddr} <<< Failed to Respond >>> ", ex, "\n")
                        pass
                    finally:
                        pass
            finally:
                print("\n\n    Script completed", time_now, "\n\n")

        elif command == '4':
            print(" Opening: ", devicelist, "\n")
            find_string = input('    Enter Last 4 of MAC address: ').strip()
            try:
                for ip in iplist:

                    try:
                        ipaddr = ip.strip()
                        ssh.connect(hostname=ipaddr, username=user, password=secret, port=port)
                        print("_" * 100)
                        print(f"\n Checking: {ipaddr} for \'{find_string}\'\n")
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('show mac address-table')
                        response = ssh_stdout.readlines()
                        err_response = ssh_stderr.readlines()
                        for line in response:
                            if find_string in line:
                                print(f" {line}\n")
                        ssh.close()
                        ssh_stdin.close()
                    except paramiko.AuthenticationException:
                        print(f" Authentication Failed: {ipaddr}\n")
                        pass
                    except socket.gaierror:
                        print(f" Hostname Not Found: {ipaddr}\n") 
                        pass
                    except Exception as ex:
                        print(f" {ipaddr} <<< Failed to Respond >>> ", ex, "\n")
                        pass
                    finally:
                        pass
            finally:
                print("\n\n    Script completed", time_now, "\n\n")

        elif command == '5':
            print("    Opening: ", devicelist, "\n")
            find_string = input('    Enter a Serial Number: ').upper().strip()
            try:
                for ip in iplist:
                    try:
                        ipaddr = ip.strip()
                        ssh.connect(hostname=ipaddr, username=user, password=secret, port=port)
                        print("_" * 100)
                        print(f"\n Checking: {ipaddr} for \'{find_string}\'\n")
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('show inventory')
                        response = ssh_stdout.readlines()
                        err_response = ssh_stderr.readlines()
                        for index, line in enumerate(response):
                            if find_string in line:
                                print("".join(response[max(0, index - 1):index + 1]))
                        ssh.close()
                        ssh_stdin.close()
                    except paramiko.AuthenticationException:
                        print(f" Authentication Failed: {ipaddr}\n")
                        pass
                    except socket.gaierror:
                        print(f" Hostname Not Found: {ipaddr}\n")
                        pass
                    except Exception as ex:
                        print(f" {ipaddr} <<< Failed to Respond >>> ", ex, "\n")
                        pass
                    finally:
                        pass
            finally:
                print("\n\n    Script completed", time_now, "\n\n")

        elif command == '6':
            devicelist = "core_devices.txt"
            input_file = open(infilepath + devicelist, "r")
            iplist = input_file.readlines()
            input_file.close()

            # loop through switches
            print("    Opening: ", devicelist, "\n")
            find_string = input('    Enter Last 4 of MAC or IP address: ').lower().strip()
            try:
                for ip in iplist:

                    try:
                        ipaddr = ip.strip()
                        ssh.connect(hostname=ipaddr, username=user, password=secret, port=port)
                        print("_" * 100)
                        print("\n Checking: ", ipaddr, " For IP Address or MAC Ending with: ", find_string, "\n")
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('show ip arp')
                        response = ssh_stdout.readlines()
                        err_response = ssh_stderr.readlines()
                        for line in response:
                            if find_string in line:
                                print(f"    {line}")
                        ssh.close()
                        ssh_stdin.close()
                    except paramiko.AuthenticationException:
                        print(f" Authentication Failed: {ipaddr}\n")
                        pass
                    except socket.gaierror:
                        print(f" Hostname Not Found: {ipaddr}\n")
                        pass
                    except Exception as ex:
                        print(f" {ipaddr} <<< Failed to Respond >>> ", ex, "\n")
                        pass
                    finally:
                        pass
            finally:
                print("\n\n    Script completed", time_now, "\n\n")
                break  # Break back to Devices Selection due to hard set devicelist
        elif command == 'b':
            break  # Back to Devices Selection
        else:
            print('\n    ***Unrecognized Entry***')

print('\n\n    Type menu.sh to relaunch\n\n    Type hosts.sh to edit your custom devices list\n\n')
