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


class Tpdu(object):

    def __init__(self, tpdu: bytes):
        self.tpdu: bytes = tpdu

        self.pcb, self._nad, self._cid, self._crc = None, None, None, None
        self._inf_field: bytes = b""
        self.iblock_is_chaining, self.is_nad_present, self.is_cid_present = False, False, False
        self.ack_nack_bit: int = 0
        self.block_nb: int = 0
        self.i: bool = False
        self.r: bool = False
        self.s: bool = False
        self.parse_block()

    def parse_pcb(self):
        pcb = self.pcb
        # Iblock
        if (pcb & 0xC0) == 0x00:
            self.iblock_is_chaining = ((pcb & 0x10) == 0x10)
            self.is_nad_present = (pcb & 0x40) == 0x40
            self.is_cid_present = (pcb & 0x08) == 0x08
            self.i = True
        # Rblock
        elif (pcb & 0xC0) == 0x80:
            self.is_cid_present = (pcb & 0x08) == 0x08
            self.is_nad_present = False
            self.ack_nack_bit = (pcb & 0x10) >> 4
            self.block_nb = pcb & 1
            self.r = True
        # Sblock
        elif (pcb & 0xC0) == 0xC0:
            self.is_cid_present = (pcb & 0x08) == 0x08
            self.is_nad_present = False
            self.s = True

    def parse_block(self):
        self.pcb = self.tpdu[0]
        self.parse_pcb()
        cmpt = 1
        if self.is_cid_present:
            self._cid = self.tpdu[cmpt]
            cmpt += 1

        if self.is_nad_present:
            self._nad = self.tpdu[cmpt]
            cmpt += 1

        self._inf_field = self.tpdu[cmpt:-2]
        self._crc = self.tpdu[-2:]

    def get_tpdu(self):
        return self.tpdu

    @property
    def inf(self) -> bytes:
        return self._inf_field

    @inf.setter
    def inf(self, data: bytes):
        self._inf_field = data

    def is_chaining(self):
        return self.iblock_is_chaining

    def is_wtx(self):
        return (self.pcb & 0xF0) == 0xF0

    def get_wtx_reply(self):

        resp = [self.pcb]

        if self.is_cid_present:
            resp.append(self._cid)

        if self.is_nad_present:
            resp.append(self._nad)

        # inf field
        resp.append(self._inf_field[0] & 0x3F)

        return resp
