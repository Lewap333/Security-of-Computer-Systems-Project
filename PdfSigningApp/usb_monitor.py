##
# @file usb_monitor.py
# @brief Module responsible for monitoring USB drive plug/unplug events on Windows.
#
# Detects private key files on USB drives and updates the application interface accordingly.

import os
import win32api
import win32file
import win32con
import win32gui
import threading

# Extensions that may contain private keys
PRIVATE_KEY_EXTENSIONS = ".pem"

# Windows USB Events
# https://learn.microsoft.com/en-us/windows/win32/devio/wm-devicechange
WM_DEVICECHANGE = 0x0219
DBT_DEVICEARRIVAL = 0x8000
DBT_DEVICEREMOVECOMPLETE = 0x8004

##
# @brief Returns a list of currently connected removable USB drives.
# @return List of removable drive letters (e.g., ['E:\\', 'F:\\']).
def get_removable_drives():
    """Returns list of currently attached USB drives."""
    drives = [i for i in win32api.GetLogicalDriveStrings().split('\\\x00') if i]
    return [d for d in drives if win32file.GetDriveType(d) == win32con.DRIVE_REMOVABLE]

##
# @brief Searches for a private key file on the given drive.
# @param drive The root path of the USB drive to search.
# @return Full path to the found key file or None if not found.
def find_key_file(drive):
    """Searches for path to the private key on a drive."""
    for root, _, files in os.walk(drive):
        for file in files:
            if file.lower().endswith(PRIVATE_KEY_EXTENSIONS):
                return os.path.join(root, file)
    return None

##
# @class USBMonitor
# @brief Class responsible for detecting USB plug/unplug events on Windows.
#
# Uses a hidden window to listen for system device change notifications.
# Can identify USB drives containing private keys and notify the GUI.
class USBMonitor:
    """Class to watch for USB events (plug/unplug)."""
    
    ##
    # @brief Initializes the USBMonitor.
    # @param update_ui Callback function to update UI on key detection.
    def __init__(self, update_ui):
        # Handle for hidden window - detection USB plug/unplug
        self.hwnd = None

        # Store initially connected drives.
        self.current_drives = get_removable_drives()

        self.key_file_path = None
        self.key_file_drive = None

        # Callback to update the UI
        self.update_ui = update_ui

    ##
    # @brief Starts monitoring USB events in a background thread.
    def start_monitoring(self):
        """Monitoring USB plug/unplug events in a separate thread."""
        thread = threading.Thread(target=self.run_monitor, daemon=True)
        thread.start()

    ##
    # @brief Creates a hidden window and starts the message loop for USB event handling.
    def run_monitor(self):
        """Set up the Windows event loop to monitor USB devices."""
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.window_proc
        wc.lpszClassName = "USBMonitorWindow"
        wc.hInstance = win32gui.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)
        self.hwnd = win32gui.CreateWindow(class_atom, "USB Monitor", 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)
        win32gui.PumpMessages()

    ##
    # @brief Handles Windows messages for USB plug/unplug events.
    def window_proc(self, hwnd, msg, wparam, lparam):
        """Handle Windows messages related to USB plug/unplug events."""
        if msg == WM_DEVICECHANGE:
            if wparam == DBT_DEVICEARRIVAL:
                self.handle_usb_plug()
            elif wparam == DBT_DEVICEREMOVECOMPLETE:
                self.handle_usb_unplug()
        return 0

    ##
    # @brief Handles logic for when a USB device is plugged in.
    def handle_usb_plug(self):
        """Handles USB plug-in event and checks for private keys."""
        new_drives = get_removable_drives()
        added_drives = [d for d in new_drives if d not in self.current_drives]

        for drive in added_drives:
            print(f"[USB Plugged In] Drive {drive} detected. Checking for private keys...")
            key_file = find_key_file(drive)
            if key_file:
                print(f"Private key found: {key_file} on drive {drive}")
                self.key_file_path = key_file
                self.key_file_drive = drive
                self.update_ui(True)
            else:
                print(f"No private key found on drive {drive}")

        self.current_drives = new_drives

    ##
    # @brief Handles logic for when a USB device is unplugged.
    def handle_usb_unplug(self):
        """Handles USB unplug event and determines which drive was removed."""
        new_drives = get_removable_drives()
        removed_drives = [d for d in self.current_drives if d not in new_drives]

        for drive in removed_drives:
            print(f"[USB Removed] Drive {drive} has been unplugged.")
            if drive == self.key_file_drive:
                # Unplugged drive with private key
                self.update_ui(False)
        self.current_drives = new_drives

    ##
    # @brief On application start, checks already connected USBs for private keys.
    def initial_key_check(self):
        """Search already plugged in USB drives for private key on startup."""
        found_key = False
        for drive in self.current_drives:
            key_file = find_key_file(drive)
            if key_file:
                print(f"Private key found on startup: {key_file} on drive {drive}")
                self.key_file_path = key_file
                self.key_file_drive = drive
                found_key = True
                break

        self.update_ui(found_key)

    ##
    # @brief Returns the full path to the detected private key file.
    # @return String containing the file path, or None.
    def get_key_file_path(self):
        return self.key_file_path

    ##
    # @brief Returns the drive letter of the USB containing the private key.
    # @return String containing the drive letter, or None.
    def get_key_file_drive(self):
        return self.key_file_drive
