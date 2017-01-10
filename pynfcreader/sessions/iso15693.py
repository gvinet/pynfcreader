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

class Iso15693Session(object):

    #https://en.wikipedia.org/wiki/ISO/IEC_15693
    #ISO/IEC 7816-6
    Manufacturer_codes = {
        "01" : "Motorola",
        "02" : "ST Microelectronics",
        "03" : "Hitachi",
        "04" : "NXP Semiconductors",
        "05" : "Infineon Technologies",
        "06" : "Cylinc",
        "07" : "Texas Instruments Tag-it",
        "08" : "Fujitsu Limited",
        "09" : "Matsushita Electric Industrial",
        "0A" : "NEC",
        "0B" : "Oki Electric",
        "0C" : "Toshiba",
        "0D" : "Mitsubishi Electric",
        "0E" : "Samsung Electronics",
        "0F" : "Hyundai Electronics",
        "10" : "LG Semiconductors",
        "16" : "EM Microelectronic-Marin",
        "1F" : "Melexis",
        "2B" : "Maxim",
        "33" : "AMIC"}

    # IC_Reference = { "04" : { "01" : }}

    def __init__(self, CID = 0, NAD = 0, drv = None, block_size = 16):
        self.__drv = drv
        self.__driver = drv
        self.__logger = self.__driver.getLogger()

    def send(self, cmd):
        cmd = self.convert_data(cmd)
        self.__logger.info("Command:")
        for hit in utils.get_pretty_print_block(cmd):
            self.__logger.info("\t" + hit)

        resp = self.__drv.send_raw(data = cmd, resp_len = 16, crc_in_cmd=False)

        self.__logger.info("Response:")
        if resp:
            for hit in utils.get_pretty_print_block(resp):
                self.__logger.info("\t" + hit)
        else:
            self.__logger.info("")
        return resp

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

    def inventory(self):
        self.__logger.info("Inventory")
        resp = self.send("26 01 00")
        self._uid = utils.int_array_to_hex_str(list(reversed(resp[2:10])))
        self._uid_rev = utils.int_array_to_hex_str(resp[2:])
        self.__logger.info("")
        return resp

    def get_system_info(self, uid):
        self.__logger.info("Get System Info")
        resp = self.send("22 2B" + uid)
        self.get_system_info_resp_pretty_print(self.get_system_info_resp_parser(resp))
        self.__logger.info("")
        return resp

    def read_single_block(self, block_number):
        self.__logger.info("Read Single Block %s" % block_number)
        resp = self.send("42 20" + block_number)
        # self.get_system_info_resp_pretty_print(self.get_system_info_resp_parser(resp))
        self.__logger.info("")
        return resp

    def write_single_block(self, block_number, data):
        self.__logger.info("Write Single Block %s : %s" % (block_number, data))
        resp = self.send("43 21" + block_number + data)
        self.__logger.info("")
        return resp

    def get_block_security_status(self, uid, first_block_number, block_number):
        self.__logger.info("Get block security status - first_block_number %s - number of block to read %d" % (first_block_number, int(block_number,16) +1 ))
        resp = self.send("22 2C" + uid + first_block_number + block_number)
        self.__logger.info("")
        return resp

    def get_system_info_resp_parser(self, resp):
        parsing = {}
        parsing["UID"]      = utils.int_array_to_hex_str(list(reversed(resp[2:10])))
        parsing["DSFID"]    = utils.int_array_to_hex_str(resp[10:11])
        parsing["AFI"]      = utils.int_array_to_hex_str(resp[11:12])
        mem_size = resp[12:14]
        block_size = (mem_size[1] & 0x1F) + 1
        parsing["MEM_SIZE_BLOCK_SIZE"] = block_size
        self._block_num  = mem_size[0] + 1

        parsing["MEM_SIZE_BLOCK_NB"] = self._block_num
        full_mem_size = block_size * self._block_num
        parsing["MEM_SIZE_PRETTY_PRINT"] = "%d bytes : %d blocks of %d bytes (%s)" % (full_mem_size, self._block_num, block_size, utils.int_array_to_hex_str(resp[12:14]))
        ic_ref = utils.int_array_to_hex_str(resp[14:15])
        parsing["IC_REF"] = "%s (%s)" % (self.Manufacturer_codes[ic_ref], ic_ref)

        self._get_sys_info_resp = parsing

        return parsing

    def get_system_info_resp_pretty_print(self, resp_parsing):
        self.__logger.info("\tUID..........: %s" % resp_parsing["UID"])
        self.__logger.info("\tDSFID........: %s" % resp_parsing["DSFID"])
        self.__logger.info("\tAFI..........: %s" % resp_parsing["AFI"])
        self.__logger.info("\tMemory size..: %s" % resp_parsing["MEM_SIZE_PRETTY_PRINT"])
        self.__logger.info("\tIC Reference.: %s" % resp_parsing["IC_REF"])

    def get_all_auto(self):
        self.inventory()
        self.get_system_info(self._uid_rev)
        resp = self.get_all_memory_info()

        self.__logger.info("\tMemory dump")
        self.__logger.info("")
        self.get_system_info_resp_pretty_print(self._get_sys_info_resp)

        for cmpt, hit in enumerate(["%02X" % hit for hit in range(self._block_num)]):
            block = utils.int_array_to_hex_str(self._memory_block[hit])
            block_ascii = utils.hex_str_to_ascii_printable_str(block)
            status = "Locked  " if (self._lock_status[cmpt] & 0x1) else "Unlocked"
            self.__logger.info("\t\t[%s] - %s -  %s | %s" % (hit, status, block, block_ascii))

    def get_all_memory_info(self, block_num = None):
        self.__logger.info("Get and print all memory")

        if not block_num:
            block_num = self._block_num

        self._memory_block = {}

        self.__logger.info("\tGet all memory")
        for hit in ["%02X" % hit for hit in range(block_num)]:
            resp = self.read_single_block(hit)[2:]
            self._memory_block[hit] = resp

        self.__logger.info("\tGet lock status")
        self._lock_status = self.get_block_security_status(self._uid_rev, "00", "%02X" % (block_num - 1))[1:]


