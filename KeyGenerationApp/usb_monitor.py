##
# @file usb_monitor.py
# @brief USB monitoring module for detecting private key storage devices.
#
# Monitors USB plug/unplug events on Windows using Win32 API.
# Used to detect insertion/removal of USB drives containing private keys.

import os
import win32api
import win32file
import win32con
import win32gui
import threading

##
# @brief File extension for private key files.
PRIVATE_KEY_EXTENSIONS = ".pem"

##
# @brief Windows USB event constants for WM_DEVICECHANGE messages.
WM_DEVICECHANGE = 0x0219
DBT_DEVICEARRIVAL = 0x8000
DBT_DEVICEREMOVECOMPLETE = 0x8004


##
# @brief Returns list of currently connected removable (USB) drives.
#
# @return List of drive letters representing USB drives.
def get_removable_drives():
    drives = [i for i in win32api.GetLogicalDriveStrings().split('\\\x00') if i]
    return [d for d in drives if win32file.GetDriveType(d) == win32con.DRIVE_REMOVABLE]


##
# @class USBMonitor
# @brief Class to monitor USB plug/unplug events and detect private key presence.
#
# Creates a hidden window to receive device change notifications from Windows.
class USBMonitor:
    ##
    # @brief Constructor.
    #
    # @param update_ui Function to call when USB state changes (True/False).
    def __init__(self, update_ui):
        self.hwnd = None                    # Handle to the hidden window.
        self.current_drives = get_removable_drives()  # Initially connected USB drives.
        self.drive = None                   # Currently selected drive containing private key.
        self.update_ui = update_ui          # Callback to update UI state.

    ##
    # @brief Starts USB monitoring in a separate thread.
    def start_monitoring(self):
        thread = threading.Thread(target=self.run_monitor, daemon=True)
        thread.start()

    ##
    # @brief Creates a hidden window and enters message loop to monitor USB events.
    def run_monitor(self):
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.window_proc
        wc.lpszClassName = "USBMonitorWindow"
        wc.hInstance = win32gui.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)

        self.hwnd = win32gui.CreateWindow(class_atom, "USB Monitor", 0, 0, 0, 0, 0,
                                          0, 0, wc.hInstance, None)
        win32gui.PumpMessages()

    ##
    # @brief Windows procedure for USB device change messages.
    #
    # @param hwnd Handle to the window.
    # @param msg Message type.
    # @param wparam Additional message-specific information.
    # @param lparam Additional message-specific information.
    #
    # @return 0 (message processed)
    def window_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_DEVICECHANGE:
            if wparam == DBT_DEVICEARRIVAL:
                self.handle_usb_plug()
            elif wparam == DBT_DEVICEREMOVECOMPLETE:
                self.handle_usb_unplug()
        return 0

    ##
    # @brief Handles USB plug-in event.
    #
    # Checks for new drives and updates internal state and UI.
    def handle_usb_plug(self):
        new_drives = get_removable_drives()
        added_drives = [d for d in new_drives if d not in self.current_drives]

        for drive in added_drives:
            print(f"[USB Plugged In] Drive {drive}")
            self.drive = drive

        self.update_ui(True)
        self.current_drives = new_drives

    ##
    # @brief Handles USB unplug event.
    #
    # Updates drive state and notifies UI if drive was removed.
    def handle_usb_unplug(self):
        new_drives = get_removable_drives()
        removed_drives = [d for d in self.current_drives if d not in new_drives]

        if self.drive in removed_drives:
            print(f"[USB Removed] Drive {self.drive} has been unplugged.")
            self.drive = None

        self.update_ui(False)
        self.current_drives = new_drives

    ##
    # @brief Checks for private key on startup in already connected drives.
    #
    # This is useful for initializing UI state on application launch.
    def initial_drive_check(self):
        if len(self.current_drives) == 0:
            self.update_ui(False)

        for drive in self.current_drives:
            print(f"[USB Drive] Drive {drive}")
            self.drive = drive
            self.update_ui(True)

    ##
    # @brief Returns the current drive where the private key is stored.
    #
    # @return Drive letter or None.
    def get_drive(self):
        return self.drive
