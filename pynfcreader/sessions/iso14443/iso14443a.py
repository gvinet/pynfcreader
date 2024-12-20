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
from pynfcreader.tools import utils


class Iso14443ASession(Iso14443Session):

    def __init__(self, cid=0, nad=0, drv=None, block_size=16):
        Iso14443Session.__init__(self, cid, nad, drv, block_size)

    def connect(self):
        self._drv.connect()
        self._drv.set_mode_iso14443A()

    def polling(self):
        self.send_reqa()
        self.send_select_full()
        self.send_pps()

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

    def send_select_full(self, fsdi="0", cid="0", do_rats=True):
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
        if do_rats:
            # RATS (Request Answer To Select)
            resp = self.send_rats_a(fsdi, cid)
        else:
            None
        return uid1 + uid2 + uid3, resp

    def send_rats_a(self, fsdi="0", cid="0"):
        """
        Request for answer to select - Type A
        0xE0 - fsdi | cid - CRC_A
        :param fsdi: defines the maximum size of a frame the PCD is able to receive.
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
        :param cid: logical number of the addressed PICC in the range from 0 to 14.
        :return: ATS (Answer to select)
        """
        dico = {"0": 16, "1": 24, "2": 32, "3": 40, "4": 48, "5": 64, "6": 96, "7": 128, "8": 256}
        self._logger.info("Request for Answer To Select (RATS):")
        self._logger.info("\tPCD selected options:")
        self._logger.info("\t\tFSDI : 0x%s => max PCD frame size : %d bytes" % (fsdi, dico[fsdi]))
        self._logger.info("\t\tCID  : 0x%s" % fsdi)

        data = bytes([0xE0, int(fsdi + cid, 16)])
        self.comment_data("RATS", data)
        resp = self._drv.write(data=data, resp_len=20, transmitter_add_crc=True)

        # resp[0] = TL = length without counting the 2 CRC bytes
        resp = resp[:resp[0] + 2]
        self.comment_data("Answer to Select (ATS = RATS response):", resp)

        t0 = resp[1]
        self._logger.info("\tT0 : 0x%02X", t0)
        self._logger.info("\t\tFSCI : 0x%01X => max card frame size : %d bytes" % (t0 & 0xF, dico[str(t0 & 0xF)]))
        ta1 = None
        tb1 = None
        tc1 = None
        cmpt = 2
        if t0 & 0x10:
            self._logger.info("\t\tTA(1) present")
            ta1 = resp[cmpt]
            cmpt += 1
        if t0 & 0x20:
            self._logger.info("\t\tTB(1) present")
            tb1 = resp[cmpt]
            cmpt += 1
        if t0 & 0x40:
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
