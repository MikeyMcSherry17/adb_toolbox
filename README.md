# 📱 ADB Toolbox

**ADB Toolbox** is a Python-based testing framework designed to run **bulk ADB commands across multiple Android devices**.  
It borrows ideas from the *BulkTransaction Tool* (structured test packs, central logging, GUI control) and adapts them for ADB workflows.  

---

## 🚀 Purpose
- Provide **repeatable test packs** for Android devices.  
- Run **diagnostic, health, and app tests** on one or many connected devices.  
- Collect structured results (JSON/CSV) for troubleshooting, demo, or regression testing.  

---

## ✨ Key Features
- **Device discovery**: Automatically detects connected devices via `adb devices -l`.  
- **Batch definitions**: Tests are stored in JSON files (easy to share, edit, and extend).  
- **Structured logging**: All runs are logged in JSONL format for analysis.  
- **Result export**: Save outputs per device with timestamped filenames.  
- **GUI control** *(planned)*: Start/stop tests, view logs, and monitor device status in real time.  

---

## 📂 Project Structure
adb_toolbox-main/
│
├── ProgramFiles/ # Core modules (logging, global state, GUI, command runner)
├── batches/ # JSON batch definitions (test packs)
│ └── device_health.json
├── results/ # Test outputs per device
│ └── device_health_123456_2025-09-24.json
├── adb_runner.py # Runs individual ADB commands
├── toolbox.py # Main entry point
└── README.md # This file

pgsql
Copy code

---

## 🧪 Example Test Pack (JSON)
Example `batches/device_health.json`:

```json
{
  "batchName": "Device Health Check",
  "description": "Collects identity, battery, storage, and logs from each connected device.",
  "commands": [
    {
      "name": "Get Android Version",
      "adb_cmd": ["shell", "getprop", "ro.build.version.release"],
      "timeout": 5,
      "parse": "string"
    },
    {
      "name": "Battery Status",
      "adb_cmd": ["shell", "dumpsys", "battery"],
      "timeout": 10,
      "parse": "battery"
    },
    {
      "name": "Storage Check",
      "adb_cmd": ["shell", "df", "/data"],
      "timeout": 10,
      "parse": "storage"
    }
  ],
  "export": {
    "format": "json",
    "filename": "results/device_health_{deviceId}_{timestamp}.json"
  }
}
