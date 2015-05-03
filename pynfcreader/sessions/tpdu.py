/*
 * Copyright (C) 2015 Guillaume VINET
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
class Tpdu(object):

    def __init__(self, tpdu):
        self._tpdu = self.remove_leading_and_trailing_zero(tpdu)
        self._pcb, self._nad, self._cid, self._inf_field, self._crc = None, None, None, None, None
        self.iblock_is_chaining, self.is_nad_present, self.is_cid_present = False, False, False
        self.parse_block()

    def remove_leading_and_trailing_zero(self, tpdu):
        """
        TODO : optimize, should not happen...
        """
        cmpt = 0
        while tpdu[cmpt] == 0:
            cmpt += 1
        if cmpt != 0:
            cmpt -= 1
        tpdu = tpdu[cmpt:]

        cmpt = -1
        while tpdu[cmpt] == 0:
            cmpt -= 1

        if cmpt == -1:
            return tpdu
        else:
            cmpt += 1
            return tpdu[:cmpt]

    def parse_pcb(self):
        pcb = self._pcb
        if (pcb & 0xC0) == 0x00:
            self.iblock_is_chaining = ((pcb & 0x10) == 0x10)
            self.is_nad_present = (pcb & 0x04) == 0x04
            self.is_cid_present = (pcb & 0x08) == 0x08

    def parse_block(self):
        self._pcb = self._tpdu[0]
        self.parse_pcb()
        cmpt = 1
        if self.is_cid_present:
            self._cid = self._tpdu[cmpt]
            cmpt += 1

        if self.is_nad_present:
            self._nad = self._tpdu[cmpt]
            cmpt += 1

        self._inf_field = self._tpdu[cmpt:-2]
        self._crc = self._tpdu[-2:]

    def get_tpdu(self):
        return self._tpdu

    def get_inf_field(self):
        return self._inf_field

    def is_chaining(self):
        return self.iblock_is_chaining