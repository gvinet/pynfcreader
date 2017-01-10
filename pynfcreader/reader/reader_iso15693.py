# Copyright (C) 2015 Guillaume VINET
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

from pynfcreader.devices.hydraNFC import HydraNFC
from pynfcreader.sessions.iso15693 import Iso15693Session

class ReaderHydraNFC(object):

    def __init__(self, port="COM8", debug_mode=True, block_size = 16):
        self.__driver = HydraNFC(port=port, debug=debug_mode)
        self.__session = Iso15693Session(drv=self.__driver, block_size= block_size)
        self.__logger = self.__driver.getLogger()

    def connect(self):
        self.__driver.connect()
        self.__driver.reset_and_configure()
        self.__driver.set_mode_iso15693()

    def field_on(self):
        self.__logger.info("field on")
        self.__driver.field_on()
        self.__logger.info("")

    def field_off(self):
        self.__logger.info("")
        self.__driver.field_off()
        self.__logger.info("")

    def inventory(self):
        return self.__session.inventory()

    def get_system_info(self, uid):
        return self.__session.get_system_info(uid)

    def read_single_block(self, block_number):
        return self.__session.read_single_block(block_number)

    def write_single_block(self, block_number, data):
        return self.__session.write_single_block(block_number, data)

    def get_block_security_status(self, uid, first_block_number, block_number):
        return self.__session.get_block_security_status(uid, first_block_number, block_number)

    def get_all_auto(self):
        self.__session.get_all_auto()

    def send(self, cmd):
        return self.__session.send(cmd)

