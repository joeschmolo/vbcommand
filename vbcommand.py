#!/usr/bin/env python3
#
# Author: Joe Schultz <jxscad@rit.edu>
# Date: 04/20/2025
#
# Description: Menu-driven program to control VirtualBox
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import subprocess

# List VMs based on provided selection
def list_virtual_machines(get_selection="all", numbered=False):
    # Only allow certain selections
    get_selection = get_selection.lower()
    if get_selection not in ("all", "running", "stopped"):
        print(f"Error (program): invalid selection '{get_selection}'. Use 'all', 'running', or 'stopped'.")
        return

    # Grab all VMs
    vm_list = subprocess.check_output(["VBoxManage","list","vms"], text=True).splitlines()
    all_vms = { line.split()[0].strip('"') for line in vm_list if line.strip() }

    # Grab all running VMs
    running_vm_list = subprocess.check_output(["VBoxManage","list","runningvms"], text=True).splitlines()
    running_vms = { line.split()[0].strip('"') for line in running_vm_list if line.strip() }

    # Decide which VMs to show
    if get_selection == "all":
        vm_selection = all_vms
    elif get_selection == "running":
        vm_selection = running_vms
    else:
        # stopped
        vm_selection = all_vms - running_vms

    # Sort into a list for both numbered & un‑numbered output
    sorted_vms = sorted(vm_selection)

    print("Virtual Machines:\n")
    if numbered:
        for i, vm in enumerate(vm_selection, start=1):
            status = "running" if vm in running_vms else "stopped"
            print(f"\t{i}. {vm}")
        print()
        return sorted_vms
    else:
        for vm in vm_selection:
            status = "running" if vm in running_vms else "stopped"
            print(f"\t[{status}] {vm}")
        print()
        return None

# List all VMs
def list_all_vms():
    print("Listing all virtual machines...\n")
    list_virtual_machines("all")

# Start a VM
def start_vm():
    # Show only stopped VMs
    print("Select a stopped VM to start:\n")
    stopped = list_virtual_machines("stopped", numbered=True)
    if not stopped:
        print("No stopped VMs available.\n")
        return

    choice = input("Enter the number of the VM to power on: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(stopped)):
        print("Error: invalid selection.\n")
        return

    vm_name = stopped[int(choice) - 1]
    print(f"Starting '{vm_name}'...\n")
    try:
        subprocess.run(["VBoxManage", "startvm", vm_name], check=True)
        print(f"'{vm_name}' started.\n")
    except subprocess.CalledProcessError:
        print(f"Failed to start '{vm_name}'.\n")

# Stop a VM
def stop_vm():
    # Show only running VMs
    print("Select a running VM to stop:\n")
    running = list_virtual_machines("running", numbered=True)
    if not running:
        print("No running VMs available.\n")
        return

    choice = input("Enter the number of the VM to stop: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(running)):
        print("Error: invalid selection.\n")
        return

    vm_name = running[int(choice) - 1]
    print(f"Stopping '{vm_name}'...\n")
    try:
        subprocess.run(
            ["VBoxManage", "controlvm", vm_name, "acpipowerbutton"],
            check=True
        )
        print(f"'{vm_name}' stopped.\n")
    except subprocess.CalledProcessError:
        print(f"Failed to stop '{vm_name}'.\n")
    

# Exit this program
def exit_program():
    print("Exiting... Goodbye!")
    raise SystemExit

# Prompt the main menu
def main_menu():
    options = {
        '0': ("Exit program", exit_program),
        '1': ("List VMs", list_all_vms),
        '2': ("Start a VM", start_vm),
        '3': ("Stop a VM", stop_vm),
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
    print("\nWelcome to the Virtual Box Command tool!\n")
    main_menu()

if __name__ == "__main__":
    main()