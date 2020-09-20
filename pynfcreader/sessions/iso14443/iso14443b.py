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


from pynfcreader.sessions.iso14443.iso14443 import Iso14443Session


class Iso14443BSession(Iso14443Session):

    def __init__(self, cid=0, nad=0, drv=None, block_size=16):
        Iso14443Session.__init__(self, cid, nad, drv, block_size)
        self.pupi = None

    def connect(self):
        self._drv.connect()
        self._drv.set_mode_iso14443B()

    def polling(self):
        self.send_reqb()
        self.send_attrib()
        # self.send_select_full()
        # self.send_pps()

    def send_reqb(self):
        reqb = bytes.fromhex("050000")
        self.comment_data("REQB:", reqb)
        resp = self._drv.write(reqb, 1)
        if not resp:
            raise Exception("REQ B failure")
        self.comment_data("ATQB:", resp)
        self.pupi = resp[1:5]
        return resp

    def send_attrib(self, pupi=None):
        if pupi is None:
            pupi = self.pupi
        reqb = bytes.fromhex(f"1D {pupi.hex()}  00 00 01 00")
        self.comment_data("REQB:", reqb)
        resp = self._drv.write(reqb, 1)
        if not resp:
            raise Exception("REQ B failure")
        self.comment_data("ATQB:", resp)
        # self.pupi = resp[1:5]
        return resp
