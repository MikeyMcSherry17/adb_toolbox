# Author - M McSherry
# Revision - 14
# Build Date - 05/03/2025

import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Run ADB command

def run_command(command, output_file=None):
    process = subprocess.run(["adb"] + command.split(), capture_output=True, text=True)
    
    if output_file:
        # Get absolute path to the output directory relative to the script location
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_output_path = os.path.join(base_dir, output_file)
        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)

        with open(full_output_path, "w", encoding="utf-8") as f:
            f.write(process.stdout)
    
    output.insert(tk.END, process.stdout + "\n")
    output.see(tk.END)

# Install APK
def install_apk():
    apk_file = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")])
    if apk_file:
        run_command(f"install \"{apk_file}\"")
        messagebox.showinfo("Success", f"APK installed: {apk_file}")

# Screenshot & Screen Recording
def capture_screenshot():
    path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")], initialfile="screenshot.png")
    if path:
        run_command(f"shell screencap -p /sdcard/screenshot.png && pull /sdcard/screenshot.png \"{path}\"")

def toggle_screen_recording(start=True):
    global recording_process
    if start:
        recording_process = subprocess.Popen(["adb", "shell", "screenrecord", "/sdcard/screenrecord.mp4"])
        output.insert(tk.END, "Recording started...\n")
    elif recording_process:
        recording_process.terminate()
        path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")], initialfile="screenrecord.mp4")
        if path:
            run_command(f"pull /sdcard/screenrecord.mp4 \"{path}\" && shell rm /sdcard/screenrecord.mp4")
        output.insert(tk.END, "Recording stopped.\n")

# Export Output to Text File
def export_output():
    text = output.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "No output to export!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], initialfile="adb_output.txt")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        messagebox.showinfo("Success", f"Output saved to:\n{file_path}")

# UI Setup
window = tk.Tk()
window.title("ADB Toolbox")

# Left Frame (Buttons)
left_frame = tk.Frame(window, padx=10, pady=10)
left_frame.grid(row=0, column=0, sticky="n")

# Right Frame (Output)
right_frame = tk.Frame(window, padx=10, pady=10)
right_frame.grid(row=0, column=1, sticky="n")

# **Device Actions**
device_actions = [
    ("Install APK", install_apk, "Select and install an APK file on the device."),
    ("Reboot Device", lambda: run_command("reboot"), "Restart the connected Android device."),
    ("Capture Screenshot", capture_screenshot, "Take a screenshot and save it to your computer."),
    ("Start Recording", lambda: toggle_screen_recording(True), "Start recording the device screen."),
    ("Stop Recording", lambda: toggle_screen_recording(False), "Stop screen recording and save the file.")
]

# **System Information**
system_info = [
    ("Getprop", lambda: run_command("shell getprop", "output/getprop.txt"), "Retrieve system properties and configurations."),
    ("Dumpsys Wifi", lambda: run_command("shell dumpsys wifi", "output/dumpsys_wifi.txt"), "Get detailed WiFi status and network information."),
    ("Dumpsys Battery", lambda: run_command("shell dumpsys battery", "output/dumpsys_battery.txt"), "Display battery health and charge details."),
    ("Dumpsys Window", lambda: run_command("shell dumpsys window", "output/dumpsys_window.txt"), "Get information about the window manager."),
    ("Dumpsys Activity", lambda: run_command("shell dumpsys activity", "output/dumpsys_activity.txt"), "Show the activity manager state."),
    ("Dumpsys Package", lambda: run_command("shell dumpsys package", "output/dumpsys_package.txt"), "List installed packages and their details."),
    ("Dumpsys CPU Info", lambda: run_command("shell dumpsys cpuinfo", "output/dumpsys_cpuinfo.txt"), "Show CPU usage and performance statistics.")
]

# **Categories & Buttons**
categories = [("Device Actions", device_actions), ("System Information", system_info)]

for category, buttons in categories:
    tk.Label(left_frame, text=category, font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 2))
    for text, cmd, desc in buttons:
        frame = tk.Frame(left_frame)
        frame.pack(fill="x", pady=2)
        tk.Button(frame, text=text, command=cmd, width=20).pack(side="left")
        tk.Label(frame, text=desc, anchor="w", justify="left").pack(side="left", padx=5)

# **Output Console**
tk.Label(right_frame, text="ADB Output", font=("Arial", 12, "bold")).pack()
output = tk.Text(right_frame, height=30, width=80)
output.pack(pady=5)

# **Output Buttons**
output_button_frame = tk.Frame(right_frame)
output_button_frame.pack(pady=5)

tk.Button(output_button_frame, text="Clear Output", command=lambda: output.delete(1.0, tk.END)).pack(side="left", padx=5)
tk.Button(output_button_frame, text="Export to Text File", command=export_output).pack(side="left", padx=5)

# **Footer (Author Info)**
footer_frame = tk.Frame(window)
footer_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="se")

tk.Label(footer_frame, text="Author: M McSherry | Revision: 14 | Build Date: 05/03/2025", font=("Arial", 9)).pack()

# Run GUI
window.mainloop()
