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

import collections
from pynfcreader.tools.utils import manufacturer_codes_iso_7816_6


class Request(object):
    cmd = {b"\x01": "Inventory",
           b"\x02": "Stay quiet",
           b"\x20": "Read single block",
           b"\x21": "Write single block",
           b"\x23": "Read multiple blocks",
           b"\x24": "Write multiple blocks",
           b"\x25": "Select",
           b"\x26": "Reset to ready",
           b"\x2B": "Get system information",
           b"\x2C": "Get multiple block security status"}

    error_code_def = {1: "The command is not supported, i.e. the request code is not recognised.",
                      2: "The command is not recognised, for example: a format error occurred.",
                      3: "The option is not supported.",
                      4: "Unknown error.",
                      5: "The specified block is not available (doesn’t exist).",
                      6: "The specified block is already -locked and thus cannot be locked again",
                      0xF: "Unknown error.",
                      0x10: "The specified block is not available (doesn’t exist).",
                      0x11: "The specified block is already -locked and thus cannot be locked again",
                      0x12: "The specified block is locked and its content cannot be changed.",
                      0x13: "The specified block was not successfully programmed.",
                      0x14: "The specified block was not successfully locked."}

    def __init__(self, **kwargs):

        self.items = collections.OrderedDict(kwargs)
        self.name = self.cmd[kwargs["command"]]
        self.resp = collections.OrderedDict()

    def get_error_code(self, error_code):
        if error_code == 0:
            return "No error"

        if error_code in self.error_code_def.keys():
            return self.error_code_def[error_code]

        if error_code in range(0xA0, 0xE0):
            return "Custom command error codes"

        return "DFU"

    def get_pretty_security_status(self, status):
        return 'Locked' if status[0] == 1 else 'Unlocked'

    def pretty_print_request_info_flags(self, info_flags):
        info_flags_pretty = collections.OrderedDict({"DSFID": {0: "DSFID is not supported. DSFID field is not present",
                                                               1: "DSFID is supported. DSFID field is present"},
                                                     "AFI": {0: "AFI is not supported. AFI field is not present",
                                                             1: "AFI is supported. AFI field is present"},
                                                     "VICC memory size": {
                                                         0: "Information on VICC memory s ize is not supported. Memory size field is not present.",
                                                         1: "Information on VICC memory s ize is supported. Memory size field is present."},
                                                     "IC reference": {0: "Information on IC reference is not supported. IC reference field is not present.",
                                                                      1: "Information on IC reference is supported. IC reference field is present."}})

        pretty = ""
        bit = 0
        for key in info_flags_pretty.keys():
            pretty += f"{info_flags_pretty[key][(info_flags >> bit) & 1]}\n"
        return pretty

    def pretty_print_request_flags(self, flag):
        info = collections.OrderedDict()
        request_flags_b1_to_b4 = {"Sub-carrier_flag": {0: "A single sub-carrier frequency shall be used by the VICC",
                                                       1: "Two sub-carriers shall be used by the VICC"},
                                  "Data_rate_flag": {0: "Low data rate shall be used",
                                                     1: "High data rate shall be used"},
                                  "Inventory_flag": {0: "Inventory flag off",
                                                     1: "Inventory flag on"},
                                  "Protocol_Extension_flag": {0: "No protocol format extension",
                                                              1: "Protocol format is extended. Reserved for future use"}}

        request_flags_b5_to_b8_inventory = {"AFI_flag": {0: "AFI field is not present",
                                                         1: "AFI field is present"},
                                            "Nb_slots_flag": {0: "16 slots",
                                                              1: "1 slots"},
                                            "Option_flag": {
                                                0: "Meaning is defined by the command description. It shall be set to 0 if not otherwise defined by the command.",
                                                1: "Meaning is defined by the command description."},
                                            "RFU": {0: "Shall be set to 0.",
                                                    1: "Shall be set to 0."}}

        request_flags_b5_to_b8_no_inventory = {"Select_flag": {0: "Request shall be executed by any VICC according to the setting of Address_flag",
                                                               1: "Request shall be executed only by VICC in selected state"},
                                               "Address_flag": {0: "Request is not addressed. UID field is not present. It shall be executed by any VICC.",
                                                                1: "Request is addressed. UID field is present. It shall be executed only by the VICC whose UID matches the UID specified in the request."},
                                               "Option_flag": {
                                                   0: "Meaning is defined by the command description. It shall be set to 0 if not otherwise defined by the command.",
                                                   1: "Meaning is defined by the command description."},
                                               "RFU": {0: "Shall be set to 0.",
                                                       1: "Shall be set to 0."}}

        # for bit in range(4):
        #     print(f"{key:20}: {' '.join(f'{hit:02X}' for hit in value)}")

    def cmd_pretty_print(self):
        for key, value in self.items.items():
            if value != b"":
                print(f"{key:20}: {' '.join(f'{hit:02X}' for hit in value)}")

    def resp_pretty_print(self, resp=b""):
        flags = resp[0:1]
        self.resp["flags"] = {"raw": flags,
                              "pretty": f"{self.get_error_code(flags)} ({flags:02X})"}

        # Error flag?
        if resp[0] & 1:
            error_code = resp[1:2]
            self.resp["error_code"] = {"raw": error_code,
                                       "pretty": f"{self.get_error_code(error_code)} ({error_code:02X})"}

    def __call__(self):
        return b"".join(hit for hit in self.items.values() if hit != b"")


