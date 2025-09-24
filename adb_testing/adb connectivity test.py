import tkinter as tk
from tkinter import scrolledtext
import subprocess
import re
from datetime import datetime
import time
import threading

def get_gprs_signal():
    # Retrieve the interval and repeat values from the entry fields
    try:
        interval = int(interval_entry.get())
        repeat = int(repeat_entry.get())
    except ValueError:
        output_text.insert(tk.END, "Please enter valid numbers for interval and repeat values.\n")
        return

    def run_tests():
        for i in range(repeat):
            # Run the adb shell command to get GPRS information
            command = "adb shell dumpsys telephony.registry"
            result = subprocess.run(command, capture_output=True, text=True, shell=True)

            # Check if the command was successful
            if result.returncode != 0:
                output_text.insert(tk.END, "Failed to execute adb command. Ensure that adb is installed and the device is connected.\n")
                return

            # Extract signal strength values and relevant information
            output = result.stdout
            signal_strength_info = re.findall(r'SignalStrength: (\d+)', output)
            network_type_info = re.findall(r'NetworkType: (\d+)', output)
            data_state_info = re.findall(r'DataState: (\d+)', output)

            # Get the current timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Display the extracted information with a timestamp and aligned output
            if not signal_strength_info:
                output_text.insert(tk.END, f"[{timestamp}] No signal strength information found.\n")
            else:
                header = f"[{timestamp}] {'Signal Strength':<20} {'Network Type':<20} {'Data State':<20}\n"
                output_text.insert(tk.END, header)
                output_text.insert(tk.END, '-' * len(header) + '\n')
                for j, signal_strength in enumerate(signal_strength_info):
                    network_type = network_type_info[j] if j < len(network_type_info) else "N/A"
                    data_state = data_state_info[j] if j < len(data_state_info) else "N/A"
                    line = f"{signal_strength:<20} {network_type:<20} {data_state:<20}\n"
                    output_text.insert(tk.END, line)

            output_text.see(tk.END)  # Auto-scroll to the latest entry
            time.sleep(interval)

    # Run the tests in a separate thread to avoid blocking the GUI
    threading.Thread(target=run_tests).start()

def get_wifi_rssi():
    # Retrieve the interval and repeat values from the entry fields
    try:
        interval = int(interval_entry.get())
        repeat = int(repeat_entry.get())
    except ValueError:
        output_text.insert(tk.END, "Please enter valid numbers for interval and repeat values.\n")
        return

    def run_tests():
        for i in range(repeat):
            # Run the adb shell command to get Wi-Fi information
            command = "adb shell dumpsys wifi"
            result = subprocess.run(command, capture_output=True, text=True, shell=True)

            # Check if the command was successful
            if result.returncode != 0:
                output_text.insert(tk.END, "Failed to execute adb command. Ensure that adb is installed and the device is connected.\n")
                return

            # Extract RSSI values and relevant information
            output = result.stdout
            rssi_info = re.findall(r'RSSI: (-\d+)', output)
            ssid_info = re.findall(r'SSID: (\S+)', output)
            bssid_info = re.findall(r'BSSID: (\S+)', output)
            frequency_info = re.findall(r'Frequency: (\d+)', output)
            link_speed_info = re.findall(r'Link speed: (\d+)', output)

            # Get the current timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Display the extracted information with a timestamp and aligned output
            if not rssi_info:
                output_text.insert(tk.END, f"[{timestamp}] No RSSI information found.\n")
            else:
                header = f"[{timestamp}] {'SSID':<20} {'BSSID':<20} {'Frequency':<10} {'RSSI':<10} {'Link Speed':<10}\n"
                output_text.insert(tk.END, header)
                output_text.insert(tk.END, '-' * len(header) + '\n')
                for j, rssi in enumerate(rssi_info):
                    ssid = ssid_info[j] if j < len(ssid_info) else "N/A"
                    bssid = bssid_info[j] if j < len(bssid_info) else "N/A"
                    frequency = frequency_info[j] if j < len(frequency_info) else "N/A"
                    link_speed = link_speed_info[j] if j < len(link_speed_info) else "N/A"
                    line = f"{ssid:<20} {bssid:<20} {frequency:<10} {rssi:<10} {link_speed:<10}\n"
                    output_text.insert(tk.END, line)

            output_text.see(tk.END)  # Auto-scroll to the latest entry
            time.sleep(interval)

    # Run the tests in a separate thread to avoid blocking the GUI
    threading.Thread(target=run_tests).start()

# Set up the tkinter GUI
root = tk.Tk()
root.title("ADB Connectivity Test")

# Interval and Repeat input fields
tk.Label(root, text="Interval (seconds):").grid(row=0, column=0, padx=5, pady=5)
interval_entry = tk.Entry(root)
interval_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Repeat:").grid(row=1, column=0, padx=5, pady=5)
repeat_entry = tk.Entry(root)
repeat_entry.grid(row=1, column=1, padx=5, pady=5)

# Output text area
output_text = scrolledtext.ScrolledText(root, width=100, height=30)
output_text.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

# Buttons to start the tests
gprs_button = tk.Button(root, text="Get GPRS Signal", command=get_gprs_signal)
gprs_button.grid(row=3, column=0, padx=5, pady=5)

wifi_button = tk.Button(root, text="Get WiFi RSSI", command=get_wifi_rssi)
wifi_button.grid(row=3, column=1, padx=5, pady=5)

# Run the tkinter event loop
root.mainloop()
