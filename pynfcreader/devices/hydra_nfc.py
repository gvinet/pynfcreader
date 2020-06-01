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
from pyHydrabus import NFC


class HydraNFC(Devices):

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

    def connect(self):
        self.__logger.info("Connect to HydraNFC")
        self.__logger.info("")
        self._hydranfc = NFC(self._port)

    def get_logger(self):
        return self.__logger

    def set_mode_iso14443A(self):
        self._hydranfc.mode = self._hydranfc.MODE_ISO_14443A

    def set_mode_iso15693(self):
        self._hydranfc.mode = self._hydranfc.MODE_ISO_15693

    def field_off(self):
        self.__logger.debug("Field off")
        self._hydranfc.rf = 0

    def field_on(self):
        self.__logger.debug("Field on")
        self._hydranfc.rf = 1

    def write_bits(self, data=b"", num_bits=0):
        resp = self._hydranfc.write_bits(data, num_bits)
        self.__logger.debug(f"\t<{' '.join(f'{hit:02X}' for hit in resp)}")
        self.__logger.debug("")
        return resp

    def write(self, data=b"", resp_len=None, transmitter_add_crc=True):
        self.__logger.debug("write")
        self.__logger.debug(f"\t>{data.hex()}")

        resp = self._hydranfc.write(data, transmitter_add_crc)
        self.__logger.debug(f"\t<{data.hex()}")
        self.__logger.debug("")

        return resp
