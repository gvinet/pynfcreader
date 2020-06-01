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


import re

manufacturer_codes_iso_7816_6 = {
    "01": "Motorola",
    "02": "ST Microelectronics",
    "03": "Hitachi",
    "04": "NXP Semiconductors",
    "05": "Infineon Technologies",
    "06": "Cylinc",
    "07": "Texas Instruments Tag-it",
    "08": "Fujitsu Limited",
    "09": "Matsushita Electric Industrial",
    "0A": "NEC",
    "0B": "Oki Electric",
    "0C": "Toshiba",
    "0D": "Mitsubishi Electric",
    "0E": "Samsung Electronics",
    "0F": "Hyundai Electronics",
    "10": "LG Semiconductors",
    "16": "EM Microelectronic-Marin",
    "1F": "Melexis",
    "2B": "Maxim",
    "33": "AMIC"}


def int_array_to_hex_str(array):
    return " ".join(f"{hit:02X}" for hit in array)


def bytes_to_ascii_printable_str(data):
    data = data.decode(encoding='ascii', errors='replace')
    return re.sub(r'[^\x20-\x7E]', '.', data)


def bytes_to_str(data_b):
    return ' '.join(f'{hit:02X}' for hit in data_b)


def get_pretty_print_block(msg):
    lst = []

    for hit in range(0, len(msg), 16):
        block1 = msg[hit:hit + 8]
        hex1 = " ".join(f"{c:02X}" for c in block1)
        str1 = bytes_to_ascii_printable_str(block1)
        block2 = msg[hit + 8:hit + 16]
        hex2 = " ".join(f"{c:02X}" for c in block2)
        str2 = bytes_to_ascii_printable_str(block2)

        lpart = f"{hex1}   {hex2}"
        lst.append(f'{lpart}{" " * (49 - len(lpart))}      {str1}   {str2}')
    return lst
