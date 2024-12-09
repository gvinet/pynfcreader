import csv
from pathlib import Path

import serial
import serial.tools.list_ports


class SerialCnx:
    def __init__(self, port: str, baudrate: int, timeout=None, recording: str = ""):
        self.port: str = port
        self.baudrate: int = baudrate
        self.timeout: int = timeout
        self.cnx = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)
        self.recording_writer = None
        self._recording_init(recording)

    def _recording_init(self, recording):
        if recording != "":
            self.recording_writer = csv.writer(Path(recording).open(mode="w", newline="", encoding="utf-8"))
            self.recording_writer.writerow(["Type", "Data"])

    def _recording_write(self, mode: str, data: str):
        if self.recording_writer:
            self.recording_writer.writerow([mode, data])

    def reset_input_buffer(self):
        self.cnx.reset_input_buffer()

    def reset_output_buffer(self):
        self.cnx.reset_output_buffer()

    def set_timeout(self, timeout: int):
        self.cnx.timeout = timeout

    def close(self):
        self.cnx.close()

    def readline(self):
        data = self.cnx.readline()
        self._recording_write("R", data.decode())
        return data

    def write(self, data: bytes):
        self._recording_write("W", data.decode())
        self.cnx.write(data)


class SerialCnxVirtual:
    def __init__(self, log: str = ""):
        self.reader = csv.reader(Path(log).open(mode="r", encoding="utf-8", newline=""))
        self._log_get_line()

    def _log_get_line(self):
        return next(self.reader)

    def reset_input_buffer(self):
        pass

    def reset_output_buffer(self):
        pass

    def set_timeout(self, timeout: int):
        pass

    def close(self):
        pass

    def readline(self):
        data = self._log_get_line()
        return data[1].encode()

    def write(self, data: bytes):
        a = self._log_get_line()
