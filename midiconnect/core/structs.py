import ctypes
from ctypes import wintypes


class MIDIHDR(ctypes.Structure):
    _fields_ = [
        ("lpData", ctypes.POINTER(ctypes.c_char)),  # Pointer to the message data
        ("dwBufferLength", wintypes.DWORD),  # Length of the buffer
        ("dwBytesRecorded", wintypes.DWORD),  # Actual data length
        ("dwUser", wintypes.DWORD),  # Custom user data (optional)
        ("dwFlags", wintypes.DWORD),  # Flags (e.g., prepared)
        ("lpNext", wintypes.HANDLE),  # Reserved for driver use
        ("reserved", wintypes.DWORD),  # Reserved
        ("dwOffset", wintypes.DWORD),  # Callback offset
        ("dwReserved", wintypes.DWORD * 8)  # Reserved
    ]


class MIDIEVENT(ctypes.Structure):
    _fields_ = [
        ("dwDeltaTime", wintypes.DWORD),  # Time delay before this event
        ("dwStreamID", wintypes.DWORD),   # Stream identifier
        ("dwEvent", wintypes.DWORD),      # Event data (status and data bytes)
        ("dwReserved", wintypes.DWORD)    # Reserved
    ]


class MIDIINCAPS(ctypes.Structure):
    _fields_ = [
        ("wMid", wintypes.WORD),           # Manufacturer ID
        ("wPid", wintypes.WORD),           # Product ID
        ("vDriverVersion", wintypes.DWORD),  # Version of the driver
        ("szPname", ctypes.c_char * 32),  # Product name
        ("dwSupport", wintypes.DWORD)      # Capabilities of the input port
    ]


class MIDIOUTCAPS(ctypes.Structure):
    _fields_ = [
        ("wMid", wintypes.WORD),           # Manufacturer ID
        ("wPid", wintypes.WORD),           # Product ID
        ("vDriverVersion", wintypes.DWORD),  # Version of the driver
        ("szPname", ctypes.c_char * 32),  # Product name
        ("dwSupport", wintypes.DWORD)      # Capabilities of the output port
    ]


class MIDIPROPTEMPO(ctypes.Structure):
    _fields_ = [
        ("dwTempo", wintypes.DWORD)  # Tempo (microseconds per beat)
    ]


class MIDIPROPTIMEDIV(ctypes.Structure):
    _fields_ = [
        ("dwTimeDiv", wintypes.DWORD)  # Time division (e.g., ticks per beat)
    ]


class MIDISTRMBUFFVER(ctypes.Structure):
    _fields_ = [
        ("dwVersion", wintypes.DWORD)  # Version of the streaming buffer
    ]
