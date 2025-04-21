#!/usr/bin/env python3
#
# Author: Joe Schultz <jxscad@rit.edu>
# Date: 04/20/2025
#
# Description: Menu-driven program to control VirtualBox
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import subprocess

# List VMs
def list_virtual_machines():
    # Grab all VMs
    vm_list = subprocess.check_output(
        ["VBoxManage", "list", "vms"],
        text=True
    ).splitlines()
    all_vms = {
        line.split()[0].strip('"')
        for line in vm_list
        if line.strip()
    }

    # Grab only running VMs
    running_vm_list = subprocess.check_output(
        ["VBoxManage", "list", "runningvms"],
        text=True
    ).splitlines()
    running_vms = {
        line.split()[0].strip('"')
        for line in running_vm_list
        if line.strip()
    }

    print("Virtual Machines:\n")
    for vm in sorted(all_vms):
        status = "running" if vm in running_vms else "stopped"
        print(f"[{status}] {vm}")
    print()

# Exit this program
def exit_program():
    print("Exiting... Goodbye!")
    # either raise SystemExit or just return a flag
    raise SystemExit

# Prompt the main menu
def main_menu():
    options = {
        '0': ("Exit program", exit_program),
        '1': ("List VMs", list_virtual_machines),

    }
    # Display the menu
    while True:
        print("################################\n\nMenu:")
        for index in sorted(options):
            print(f"\t{index}. {options[index][0]}")
        print("")
        selection = input("Menu Selection: ").strip()
        command = options.get(selection)
        if command:
            # Run the selected option
            command[1]()
        else:
            # Output error if text entered is not one of the options
            print("Error: Option unknown. Please select from the menu.\n")


# Main program
def main():
    main_menu()

if __name__ == "__main__":
    main()