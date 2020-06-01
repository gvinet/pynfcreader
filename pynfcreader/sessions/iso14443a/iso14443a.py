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


from pynfcreader.sessions.iso14443a.tpdu import Tpdu
from pynfcreader.tools import utils


class Iso14443ASession(object):

    def __init__(self, cid=0, nad=0, drv=None, block_size=16):
        self._init_pcb_block_nb()
        self._addNAD = False
        self._addCID = True
        self._cid = cid
        self._nad = nad
        self._drv = drv
        self._iblock_pcb_number = 0x00
        self._pcb_block_number = None
        self._drv = drv
        self._logger = self._drv.get_logger()
        self.block_size = block_size

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
        return self._iblock_pcb_number ^ 1

    def send_reqa(self):
        """
        REQA = REQ frame - Type A
        0x26 - 7 bits - no CRC

        ret :
          - nothing
          - ATQA (Answer To Request - Type A)
        """
        self.comment_data("REQA (7 bits):", b"\x26")
        resp = self._drv.write_bits(b'\x26', 7)
        if not resp:
            raise Exception("REQ A failure")
        self.comment_data("ATQA:", resp)
        return resp

    def send_wupa(self):
        """
        REQA = REQ frame - Type A
        0x26 - 7 bits - no CRC

        ret :
          - nothing
          - ATQA (Answer To Request - Type A)
        """
        self.comment_data("WUPA (7 bits):", [0x52])
        resp = self._drv.write_bits(b'\x52', 7)
        self.comment_data("ATQA:", resp)

    def send_select_full(self, FSDI="0", CID="0"):
        """
        Select
        0x9320 - 8 bits - no CRC
        """

        uid1 = bytes()
        uid2 = bytes()
        uid3 = bytes()

        # 93 : Select cascade level 1
        # 20 : 2 * 8 + 0 = 16 bits = 2 bytes transmitted
        # No CRC
        data = bytes([0x93, 0x20])
        self.comment_data("Select cascade level 1:", data)
        resp = self._drv.write(data=data, transmitter_add_crc=False)
        self.comment_data("Select cascade level 1 response:", resp)

        # resp : CT + UID (3 bytes) + BCC
        # 93 : Select cascade level 1
        # 70 : 7 * 8 + 0 = 56 bits  = 7 bytes transmitted
        # 4 bytes : CT + UID
        # CRC_A (2 bytes)
        uid1 = resp
        data = bytes([0x93, 0x70]) + uid1
        self.comment_data("Select cascade level 1:", data)
        resp = self._drv.write(data=data, resp_len=3, transmitter_add_crc=True)
        self.comment_data("Select cascade level 1 response:", resp)

        # if uid1[0] == 0x88:
        #
        #     # resp : SAK + CRC_A
        #     # Cascade bit set? => UID not complete
        #     if resp[0] & 0x04:
        #         # 95 : Select cascade level 2 (SEL)
        #         # 20 : 2 * 8 + 0 = 16 bits = 2 bytes transmitted
        #         # No CRC
        #         data = [0x95, 0x20]
        #         self.comment_data("Select cascade level 2:", data)
        #         resp = self.__drv.write(data = data, resp_len = 5)
        #         self.comment_data("Select cascade level 2 response:", resp)
        #
        #         # resp : 4 bytes (UID) (+BCC not see in this implementation)
        #         # 95 : Select cascade level 2 (SEL)
        #         # 70 : 7 * 8 + 0 = 56 bits  = 7 bytes transmitted
        #         # No CRC
        #         uid2 = resp
        #         data = [0x95, 0x70] + uid2
        #         self.comment_data("Select cascade level 2:", data)
        #         resp = self.__drv.write(data = data, resp_len = 3, crc_in_cmd=False)
        #         self.comment_data("Select cascade level 2 response:", resp)
        #
        #         # resp : SAK + CRC_A
        #         # Cascade bit set? => UID not complete
        #         if resp[0] & 0x04:
        #             # 97 : Select cascade level 3 (SEL)
        #             # 20 : 2 * 8 + 0 = 16 bits = 2 bytes transmitted
        #             # No CRC
        #             # resp = self.hf14a_raw(data = "9720", leaveSigOnAfterRec= True, fieldMode = "OnWithoutSelect")
        #             self.__logger.info("Select cascade level 3")
        #             resp = self.__drv.write(data = [0x97, 0x20], resp_len = 3)
        #
        #             # resp : 4 bytes (UID) + BCC
        #             # 97 : Select cascade level 32 (SEL)
        #             # 70 : 7 * 8 + 0 = 56 bits  = 7 bytes transmitted
        #             # No CRC
        #             uid2 = resp
        #             # resp = self.hf14a_raw(data = "9770" + resp, leaveSigOnAfterRec= True, fieldMode = "OnWithoutSelect", AutoAddCRC = True)
        #             self.__logger.info("Select cascade level 3")
        #             resp = self.__drv.write(data = [0x97, 0x70] + resp, resp_len = 3, crc_in_cmd=False)
        #
        # RATS (Request Answer To Select)
        resp = self.send_rats_a(FSDI, CID)
        return (uid1 + uid2 + uid3, resp)

    def send_rats_a(self, FSDI="0", CID="0"):
        """
        Request for answer to select - Type A
        0xE0 - FSDI | CID - CRC_A
        :param FSDI: defines the maximum size of a frame the PCD is able to receive.
            - 0 : 16 bytes
            - 1 : 24 bytes
            - 2 : 32
            - 3 : 40
            - 4 : 48
            - 5 : 64
            - 6 : 96
            - 7 : 128
            - 8 : 256
            - .. : RFU
        :param CID: logical number of the addressed PICC in the range from 0 to 14.
        :return: ATS (Answer to select)
        """
        dico = {"0": 16, "1": 24, "2": 32, "3": 40, "4": 48, "5": 64, "6": 96, "7": 128, "8": 256}
        self._logger.info("Request for Answer To Select (RATS):")
        self._logger.info("\tPCD selected options:")
        self._logger.info("\t\tFSDI : 0x%s => max PCD frame size : %d bytes" % (FSDI, dico[FSDI]))
        self._logger.info("\t\tCID  : 0x%s" % FSDI)

        data = bytes([0xE0, int(FSDI + CID, 16)])
        self.comment_data("RATS", data)
        resp = self._drv.write(data=data, resp_len=20, transmitter_add_crc=True)

        # resp[0] = TL = length without counting the 2 CRC bytes
        resp = resp[:resp[0] + 2]
        self.comment_data("Answer to Select (ATS = RATS response):", resp)

        T0 = resp[1]
        self._logger.info("\tT0 : 0x%02X", T0)
        self._logger.info("\t\tFSCI : 0x%01X => max card frame size : %d bytes" % (T0 & 0xF, dico[str(T0 & 0xF)]))
        ta1 = None
        tb1 = None
        tc1 = None
        cmpt = 2
        if T0 & 0x10:
            self._logger.info("\t\tTA(1) present")
            ta1 = resp[cmpt]
            cmpt += 1
        if T0 & 0x20:
            self._logger.info("\t\tTB(1) present")
            tb1 = resp[cmpt]
            cmpt += 1
        if T0 & 0x40:
            self._logger.info("\t\tTC(1) present")
            tc1 = resp[cmpt]
            cmpt += 1

        if ta1:
            self._logger.info("\tTA(1) : 0x%02X" % ta1)
            self._logger.info("\t\tInterpretation : TODO...")
        if tb1:
            self._logger.info("\tTB(1) : 0x%02X" % tb1)
            self._logger.info("\t\tInterpretation : TODO...")
        if tc1:
            self._logger.info("\tTC(1) : 0x%02X" % tc1)
            self._addNAD = ((tc1 & 0x01) == 0x01)
            self._logger.info("\t\tNAD %ssupported" % ((not self._addNAD) * "not "))
            self._addCID = ((tc1 & 0x02) == 0x02)
            self._logger.info("\t\tCID %ssupported" % ((not self._addCID) * "not "))
        self._logger.info("\tHistorical bytes : %s" % utils.int_array_to_hex_str(resp[cmpt:-2]))
        self._logger.info("\tCRC : %s" % utils.int_array_to_hex_str(resp[-2:]))

        self._logger.info("")
        self._logger.info("")
        self._logger.info("")
        return resp

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

    def get_rblock(self, ack=True, cid=True, block_number=None):

        pcb = 0xA2
        cid = ""
        if not ack:
            pcb |= 0x10

        if cid:
            pcb |= 0x08
            cid = f" 0x{self._cid:02X} "

        if block_number:
            pcb |= block_number
        else:
            pcb |= self.get_and_update_iblock_pcb_number()

        if cid != "":
            return bytes([pcb, cid])
        else:
            return bytes([pcb])

    def getIBlock(self, data, chaining_bit=False):
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

    def chaining_iblock(self, data=None, block_size=None):

        if not block_size:
            block_size = self.block_size

        block_lst = []
        fragmented_data_index = range(0, len(data), block_size)
        for hit in fragmented_data_index[:-1]:
            inf_field = data[hit:hit + block_size]
            frame = self.getIBlock(inf_field, chaining_bit=True)
            block_lst.append(frame)

        if fragmented_data_index[-1]:
            index = fragmented_data_index[-1]
        else:
            index = 0
        inf_field = data[index:index + block_size]
        frame = self.getIBlock(inf_field, chaining_bit=False)
        block_lst.append(frame)

        return block_lst

    def _send_tpdu(self, tpdu):
        self._logger.info("\t\t" + "TPDU command:")
        for hit in utils.get_pretty_print_block(tpdu):
            self._logger.info("\t\t" + hit)

        resp = self._drv.write(data=tpdu, resp_len=16, transmitter_add_crc=True)

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

        rapdu = resp.get_inf_field()

        while resp.is_chaining():
            rblock = self.get_rblock()

            resp = self._send_tpdu(rblock)

            rapdu += resp.get_inf_field()

        self._logger.info("APDU response:")
        for hit in utils.get_pretty_print_block(rapdu):
            self._logger.info("\t" + hit)
        return rapdu

    def comment_data(self, msg, data):
        self._logger.info(msg)
        for hit in utils.get_pretty_print_block(data):
            self._logger.info("\t" + hit)
