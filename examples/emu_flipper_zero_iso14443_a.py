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

import time
from pynfcreader.sessions.iso14443.tpdu import Tpdu
from pynfcreader.devices import flipper_zero
from pynfcreader.sessions.iso14443.iso14443a import Iso14443ASession

fz = flipper_zero.FlipperZero("", debug=False)

fz.connect()
fz.set_mode_emu_iso14443A()

def process_apdu(cmd: str):
    print(f"apdu {cmd}")
    if cmd == "00a404000e325041592e5359532e444446303100":
        rapdu = "6F57840E325041592E5359532E4444463031A545BF0C42611B4F07A0000000421010500243428701019F2808400200000000000061234F07A0000000041010500A4D4153544552434152448701029F280840002000000000009000"
    else:
        rapdu = "6F00"
    return rapdu

class Emu(Iso14443ASession):
    def __init__(self, cid=0, nad=0, drv=None, block_size=16, process_function=None):
        Iso14443ASession.__init__(self, cid, nad, drv, block_size)
        self._addCID = False
        self.drv = self._drv
        self.process_function = process_function

    def run(self):
        self.drv.start_emulation()
        print("...go!")
        self.low_level_dispatcher()

    def low_level_dispatcher(self):
        capdu = bytes()
        ats_sent = False

        iblock_resp_lst = []

        while 1:
            r = fz.emu_get_cmd()
            rtpdu = None
            print(f"tpdu < {r}")
            if r == "off":
                print("field off")
            elif r == "on":
                print("field on")
                ats_sent = False
            else:
                tpdu = Tpdu(bytes.fromhex(r))

                if (tpdu.tpdu[0] == 0xE0) and (ats_sent is False):
                    rtpdu, crc = "0A788082022063CBA3A0", True
                    ats_sent = True
                elif tpdu.r:
                    print("r block")
                    if r == "BA00BED9":
                        rtpdu, crc = "BA00", True
                    elif r[0:2] in ["A2", "A3", "B2", "B3"]:
                        rtpdu, crc = iblock_resp_lst.pop(0).hex(), True
                elif tpdu.s:
                    print("s block")
                elif tpdu.i:
                    print("i block")
                    capdu += tpdu.get_inf_field()

                    if tpdu.is_chaining() is False:
                        rapdu = self.process_function(capdu.hex())
                        capdu = bytes()
                        iblock_resp_lst = self.chaining_iblock(data=bytes.fromhex(rapdu))
                        rtpdu, crc = iblock_resp_lst.pop(0).hex(), True

                print(f">>> rtdpu {rtpdu}\n")
                fz.emu_send_resp(rtpdu.encode(), crc)


emu = Emu(drv=fz, process_function=process_apdu)
emu.run()