class RequestInventory(Request):

    def __init__(self, flags=b"\x00", afi_opt=b"", mask_opt=b""):
        Request.__init__(self,
                         flags=flags,
                         command=b"\x01",
                         afi_opt=afi_opt,
                         mask_len=bytes([len(mask_opt)]),
                         mask_opt=mask_opt)

    def resp_pretty_print(self, resp=b""):
        flags = resp[0:1]
        self.resp["flags"] = {"raw": flags,
                              "pretty": f"0x{flags[0]:02X}"}
        dsfid = resp[1:2]
        self.resp["dsfid"] = {"raw": dsfid,
                              "pretty": f"0x{dsfid[0]:02X}"}

        uid = resp[2:10]
        self.resp["uid"] = {"raw": uid,
                            "pretty": " ".join(f"{hit:02X}" for hit in resp[2:10][::-1])}


class RequestStayQuiet(Request):

    def __init__(self,
                 flags=b"\x00",
                 uid=b""):
        Request.__init__(self,
                         flags=flags,
                         command=b"\x02",
                         uid=uid)


class RequestReadSingleBlock(Request):

    def __init__(self,
                 flags=b"\x00",
                 uid_opt=b"",
                 block_nb=b""):
        Request.__init__(self,
                         flags=flags,
                         command=b"\x20",
                         uid_opt=uid_opt,
                         block_nb=block_nb)

    def resp_pretty_print(self, resp=b""):
        flags = resp[0:1]
        self.resp["flags"] = {"raw": flags,
                              "pretty": f"0x{flags[0]:02X}"}

        # Error flag?
        if resp[0] & 1:
            error_code = resp[1:2]
            self.resp["flags"] = {"raw": error_code,
                                  "pretty": f"{self.get_error_code(error_code[0])} ({error_code[0]:02X})"}
        else:
            if self.items["flags"][0] & 0x40:
                self.resp["block_security_status"] = resp[1:2]
                block_security_status = resp[1:2]
                self.resp["block_security_status"] = {"raw": block_security_status,
                                                      "pretty": f"{self.get_pretty_security_status(block_security_status)} ({block_security_status[0]:02X})"}
            self.resp["data"] = {"raw": resp[2:],
                                 "pretty": ""}


class RequestWriteSingleBlock(Request):

    def __init__(self,
                 flags=b"\x00",
                 uid_opt=b"",
                 block_nb=b"",
                 data=b""):
        Request.__init__(self,
                         flags=flags,
                         command=b"\x21",
                         uid_opt=uid_opt,
                         block_nb=block_nb,
                         data=data)


class RequestReadMultipleBlocks(Request):

    def __init__(self,
                 flags=b"\x00",
                 uid_opt=b"",
                 first_block_nb=b"\x00",
                 nb_blocks=b"\x00"):
        Request.__init__(self,
                         flags=flags,
                         command=b"\x23",
                         uid_opt=uid_opt,
                         first_block_nb=first_block_nb,
                         nb_blocks=nb_blocks)

        if uid_opt:
            self.items["uid_opt"] = uid_opt
        self.items["first_block_nb"] = first_block_nb
        self.items["nb_blocks"] = nb_blocks

    def resp_pretty_print(self, resp=b""):
        flags = resp[0:1]
        self.resp["flags"] = {"raw": flags,
                              "pretty": f"0x{flags[0]:02X}"}

        # Error flag?
        if resp[0] & 1:
            error_code = resp[1:2]
            self.resp["flags"] = {"raw": error_code,
                                  "pretty": f"{self.get_error_code(error_code[0])} ({error_code[0]:02X})"}
        else:
            nb_blocks = self.items["nb_blocks"][0] + 1
            chunk_size = len(resp[1:]) // nb_blocks
            if self.items["flags"][0] & 0x40:
                chunk_size -= 1
            cmpt = 2
            for hit in range(nb_blocks):
                if self.items["flags"][0] & 0x40:
                    block_security_status = resp[cmpt:cmpt + 1]
                    cmpt += 1
                    pretty = f"{self.get_pretty_security_status(block_security_status)} ({block_security_status[0]:02X})"
                    self.resp[f"block_security_status {hit}"] = {"raw": block_security_status,
                                                                 "pretty": pretty}
                data = resp[cmpt:cmpt + chunk_size]
                self.resp[f"block {hit}"] = {"raw": data,
                                             "pretty": b" ".join(f"{hit:02X}" for hit in data)}
                cmpt += chunk_size


