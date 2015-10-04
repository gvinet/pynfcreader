#
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
#
from pynfcreader.devices.hydraNFC import HydraNFC
from pynfcreader.sessions.iso14443a import Iso14443ASession


class ReaderHydraNFC(object):

    def __init__(self, port="COM8", baudrate=230400, debug_mode=True):
        """

        :param port: aaa
        :param baudrate:  bbb
        :param debug_mode:  ccc
        :return:
        """
        self.__driver = HydraNFC(port=port, baudrate=baudrate, debug=debug_mode)
        self.__session = Iso14443ASession(drv=self.__driver)
        self.__logger = self.__driver.getLogger()

    def connect(self):
        self.__driver.connect()
        self.__driver.reset()
        self.__driver.configure()
        self.__driver.set_mode_iso14443A()

    def polling(self):
        self.__session.send_reqa()
        self.__session.sendSelectFull()
        self.__session.send_pps()

    def send_apdu(self, apdu):

        resp = self.__session.send_apdu(apdu)

        return resp
