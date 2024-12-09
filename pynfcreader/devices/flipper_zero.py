# Copyright (C) 2015-2024 Guillaume VINET
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys

import serial
import serial.tools.list_ports

from pynfcreader.devices.devices import Devices
from pynfcreader.devices.connection import SerialCnx, SerialCnxVirtual

class FlipperZero(Devices):

    def __init__(self, port: str = "", baudrate: int = 115200 * 8, debug: bool = True, recording="", log=""):

        self._port = port if port != "" else self.auto_search()
        self._baudrate = baudrate
        if log == "":
            self.cnx = SerialCnx(self._port, baudrate=115200 * 8, timeout=None, recording=recording)
        else:
            self.cnx = SerialCnxVirtual(log)

        self.__logger = logging.getLogger()
        stream_handler = logging.StreamHandler()
        stream_debug_formatter = logging.Formatter('%(levelname)s  ::  %(message)s')
        stream_handler.setFormatter(stream_debug_formatter)

        self.__logger.setLevel(logging.INFO)
        stream_handler.setLevel(logging.INFO)

        self._python_ver = sys.version[0]

        if debug:
            self.__logger.setLevel(logging.DEBUG or logging.INFO)
            stream_handler.setLevel(logging.DEBUG or logging.INFO)

        self.__logger.addHandler(stream_handler)

    def auto_search(self) -> str:
        for port in serial.tools.list_ports.comports():
            if "Flipper" in port.description:
                return port.device
        print("Error. No flipper zero device found")
        exit(1)

    def connect(self):

        self.__logger.info("Connect to Flipper Zero")
        self.__logger.info("")

        # self.cnx.connect()

        self.cnx.reset_input_buffer()

        r = self.cnx.readline().decode()

        while "Firmware version:" not in r:
            r = self.cnx.readline().decode()

        self.cnx.readline().decode()

        self.cnx.set_timeout(0.1)

    def close(self):
        self.cnx.close()

    def get_logger(self):
        return self.__logger

    def set_mode_iso14443A(self):
        self.cnx.reset_input_buffer()
        self.cnx.reset_output_buffer()
        self.cnx.write(b"nfc mode_14443_a\r\n")
        r = self.read_all()
        assert "Set mode ISO 14443 A" in r

    def set_mode_emu_iso14443A(self):
        self.cnx.reset_input_buffer()
        self.cnx.reset_output_buffer()
        self.cnx.write(b"nfc mode_emu_14443_a\r\n")
        return self.read_all()
        # assert "Set mode ISO 14443 A" in r

    def set_mode_iso14443B(self):
        self.cnx.reset_input_buffer()
        self.cnx.reset_output_buffer()
        self.cnx.write(b"nfc mode_14443_b\r\n")
        return self.read_all()

    def set_mode_iso15693(self):
        self.cnx.reset_input_buffer()
        self.cnx.reset_output_buffer()
        self.cnx.write(b"nfc mode_15693\r\n")
        return self.read_all()

    def set_mode_emu_iso15693(self):
        self.cnx.reset_input_buffer()
        self.cnx.reset_output_buffer()
        self.cnx.write(b"nfc mode_emu_15693\r\n")
        return self.read_all()

    def start_emulation(self):
        self.cnx.reset_input_buffer()
        self.cnx.reset_output_buffer()
        self.cnx.write(b"nfc run_emu\r\n")
        self.read_all()
        self.cnx.set_timeout(None)

    def emu_get_cmd(self) -> str:
        return str(self.cnx.readline().decode()).strip()

    def emu_send_resp(self, resp: bytes, flipper_add_crc=False) -> None:

        crc = b"1" if flipper_add_crc else b"0"
        self.cnx.write(crc + resp.hex().encode() + b"\n")

    def read_all(self):
        r = ""
        d = self.cnx.readline().decode()
        while d != "":
            r += d
            d = self.cnx.readline().decode()
        return r

    def field_off(self):
        self.__logger.debug("Field off")
        self.cnx.reset_input_buffer()
        self.cnx.reset_output_buffer()
        self.cnx.write(b"nfc off\r\n")
        r = self.read_all()
        assert "Field is off" in r

    def field_on(self):
        self.__logger.debug("Field on")
        self.cnx.reset_input_buffer()
        self.cnx.reset_output_buffer()
        self.cnx.write(b"nfc on\r\n")
        self.read_all()

    def write_bits(self, data=b"", num_bits=0):

        self.cnx.reset_input_buffer()
        self.cnx.reset_output_buffer()
        self.cnx.write(b"nfc reqa\r\n")
        resp = bytes.fromhex(self.read_all().split("\r\n")[1])

        self.__logger.debug(f"\t<{' '.join(f'{hit:02X}' for hit in resp)}")
        self.__logger.debug("")

        return resp

    def set_uid(self, uid: str):
        self.__logger.debug(f"set uid: {uid}")
        self.cnx.reset_input_buffer()
        self.cnx.reset_output_buffer()
        self.cnx.write(b"nfc set_uid {uid}\r\n")
        r = self.read_all()

    def set_sak(self, sak: int):
        assert sak in range(256)
        self.__logger.debug(f"set sak: {sak}")
        self.cnx.reset_input_buffer()
        self.cnx.reset_output_buffer()
        self.cnx.write(b"nfc set_sak {sak:02X}\r\n")
        r = self.read_all()

    def set_atqa(self, atqa: str):
        self.__logger.debug(f"set atqa: {atqa}")
        self.cnx.reset_input_buffer()
        self.cnx.reset_output_buffer()
        self.cnx.write(b"nfc set_sak atqa\r\n")
        r = self.read_all()

    def write(self, data=b"", resp_len=None, transmitter_add_crc=True):
        self.cnx.reset_input_buffer()
        self.cnx.reset_output_buffer()
        add_crc = 1 if transmitter_add_crc else 0

        self.__logger.debug("write")
        self.__logger.debug(f"\t>{data.hex()}")

        self.cnx.write(f"nfc send {add_crc} {data.hex()}\r\n".encode())
        resp = bytes.fromhex(self.read_all().split("\r\n")[1])

        self.__logger.debug(f"\t<{data.hex()}")
        self.__logger.debug("")

        return resp