class RequestWriteMultipleBlock(Request):

    def __init__(self,
                 flags=b"\x00",
                 uid_opt=b"",
                 first_block_nb=b"\x00",
                 nb_blocks=b"\x00",
                 data=b""):
        Request.__init__(self,
                         flags=flags,
                         command=b"\x24",
                         uid_opt=uid_opt,
                         first_block_nb=first_block_nb,
                         nb_blocks=nb_blocks,
                         data=data)


class RequestSelect(Request):

    def __init__(self,
                 flags=b"\x00",
                 uid=b""):
        Request.__init__(self,
                         flags=flags,
                         command=b"\x25",
                         uid=uid)


class RequestResetToReady(Request):

    def __init__(self,
                 flags=b"\x00",
                 uid_opt=b""):
        Request.__init__(self,
                         flags=flags,
                         command=b"\x25",
                         uid_opt=uid_opt)


class RequestGetMultipleBlockSecurityStatus(Request):

    def __init__(self,
                 flags=b"\x00",
                 uid_opt=b"",
                 first_block_nb=b"\x00",
                 nb_blocks=b"\x00"):
        Request.__init__(self,
                         flags=flags,
                         command=b"\x2C",
                         uid_opt=uid_opt,
                         first_block_nb=first_block_nb,
                         nb_blocks=nb_blocks)

    def resp_pretty_print(self, resp=b""):
        flags = resp[0:1]
        self.resp["flags"] = {"raw": flags,
                              "pretty": f"0x{flags[0]:02X}"}

        # Error flag?
        if resp[0] & 1:
            error_code = resp[1:2]
            self.resp["flags"] = {"raw": error_code,
                                  "pretty": f"{self.get_error_code(error_code[0])} ({error_code[0]:02X})"}
        else:
            nb = self.items["nb_blocks"][0] + 1
            for hit in range(1, len(resp)):
                block_security_status = resp[hit:hit + 1]
                pretty = f"{self.get_pretty_security_status(block_security_status)} ({block_security_status[0]:02X})"
                self.resp[f"block_security_status {nb}"] = {"raw": block_security_status,
                                                            "pretty": pretty}
                nb += 1


class RequestGetSystemInformation(Request):

    def __init__(self, flags=b"\x00", uid_opt=b""):
        Request.__init__(self,
                         flags=flags,
                         command=b"\x2B",
                         uid_opt=uid_opt[::-1])

        self.nb_block = None
        self.block_byte_size = None
        self.ic_reference = None

    def resp_pretty_print(self, resp=b""):
        flags = resp[0:1]
        self.resp["flags"] = {"raw": flags,
                              "pretty": f"0x{flags[0]:02X}"}

        # Error flag?
        if resp[0] & 1:
            error_code = resp[1:2]
            self.resp["flags"] = {"raw": error_code,
                                  "pretty": f"{self.get_error_code(error_code[0])} ({error_code[0]:02X})"}
        else:
            info_flags = resp[1:2]
            self.resp["info_flags"] = {"raw": info_flags,
                                       "pretty": self.pretty_print_request_info_flags(info_flags[0])}

            uid = resp[2:10]
            self.resp["uid"] = {"raw": uid,
                                "pretty": " ".join(f"{hit:02X}" for hit in resp[2:10][::-1])}

            cmpt = 10

            if resp[1] & 1:
                dsfid = resp[cmpt:cmpt + 1]
                self.resp["dsfid"] = {"raw": dsfid,
                                      "pretty": " ".join(f"{hit:02X}" for hit in dsfid)}
                cmpt += 1

            if resp[1] & 2:
                afi = resp[cmpt:cmpt + 1]
                self.resp["afi"] = {"raw": afi,
                                    "pretty": " ".join(f"{hit:02X}" for hit in dsfid)}
                cmpt += 1

            if resp[1] & 4:
                vicc_memory_size = resp[cmpt:cmpt + 2]
                self.nb_block = resp[cmpt] + 1
                cmpt += 1
                self.block_byte_size = (resp[cmpt] & 0x1F) + 1
                cmpt += 1

                self.resp["vicc_memory_size"] = {"raw": vicc_memory_size,
                                                 "pretty": f"{self.nb_block} blocks of {self.block_byte_size} bytes"}



            if resp[1] & 8:
                ic_reference = resp[cmpt:cmpt + 1]
                try:
                    ic_reference_pretty = manufacturer_codes_iso_7816_6(ic_reference.hex().upper())
                except:  # noqa: E722
                    ic_reference_pretty = "Unknown code"
                self.resp["ic_reference"] = {"raw": ic_reference,
                                             "pretty": ic_reference_pretty}
