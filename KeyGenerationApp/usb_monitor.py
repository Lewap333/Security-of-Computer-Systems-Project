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


def get_removable_drives():
    """Returns list of currently attached USB drives."""
    drives = [i for i in win32api.GetLogicalDriveStrings().split('\\\x00') if i]
    return [d for d in drives if win32file.GetDriveType(d) == win32con.DRIVE_REMOVABLE]


class USBMonitor:
    """Class to watch for USB events (plug/unplug)."""
    def __init__(self, update_ui):
        # Handle for hidden window - detection USB plug/unplug
        self.hwnd = None

        # Store initially connected drivers.
        self.current_drives = get_removable_drives()

        self.drive = None

        # Update UI
        self.update_ui = update_ui

    def start_monitoring(self):
        """Monitoring USB plug/unplug events in a separate thread."""
        thread = threading.Thread(target=self.run_monitor, daemon=True)
        thread.start()

    def run_monitor(self):
        """Set up the Windows event loop to monitor USB devices."""
        # https://learn.microsoft.com/en-us/windows/win32/learnwin32/creating-a-window
        # https://www.programcreek.com/python/index/322/win32gui

        # https://learn.microsoft.com/en-us/previous-versions/ms942860(v=msdn.10)
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.window_proc
        wc.lpszClassName = "USBMonitorWindow"
        wc.hInstance = win32gui.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)
        # https://learn.microsoft.com/en-us/previous-versions/ms959988(v=msdn.10)
        self.hwnd = win32gui.CreateWindow(class_atom, "USB Monitor", 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)
        win32gui.PumpMessages()

    def window_proc(self, hwnd, msg, wparam, lparam):
        """Handle Windows messages related to USB plug/unplug events."""
        if msg == WM_DEVICECHANGE:
            if wparam == DBT_DEVICEARRIVAL:
                self.handle_usb_plug()
            elif wparam == DBT_DEVICEREMOVECOMPLETE:
                self.handle_usb_unplug()
        return 0

    def handle_usb_plug(self):
        """Handles USB plug-in event and checks for private keys."""
        new_drives = get_removable_drives()
        added_drives = [d for d in new_drives if d not in self.current_drives]

        for drive in added_drives:
            print(f"[USB Plugged In] Drive {drive}")
            self.drive = drive

        # USB detected, can save private key
        self.update_ui(True)

        self.current_drives = new_drives

    def handle_usb_unplug(self):
        """Handles USB unplug event and determines which drive was removed."""
        new_drives = get_removable_drives()
        removed_drives = [d for d in self.current_drives if d not in new_drives]

        if self.drive in removed_drives:
            print(f"[USB Removed] Drive {self.drive} has been unplugged.")
            self.drive = None

        self.update_ui(False)

        self.current_drives = new_drives

    def initial_drive_check(self):
        """Search already plugged in USB drives for private key on startup."""
        if len(self.current_drives) == 0:
            self.update_ui(False)

        for drive in self.current_drives:
            print(f"[USB Drive] Drive {drive}")
            self.drive = drive
            self.update_ui(True)

    def get_drive(self ):
        return self.drive