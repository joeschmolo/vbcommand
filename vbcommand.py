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
            ["VBoxManage", "controlvm", vm_name, "savestate"],
            check=True
        )
        print(f"'{vm_name}' stopped.\n")
    except subprocess.CalledProcessError:
        print(f"Failed to stop '{vm_name}'.\n")

# Create a VM
def create_vm():
    # Set VM name
    vm_name = input("Enter a name for the new VM: ").strip()
    if not vm_name:
        print("Error: VM name cannot be empty.\n")
        return

    # Set memory size
    mem = input("Enter RAM size in MB (e.g. 2048): ").strip()
    if not mem.isdigit() or int(mem) < 4:
        print("Error: Invalid memory size.\n")
        return

    # Set disk size
    disk_size = input("Enter disk size in MB (e.g. 20000): ").strip()
    if not disk_size.isdigit() or int(disk_size) < 1:
        print("Error: Invalid disk size.\n")
        return

    # Choose network
    net_mode = input("Network type? [1] NAT  [2] Bridged  (default 1): ").strip()
    if net_mode == "2":
        # for bridged you need to pick a host interface, e.g. en0 or eth0
        host_if = input(" Host interface to bridge (e.g. eth0): ").strip()
        nic_args = ["--nic1", "bridged", "--bridgeadapter1", host_if]
    else:
        nic_args = ["--nic1", "nat"]

    print(f"\nCreating VM '{vm_name}' with {mem}MB RAM, {disk_size}MB disk, network={nic_args[1]}...\n")
    try:
        # create
        subprocess.run(["VBoxManage", "createvm", "--name", vm_name, "--register"], check=True)
        subprocess.run([
            "VBoxManage", "modifyvm", vm_name,
            "--memory", mem,
            "--vram", "16",
            *nic_args
        ], check=True)

        # create virtual disk
        disk_file = f"{vm_name}.vdi"
        subprocess.run([
            "VBoxManage", "createmedium", "disk",
            "--filename", disk_file,
            "--size", disk_size
        ], check=True)

        # add SATA controller
        subprocess.run([
            "VBoxManage", "storagectl", vm_name,
            "--name", "SATA Controller",
            "--add", "sata",
            "--controller", "IntelAhci"
        ], check=True)
        subprocess.run([
            "VBoxManage", "storageattach", vm_name,
            "--storagectl", "SATA Controller",
            "--port", "0", "--device", "0",
            "--type", "hdd",
            "--medium", disk_file
        ], check=True)

        print(f"VM '{vm_name}' created successfully!\n")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred creating '{vm_name}':\n  {e}\n")



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
        '3': ("Stop a VM (save current state)", stop_vm),
        '4': ("Create a VM", create_vm),
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