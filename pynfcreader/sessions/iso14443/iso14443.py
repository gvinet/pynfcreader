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


from pynfcreader.sessions.iso14443.tpdu import Tpdu
from pynfcreader.tools import utils


class Iso14443Session(object):

    def __init__(self, cid=0, nad=0, drv=None, block_size=16, mode: str = "reader"):
        self._init_pcb_block_nb()
        self._addNAD: bool = False
        self._addCID: bool = False
        self._cid = cid
        self._nad = nad
        self._drv = drv
        self._iblock_pcb_number = 0x00
        self._pcb_block_number = None
        self._drv = drv
        self._logger = self._drv.get_logger()
        self.block_size = block_size
        assert mode in ["card", "reader"]
        if mode == "card":
            self.card_emu = True
        else:
            self.card_emu = False

    def connect(self):
        self._drv.connect()
        self._drv.set_mode_iso14443A()

    def field_on(self):
        self._logger.info("field on")
        self._drv.field_on()

    def field_off(self):
        self._logger.info("field off")
        self._drv.field_off()

    def polling(self):
        self.send_reqa()
        self.send_select_full()
        self.send_pps()

    @property
    def block_size(self):
        return self._block_size

    @block_size.setter
    def block_size(self, size):
        assert (0 <= size <= 256)
        self._block_size = size

    def get_and_update_iblock_pcb_number(self):
        self._iblock_pcb_number ^= 1
        if self.card_emu:
            return self._iblock_pcb_number
        else:
            return self._iblock_pcb_number ^ 1

    def send_pps(self, cid=0x0, pps1=False, dri=0x0, dsi=0x0):
        self._logger.info("PPS")
        self._logger.info("\tPCD selected options:")
        pps0_pps1 = [0x01]
        if pps1:
            pps0_pps1.append(dri << 4 + dsi)
        self._logger.info("\tCID : 0x%X" % cid)
        self._logger.info("\tPPS1 %stransmitted" % ("not " * (not pps1)))

        data = bytes([0xD0 + cid] + pps0_pps1)
        self.comment_data("PPS:", data)
        resp = self._drv.write(data=data, resp_len=3, transmitter_add_crc=True)
        self.comment_data("PPS response:", resp)
        if resp[0] == (0xD0 + cid):
            self._logger.info("\tPPS accepted")
        else:
            self._logger.info("\tPPS rejected")
        self._logger.info("")

        return resp

    def _init_pcb_block_nb(self):
        self._pcb_block_number = 0

    def _inc_pcb_block_number(self):
        self._pcb_block_number ^= 1

    def _get_pcb_block_number(self):
        return self._pcb_block_number

    def _get_and_update_pcb_block_number(self):
        nb = self._get_pcb_block_number()
        self._inc_pcb_block_number()
        return nb

    def build_rblock(self, ack: bool = True) -> bytes:
        return self.build_rblock_ll(ack, self._addCID)

    def build_rblock_ll(self, ack: bool = True,
                        cid: bool = True,
                        block_number=None,
                        add_crc: bool = True) -> bytes:

        pcb = 0xA2
        data = ""
        if not ack:
            pcb |= 0x10

        if cid:
            pcb |= 0x08
            data = f"{self._cid:02X} "

        if block_number:
            pcb |= block_number
        else:
            pcb |= self.get_and_update_iblock_pcb_number()

        data = f"{pcb:02X}" + data

        return bytes.fromhex(data)

    def build_iblock(self, data, chaining_bit=False):
        """
         - 0
         - 0
         - 0
         - Chaining if 1
         - CID following if 1
         - NAD following if 1
         - 1
         - Block number
        """
        pcb = self.get_and_update_iblock_pcb_number() + 0x02

        cid = ""
        if self._addCID:
            cid = self._cid
            pcb |= 0x08

        if chaining_bit:
            pcb |= 0x10

        nad = ""
        if self._addNAD:
            nad = self._nad
            pcb |= 0x04

        header = [pcb]
        if nad != "":
            header.append(nad)
        if cid != "":
            header.append(cid)

        return bytes(header) + data

    def chaining_iblock(self, data: bytes = None, block_size: int = None):

        if not block_size:
            block_size = self.block_size

        block_lst = []
        fragmented_data_index = range(0, len(data), block_size)
        for hit in fragmented_data_index[:-1]:
            inf_field = data[hit:hit + block_size]
            frame = self.build_iblock(inf_field, chaining_bit=True)
            block_lst.append(frame)

        if fragmented_data_index[-1]:
            index = fragmented_data_index[-1]
        else:
            index = 0
        inf_field = data[index:index + block_size]
        frame = self.build_iblock(inf_field, chaining_bit=False)
        block_lst.append(frame)

        return block_lst

    def _send_tpdu(self, tpdu: bytes, add_crc: bool = True) -> bytes:
        self._logger.info("\t\t" + "TPDU command:")
        for hit in utils.get_pretty_print_block(tpdu):
            self._logger.info("\t\t" + hit)

        resp = self._drv.write(data=tpdu, resp_len=16, transmitter_add_crc=add_crc)

        resp = Tpdu(resp)
        self._logger.info("\t\t" + "TPDU response:")
        for hit in utils.get_pretty_print_block(resp.get_tpdu()):
            self._logger.info("\t\t" + hit)
        return resp

    def send_apdu(self, apdu):
        apdu = bytes.fromhex(apdu)
        self._logger.info("APDU command:")
        for hit in utils.get_pretty_print_block(apdu):
            self._logger.info("\t" + hit)

        block_lst = self.chaining_iblock(data=apdu)

        if len(block_lst) == 1:
            resp = self._send_tpdu(block_lst[0])
        else:
            self._logger.info("Block chaining, %d blocks to send" % len(block_lst))
            for iblock in block_lst:
                resp = self._send_tpdu(iblock)

        while resp.is_wtx():
            wtx_reply = resp.get_wtx_reply()
            resp = self._send_tpdu(wtx_reply)

        rapdu = resp.inf

        while resp.is_chaining():
            rblock = self.build_rblock()

            resp = self._send_tpdu(rblock)

            rapdu += resp.inf

        self._logger.info("APDU response:")
        for hit in utils.get_pretty_print_block(rapdu):
            self._logger.info("\t" + hit)
        return rapdu

    def send_raw_bytes(self, data, transmitter_add_crc=True):
        self._logger.info("Send Raw Bytes:")

        for hit in utils.get_pretty_print_block(data):
            self._logger.info("\t" + hit)

        resp = self._drv.write(data=data, transmitter_add_crc=transmitter_add_crc)
        self._logger.info("Response:")

        for hit in utils.get_pretty_print_block(resp):
            self._logger.info("\t" + hit)

        return resp

    def comment_data(self, msg, data):
        self._logger.info(msg)
        for hit in utils.get_pretty_print_block(data):
            self._logger.info("\t" + hit)
