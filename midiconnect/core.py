import abc
import ctypes
from ctypes import wintypes

# Windows multimedia (winmm) library
winmm = ctypes.windll.winmm


class MidiConnection(metaclass=abc.ABCMeta):
    def __init__(self, port: int = 0) -> None:
        self._port = port
        self._handle = None
        self.open()

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"Expected 'port' to be an integer, but got type '{type(value).__name__}'.")
        self._port = value

    @property
    def handle(self):
        return self._handle

    @abc.abstractmethod
    def open(self) -> None:
        """Open the MIDI connection."""
        pass

    @abc.abstractmethod
    def close(self) -> None:
        """Close the MIDI connection."""
        pass

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class MidiOut(MidiConnection):
    def open(self) -> None:
        self._handle = wintypes.HANDLE()
        result = winmm.midiOutOpen(
            ctypes.byref(self._handle),  # Pointer to the device handle
            self._port,                 # Port number
            0,                          # Callback function (NULL)
            0,                          # Callback instance (NULL)
            0                           # Callback flags (NULL)
        )
        if result != 0:  # MMSYSERR_NOERROR is 0
            raise RuntimeError(f"Failed to open MIDI output port. Error code: {result}")

    def send(self, status: int, data1: int, data2: int) -> None:
        if self._handle is None:
            raise RuntimeError("MIDI output is not open.")
        message = (data2 << 16) | (data1 << 8) | status  # Combine into a single 32-bit message
        result = winmm.midiOutShortMsg(self._handle, message)
        if result != 0:
            raise RuntimeError(f"Failed to send MIDI message. Error code: {result}")

    def reset(self) -> None:
        if self._handle is None:
            raise RuntimeError("MIDI output is not open.")
        result = winmm.midiOutReset(self._handle)
        if result != 0:
            raise RuntimeError(f"Failed to reset MIDI output. Error code: {result}")

    def close(self) -> None:
        if self._handle:
            result = winmm.midiOutClose(self._handle)
            if result != 0:
                raise RuntimeError(f"Failed to close MIDI output. Error code: {result}")
            self._handle = None


class MidiIn(MidiConnection):
    def open(self) -> None:
        self._handle = wintypes.HANDLE()
        result = winmm.midiInOpen(
            ctypes.byref(self._handle),  # Pointer to the device handle
            self._port,                 # Port number
            0,                          # Callback function (NULL)
            0,                          # Callback instance (NULL)
            0                           # Callback flags (NULL)
        )
        if result != 0:  # MMSYSERR_NOERROR is 0
            raise RuntimeError(f"Failed to open MIDI input port. Error code: {result}")

    def start(self) -> None:
        if self._handle is None:
            raise RuntimeError("MIDI input is not open.")
        result = winmm.midiInStart(self._handle)
        if result != 0:
            raise RuntimeError(f"Failed to start MIDI input. Error code: {result}")

    def stop(self) -> None:
        if self._handle is None:
            raise RuntimeError("MIDI input is not open.")
        result = winmm.midiInStop(self._handle)
        if result != 0:
            raise RuntimeError(f"Failed to stop MIDI input. Error code: {result}")

    def reset(self) -> None:
        if self._handle is None:
            raise RuntimeError("MIDI input is not open.")
        result = winmm.midiInReset(self._handle)
        if result != 0:
            raise RuntimeError(f"Failed to reset MIDI input. Error code: {result}")

    def close(self) -> None:
        if self._handle:
            result = winmm.midiInClose(self._handle)
            if result != 0:
                raise RuntimeError(f"Failed to close MIDI input. Error code: {result}")
            self._handle = None
