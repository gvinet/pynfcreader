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

from pynfcreader.sessions.tpdu import Tpdu
from pynfcreader.tools import utils

class Iso14443ASession(object):
    
    def __init__(self, CID = 0, NAD = 0, drv = None, block_size = 16):
        self.__initPCB_BlockNumber()
        self.__addNAD = False
        self.__addCID = True
        self.__CID = CID
        self.__NAD = NAD
        self.__drv = drv
        self.__iblock_pcb_number = 0x00
        self.__driver = drv
        self.__logger = self.__driver.getLogger()
        self.set_block_size(block_size)

    def set_block_size(self, size):
        assert( 0 <= size <= 256)
        self.__block_size = size

    def get_block_size(self):
        return self.__block_size

    def get_and_update_iblock_pcb_number(self):
        self.__iblock_pcb_number ^= 1
        return self.__iblock_pcb_number ^ 1

    def send_reqa(self):
        """
        REQA = REQ frame - Type A
        0x26 - 7 bits - no CRC

        ret :
          - nothing
          - ATQA (Answer To Request - Type A)
        """
        self.commentData("REQA (7 bits):", [0x26])
        resp = self.__drv.send_reqa()
        self.commentData("ATQA:", resp)
        return resp

    def send_wupa(self):
        """
        REQA = REQ frame - Type A
        0x26 - 7 bits - no CRC

        ret :
          - nothing
          - ATQA (Answer To Request - Type A)
        """
        self.commentData("WUPA (7 bits):", [0x52])
        resp = self.__drv.send_wupa()
        self.commentData("ATQA:", resp)

    def sendSelectFull(self, FSDI = "0", CID = "0"):
        """
        Select
        0x9320 - 8 bits - no CRC
        """

        uid1 = []
        uid2 = []
        uid3 = []

        # 93 : Select cascade level 1
        # 20 : 2 * 8 + 0 = 16 bits = 2 bytes transmitted
        # No CRC
        data = [0x93, 0x20]
        self.commentData("Select cascade level 1:", data)
        resp = self.__drv.send_raw(data = data, resp_len = 5)
        self.commentData("Select cascade level 1 response:", resp)

        # resp : CT + UID (3 bytes) + BCC
        # 93 : Select cascade level 1
        # 70 : 7 * 8 + 0 = 56 bits  = 7 bytes transmitted
        # 4 bytes : CT + UID
        # CRC_A (2 bytes)
        uid1 = resp
        data = [0x93, 0x70] + uid1
        self.commentData("Select cascade level 1:", data)
        resp = self.__drv.send_raw(data = data, resp_len = 3, crc_in_cmd=False)
        self.commentData("Select cascade level 1 response:", resp)

        if uid1[0] == 0x88:

            # resp : SAK + CRC_A
            # Cascade bit set? => UID not complete
            if resp[0] & 0x04:
                # 95 : Select cascade level 2 (SEL)
                # 20 : 2 * 8 + 0 = 16 bits = 2 bytes transmitted
                # No CRC
                data = [0x95, 0x20]
                self.commentData("Select cascade level 2:", data)
                resp = self.__drv.send_raw(data = data, resp_len = 5)
                self.commentData("Select cascade level 2 response:", resp)

                # resp : 4 bytes (UID) (+BCC not see in this implementation)
                # 95 : Select cascade level 2 (SEL)
                # 70 : 7 * 8 + 0 = 56 bits  = 7 bytes transmitted
                # No CRC
                uid2 = resp
                data = [0x95, 0x70] + uid2
                self.commentData("Select cascade level 2:", data)
                resp = self.__drv.send_raw(data = data, resp_len = 3, crc_in_cmd=False)
                self.commentData("Select cascade level 2 response:", resp)

                # resp : SAK + CRC_A
                # Cascade bit set? => UID not complete
                if resp[0] & 0x04:
                    # 97 : Select cascade level 3 (SEL)
                    # 20 : 2 * 8 + 0 = 16 bits = 2 bytes transmitted
                    # No CRC
                    # resp = self.hf14a_raw(data = "9720", leaveSigOnAfterRec= True, fieldMode = "OnWithoutSelect")
                    self.__logger.info("Select cascade level 3")
                    resp = self.__drv.send_raw(data = [0x97, 0x20], resp_len = 3)

                    # resp : 4 bytes (UID) + BCC
                    # 97 : Select cascade level 32 (SEL)
                    # 70 : 7 * 8 + 0 = 56 bits  = 7 bytes transmitted
                    # No CRC
                    uid2 = resp
                    # resp = self.hf14a_raw(data = "9770" + resp, leaveSigOnAfterRec= True, fieldMode = "OnWithoutSelect", AutoAddCRC = True)
                    self.__logger.info("Select cascade level 3")
                    resp = self.__drv.send_raw(data = [0x97, 0x70] + resp, resp_len = 3, crc_in_cmd=False)

        # RATS (Request Answer To Select)
        resp = self.sendRATS_A(FSDI, CID)
        return (uid1 + uid2 + uid3, resp)


    def sendRATS_A(self, FSDI = "0", CID = "0"):
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
        dico  = { "0" : 16, "1" : 24, "2" : 32, "3" : 40, "4" : 48, "5" : 64, "6" : 96, "7" : 128, "8" : 256}
        self.__logger.info("Request for Answer To Select (RATS):")
        self.__logger.info("\tPCD selected options:")
        self.__logger.info("\t\tFSDI : 0x%s => max PCD frame size : %d bytes" % ( FSDI, dico[FSDI]))
        self.__logger.info("\t\tCID  : 0x%s" % FSDI)

        data = [0xE0, int(FSDI + CID, 16)]
        self.commentData("RATS", data)
        resp = self.__drv.send_raw(data = data, resp_len = 20, crc_in_cmd=False)


        # resp[0] = TL = length without counting the 2 CRC bytes
        resp = resp[:resp[0]+2]
        self.commentData("Answer to Select (ATS = RATS response):", resp)

        T0 = resp[1]
        self.__logger.info("\tT0 : 0x%02X", T0)
        self.__logger.info("\t\tFSCI : 0x%01X => max card frame size : %d bytes" % (T0 & 0xF, dico[str(T0& 0xF)]))
        ta1 = None
        tb1 = None
        tc1 = None
        cmpt = 2
        if T0 & 0x10:
            self.__logger.info("\t\tTA(1) present")
            ta1 = resp[cmpt]
            cmpt += 1
        if T0 & 0x20:
            self.__logger.info("\t\tTB(1) present")
            tb1 = resp[cmpt]
            cmpt += 1
        if T0 & 0x40:
            self.__logger.info("\t\tTC(1) present")
            tc1 = resp[cmpt]
            cmpt += 1

        if ta1:
            self.__logger.info("\tTA(1) : 0x%02X" % ta1)
            self.__logger.info("\t\tInterpretation : TODO...")
        if tb1:
            self.__logger.info("\tTB(1) : 0x%02X" % tb1)
            self.__logger.info("\t\tInterpretation : TODO...")
        if tc1:
            self.__logger.info("\tTC(1) : 0x%02X" % tc1)
            self.__addNAD = ((tc1 & 0x01) == 0x01)
            self.__logger.info("\t\tNAD %ssupported" % ( ( not self.__addNAD) * "not "))
            self.__addCID = ((tc1 & 0x02) == 0x02)
            self.__logger.info("\t\tCID %ssupported" % ( ( not self.__addCID) * "not "))
        self.__logger.info("\tHistorical bytes : %s" % utils.int_array_to_hex_str(resp[cmpt:-2]))
        self.__logger.info("\tCRC : %s" % utils.int_array_to_hex_str(resp[-2:]))

        self.__logger.info("")
        self.__logger.info("")
        self.__logger.info("")
        return resp

    def send_pps(self, CID = 0x0, PPS1 = False, DRI = 0x0, DSI = 0x0):
        """

        :param CID:
        :param DRI:
        :param DSI:
        :return:
        """
        self.__logger.info("PPS")
        self.__logger.info("\tPCD selected options:")
        PPS0_PPS1 = [0x01]
        if PPS1:
            PPS0_PPS1.append(DRI << 4 + DSI)
        self.__logger.info("\tCID : 0x%X" % CID)
        self.__logger.info("\tPPS1 %stransmitted" % ("not " * (not PPS1)))

        data = [ 0xD0 + CID]
        self.commentData("PPS:", data)
        resp =  self.__drv.send_raw(data = data + PPS0_PPS1, resp_len = 3, crc_in_cmd=False)
        self.commentData("PPS response:", resp)
        if resp[0] == (0xD0 + CID):
            self.__logger.info("\tPPS accepted")
        else:
            self.__logger.info("\tPPS rejected")
        self.__logger.info("")

        return resp



    def __initPCB_BlockNumber(self):
        self.__PCB_BlockNumber = 0
    
    def __incPCB_BlockNumber(self):
        self.__PCB_BlockNumber ^=  1
    
    def __getPCB_BlockNumber(self):
        return self.__PCB_BlockNumber

    def __getAndUpdatePCB_BlockNumber(self):
        nb = self.__getPCB_BlockNumber()
        self.__incPCB_BlockNumber()
        return nb

    def get_rblock(self, ack = True, cid = True, block_number = None):

        pcb = 0xA2
        cid = ""
        if not ack:
            pcb |= 0x10

        if cid:
            pcb |= 0x08
            cid = " 0x%02X " % self.__CID

        if block_number:
            pcb |= block_number
        else:
            pcb |= self.get_and_update_iblock_pcb_number()

        if cid != "":
            return [pcb, cid]
        else:
            return [pcb]


    def getIBlock(self, data, chaining_bit = False):
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
        pcb =  self.get_and_update_iblock_pcb_number() + 0x02

        cid = ""
        if self.__addCID:
            cid = self.__CID
            pcb |= 0x08

        if chaining_bit:
            pcb |= 0x10

        nad = ""
        if self.__addNAD:
            nad = self.__NAD
            pcb |= 0x04

        header = [pcb]
        if nad != "":
            header.append(nad)
        if cid != "":
            header.append(cid)

        return header + data

    def chaining_iblock(self, data = None, block_size = None):

        if not block_size:
            block_size = self.get_block_size()

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
        self.__logger.info("\t\t" + "TPDU command:")
        for hit in utils.get_pretty_print_block(tpdu):
            self.__logger.info("\t\t" + hit)

        resp = self.__drv.send_raw(data = tpdu, resp_len = 16, crc_in_cmd=False)

        resp = Tpdu(resp)
        self.__logger.info("\t\t" + "TPDU response:")
        for hit in utils.get_pretty_print_block(resp.get_tpdu()):
            self.__logger.info("\t\t" + hit)
        return resp


    def send_apdu(self, apdu):
        apdu = self.convert_data(apdu)
        self.__logger.info("APDU command:")
        for hit in utils.get_pretty_print_block(apdu):
            self.__logger.info("\t" + hit)

        block_lst = self.chaining_iblock(data = apdu)
        resp_block_lst = []

        if len(block_lst) == 1:
            resp = self._send_tpdu(block_lst[0])

        else:
            self.__logger.info("Block chaining, %d blocks to send" % len(block_lst))
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

        self.__logger.info("APDU response:")
        for hit in utils.get_pretty_print_block(rapdu):
            self.__logger.info("\t" + hit)
        return rapdu

    def commentData(self, msg, data):
        self.__logger.info(msg)
        for hit in utils.get_pretty_print_block(data):
            self.__logger.info("\t" + hit)

    def convert_data(self, data):
        assert(isinstance(data, str))
        data = data.upper().strip().replace(" ", "")
        assert( (len(data) % 2) == 0 )
        convert = []
        for hit in range(0, len(data), 2):
            convert.append( int(data[hit:hit+2], 16) )
        return convert