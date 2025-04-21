#!/usr/bin/env python3
#
# Author: Joe Schultz <jxscad@rit.edu>
# Date: 04/20/2025
#
# Description: Menu-driven program to control VirtualBox
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import subprocess

# List VMs based on provided selection
def list_virtual_machines(get_selection="all"):
    # Only allow certain selections
    get_selection = get_selection.lower()
    if get_selection not in ("all", "running", "stopped"):
        print(f"Error (program): invalid selection '{get_selection}'. Use 'all', 'running', or 'stopped'.")
        return

    # Grab all VMs
    vm_list = subprocess.check_output(
        ["VBoxManage", "list", "vms"],
        text=True
    ).splitlines()
    all_vms = { line.split()[0].strip('"') for line in vm_list if line.strip() }

    # Grab all running VMs
    running_vm_list = subprocess.check_output(
        ["VBoxManage", "list", "runningvms"],
        text=True
    ).splitlines()
    running_vms = { line.split()[0].strip('"') for line in run_list if line.strip() }

    # Decide which VMs to show
    if get_selection == "all":
        vm_selection = all_vms
    elif get_selection == "running":
        vm_selection = running_vms
    else:
        # stopped
        vm_selection = all_vms - running_vms

    # Print selection
    print("Virtual Machines:\n")
    for vm in sorted(vm_selection):
        status = "running" if vm in running_vms else "stopped"
        print(f"[{status}] {vm}")
    print()

# List all VMs
def list_all_vms():
    list_virtual_machines("all")

# Exit this program
def exit_program():
    print("Exiting... Goodbye!")
    raise SystemExit

# Prompt the main menu
def main_menu():
    options = {
        '0': ("Exit program", exit_program),
        '1': ("List VMs", list_all_vms),

    }
    # Display the menu
    while True:
        print(">>> Menu:")
        for index in sorted(options):
            print(f"\t{index}. {options[index][0]}")
        print("")
        selection = input("(prompt) Menu Selection: ").strip()
        command = options.get(selection)
        if command:
            # Run the selected option
            command[1]()
        else:
            # Output error if text entered is not one of the options
            print("Error: Option unknown. Please select from the menu.\n")


# Main program
def main():
    print("################################")
    print("### VBCommand by Joe Schultz ###")
    print("################################")
    main_menu()

if __name__ == "__main__":
    main()