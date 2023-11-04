import  ctypes
import psutil

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)

# find proccess id by name
def get_process_id_by_name(process_name):
    process_id = None
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            process_id = proc.pid
            break
    return process_id

from ctypes import wintypes
import win32api
import win32process
import struct

rPM = ctypes.WinDLL('kernel32',use_last_error=True).ReadProcessMemory
rPM.argtypes = [wintypes.HANDLE,wintypes.LPCVOID,wintypes.LPVOID,ctypes.c_size_t,ctypes.POINTER(ctypes.c_size_t)]
rPM.restype = wintypes.BOOL
wPM = ctypes.WinDLL('kernel32',use_last_error=True).WriteProcessMemory
wPM.argtypes = [wintypes.HANDLE,wintypes.LPVOID,wintypes.LPCVOID,ctypes.c_size_t,ctypes.POINTER(ctypes.c_size_t)]
wPM.restype = wintypes.BOOL

process_name = "ac_client.exe"
process_id = get_process_id_by_name(process_name)
print("siaosdaosndasodn")

# get handle to proccess_id with all access
process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, process_id)
# print(process_handle)
# PROCESS = win32api.OpenProcess(PROCESS_ALL_ACCESS,0,process_id)
# print("PROCESS: ", PROCESS, "PROCESS HANDLE: ", PROCESS.handle)

#get basee address of module
# module = win32process.EnumProcessModules(PROCESS)
# print("MODULE: ", module)
# base_address = module[0]
# print("BASE ADDRESS: ", base_address)

BASE_ADDRESS = 0x400000
ADDRESS1 = 0x17E360 + BASE_ADDRESS
ADDRESS2 = ctypes.pointer(ctypes.c_int(0))
bytes_read = ctypes.c_size_t()
result = rPM(process_handle, ADDRESS1, ADDRESS2, ctypes.sizeof(ADDRESS2), ctypes.byref(bytes_read))
print(f"result = {result}, bytes_read = {bytes_read.value}, ADDRESS2 = {struct.unpack('I', ADDRESS2.contents)}")
print(f"last error: {ctypes.get_last_error()}")
health_address = ADDRESS2.contents.value + 0xEC
ammo_address = ADDRESS2.contents.value + 0x138
while True:
    wPM(process_handle, health_address, ctypes.pointer(ctypes.c_int(1337)), ctypes.sizeof(ctypes.c_int(1337)), ctypes.byref(bytes_read))
    wPM(process_handle, ammo_address, ctypes.pointer(ctypes.c_int(1337)), ctypes.sizeof(ctypes.c_int(1337)), ctypes.byref(bytes_read))