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

from pynfcreader.sessions.iso15693.requests import \
    RequestInventory, \
    RequestReadSingleBlock, \
    RequestReadMultipleBlocks, \
    RequestGetSystemInformation, \
    RequestStayQuiet, \
    RequestWriteSingleBlock, \
    RequestWriteMultipleBlock, \
    RequestSelect, \
    RequestGetMultipleBlockSecurityStatus
from pynfcreader.tools import utils


class Iso15693Session(object):

    def __init__(self, drv=None):
        self._drv = drv
        self._logger = self._drv.get_logger()
        self.last_request = None
        self._memory_block = {}
        self._lock_status = {}

    def connect(self):
        self._drv.connect()
        self._drv.set_mode_iso15693()

    def field_on(self):
        self._logger.info("field on")
        self._drv.field_on()
        self._logger.info("")

    def field_off(self):
        self._logger.info("field off")
        self._drv.field_off()
        self._logger.info("")

    def send(self, cmd):

        return self._drv.write(data=cmd, resp_len=16, transmitter_add_crc=True)

    def send_cmd(self, cmd, no_answer=False):
        self._logger.info(f"Command {cmd.name}")

        for hit in utils.get_pretty_print_block(cmd()):
            self._logger.info(f"{hit}")

        for key, value in cmd.items.items():
            if value != b"":
                self._logger.info(f"\t{key:20}: {utils.bytes_to_str(value)}")
        self._logger.info("")

        resp = self.send(cmd())

        self.last_request = cmd

        if no_answer:
            return

        self._logger.info("Response:")
        if resp:
            for hit in utils.get_pretty_print_block(resp):
                self._logger.info(hit)
        else:
            self._logger.info("")
        try:
            cmd.resp_pretty_print(resp)
        except:  # noqa: E722
            pass
        for key, value in cmd.resp.items():
            if value != b"":
                self._logger.info(
                    f"\t{key:25}: {utils.bytes_to_str(value['raw'])}")
                if value["pretty"] != "":
                    self._logger.info(f"\t{' ' * 25}: {value['pretty']}")
        self._logger.info("")

        return resp

    def inventory(self, flags=b"\x26", afi_opt=b"", mask=b""):
        return self.send_cmd(RequestInventory(flags, afi_opt, mask))

    def stay_quiet(self, flags=b"\x22", uid=b""):
        return self.send_cmd(RequestStayQuiet(flags, uid), no_answer=True)

    def read_single_block(self, flags=b"\x42", uid_opt=b"", block_nb=b""):
        return self.send_cmd(RequestReadSingleBlock(flags, uid_opt, block_nb))

    def write_single_block(self, flags=b"\x42", uid_opt=b"", block_nb=b"",
                           data=b""):
        return self.send_cmd(
            RequestWriteSingleBlock(flags, uid_opt, block_nb, data))

    def get_system_info(self, flags=b"\x22", uid_opt=b""):
        return self.send_cmd(RequestGetSystemInformation(flags, uid_opt))

    def read_multiple_blocks(self, flags=b"\x42", uid_opt=b"",
                             first_block_nb=b"\x00", nb_blocks=b"\x00"):
        return self.send_cmd(
            RequestReadMultipleBlocks(flags, uid_opt, first_block_nb,
                                      nb_blocks))

    def write_multiple_block(self, flags=b"\x02", uid_opt=b"",
                             first_block_nb=b"\x00", nb_blocks=b"\x00",
                             data=b""):
        return self.send_cmd(
            RequestWriteMultipleBlock(flags, uid_opt, first_block_nb, nb_blocks,
                                      data))

    def select(self, flags=b"\x22", uid=b""):
        return self.send_cmd(RequestSelect(flags, uid))

    def get_multiple_blocks_security_status(self, flags=b"\x02", uid_opt=b"",
                                            first_block_nb=b"\x00",
                                            nb_blocks=b"\x00"):
        return self.send_cmd(
            RequestGetMultipleBlockSecurityStatus(flags, uid_opt,
                                                  first_block_nb, nb_blocks))

    def get_all_auto(self):
        uid = self.inventory()[2:][::-1]
        self.get_system_info(uid_opt=uid)
        nb_block = self.last_request.nb_block
        self.get_all_memory_info(nb_block)

        self._logger.info("\tMemory dump")
        self._logger.info("")

        for hit in range(nb_block):
            block = utils.int_array_to_hex_str(self._memory_block[hit])
            block_ascii = utils.bytes_to_ascii_printable_str(
                self._memory_block[hit])
            status = "Locked  " if (
                    self._lock_status[hit][0] & 0x1) else "Unlocked"
            self._logger.info(
                f"\t\t[{hit:3d}] - {status} -  {block} | {block_ascii}")

    def get_all_memory_info(self, block_num):
        self._logger.info("Get and print all memory")

        self._memory_block = {}
        self._lock_status = {}

        self._logger.info("\tGet all memory")
        for hit in range(block_num):
            block_nb = bytes([hit])
            resp = self.read_single_block(block_nb=block_nb)[2:]
            if len(resp) == 0:
                self.read_single_block(block_nb=block_nb)[2:]
            self._memory_block[hit] = self.last_request.resp["data"]["raw"]
            self._lock_status[hit] = \
                self.last_request.resp["block_security_status"]["raw"]
