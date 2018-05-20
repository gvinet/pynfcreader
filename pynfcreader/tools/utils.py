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

import string
import sys
import re

def int_array_to_hex_str(array):
    return " ".join(("%02X" % hit) for hit in array)

def hex_str_to_ascii_printable_str(data):
    if sys.version[0] == '2':
        msg = ""
        printable_lst = string.ascii_letters + string.digits + string.punctuation
        for hit in data.replace(" ", "").decode("hex"):
            if hit in printable_lst:
                msg += hit
            else:
                msg += "."
        return msg
    else:
        data = bytes.fromhex(data).decode(encoding='ascii', errors='replace')
        return re.sub(r'[^\x20-\x7E]', '.', data)

def get_pretty_print_block(msg):

    lst = []

    for hit in range(0,len(msg), 16):
        block1 = msg[hit:hit+8]
        hex1 = int_array_to_hex_str(block1)
        str1 = hex_str_to_ascii_printable_str(hex1)
        block2 = msg[hit+8:hit+16]
        hex2 = int_array_to_hex_str(block2)
        str2 = hex_str_to_ascii_printable_str(hex2)

        lpart = hex1 + "   " + hex2
        lst.append("\t" + lpart + " " * ( 49 - len(lpart) ) +  "      "  + str1 + "   " + str2)
    lst.append("")
    return lst