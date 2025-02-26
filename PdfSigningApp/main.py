import time
from usbmonitor import USBMonitor
from usbmonitor.attributes import ID_MODEL, ID_MODEL_ID, ID_VENDOR_ID

# Formatowanie informacji o urządzeniu
def device_info_str(device_info):
    return f"{device_info.get(ID_MODEL, 'Unknown')} ({device_info.get(ID_MODEL_ID, 'Unknown')} - {device_info.get(ID_VENDOR_ID, 'Unknown')})"

# Callbacki do obsługi podłączania i odłączania urządzeń USB
def on_connect(device_id, device_info):
    print(f"Connected: {device_info_str(device_info)}")

def on_disconnect(device_id, device_info):
    print(f"Disconnected: {device_info_str(device_info)}")

# Tworzenie instancji monitora USB
monitor = USBMonitor()

# Uruchomienie nasłuchiwania
def main():
    monitor.start_monitoring(on_connect=on_connect, on_disconnect=on_disconnect)
    try:
        while True:
            time.sleep(1)  # Zapobiega nadmiernemu obciążeniu procesora
    except KeyboardInterrupt:
        print("Stopping USB monitoring...")
        monitor.stop_monitoring()

if __name__ == "__main__":
    main()

