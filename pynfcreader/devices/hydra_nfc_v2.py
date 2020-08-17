# Copyright (C) 2015-2020 Guillaume VINET
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

from pynfcreader.devices.devices import Devices
import serial

class HydraNFCv2(Devices):

    def __init__(self, port="C0M8", debug=True):

        self._port = port
        self._hydranfc = None

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

    def enter_bbio(self):
        self._hydranfc.timeout = 0.01
        for _ in range(20):
            self._hydranfc.write(b"\x00")
            if b"BBIO1" in self._hydranfc.read(5):
                self._hydranfc.reset_input_buffer()
                self._hydranfc.timeout = None

                # We enter reader mode
                self._hydranfc.write(b"\x0E")
                if self._hydranfc.read(4) != b"NFC2":
                    raise Exception("Cannot enter BBIO Reader mode")
                return
        raise Exception("Cannot enter BBIO mode.")

    def connect(self):
        self.__logger.info("Connect to HydraNFC")
        self.__logger.info("")
        self._hydranfc = serial.Serial(self._port, timeout=None)
        self.enter_bbio()

    def get_logger(self):
        return self.__logger

    def set_mode_iso14443A(self):
        self._hydranfc.write(b"\x06")

    def set_mode_iso14443B(self):
        self._hydranfc.write(b"\x09")

    def set_mode_iso15693(self):
        self._hydranfc.write(b"\x07")

    def field_off(self):
        self.__logger.debug("Field off")
        self._hydranfc.write(b"\x02")

    def field_on(self):
        self.__logger.debug("Field on")
        self._hydranfc.write(b"\x03")

    def write_bits(self, data=b"", num_bits=0):
        # resp = self._hydranfc.write_bits(data, num_bits)

        self._hydranfc.write(b"\x08")
        rx_len = int.from_bytes(self._hydranfc.read(1), byteorder="little")
        resp  = self._hydranfc.read(rx_len)

        self.__logger.debug(f"\t<{' '.join(f'{hit:02X}' for hit in resp)}")
        self.__logger.debug("")

        return resp

    def write(self, data=b"", resp_len=None, transmitter_add_crc=True):
        self.__logger.debug("write")
        self.__logger.debug(f"\t>{data.hex()}")

        self._hydranfc.write(b"\x05")
        self._hydranfc.write(int(transmitter_add_crc).to_bytes(1, byteorder="big"))
        self._hydranfc.write(len(data).to_bytes(1, byteorder="big"))
        self._hydranfc.write(data)

        rx_len = int.from_bytes(self._hydranfc.read(1), byteorder="little")

        resp =  self._hydranfc.read(rx_len)

        self.__logger.debug(f"\t<{data.hex()}")
        self.__logger.debug("")

        return resp
