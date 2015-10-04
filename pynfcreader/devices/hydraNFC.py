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

import logging
import serial

from pynfcreader.devices.Devices import Devices


class HydraNFC(Devices):
    """
    [REF_DS_TRF7970A]
        * SLOS743K - AUGUST 2011 - REVISED APRIL
        * Available on www.ti.com

    Chip Status Control         - 0x00 - see Table 6-25, [REF_DS_TRF7970A]
    ISO Control register        - 0x01 - see Table 6-6, [REF_DS_TRF7970A]
    ISO14443 TX Option Register - 0x02 - Table 6-29, [REF_DS_TRF7970A]
    """

    __cmd_ctrl_bit_add = 0x00
    __cmd_ctrl_bit_cmd = 0x80

    def __init__(self, port="C0M8", baudrate=57600, timeout_sec=0.3, debug=True):

        self.__hydrafw_version_supported = "11.02.2015 - [HydraFW v0.5 Beta]"
        self.__version = "0.0.1 - beta"

        self.__port = port
        self.___baudrate = baudrate
        self.__timeout_sect = timeout_sec
        self.__ser = None

        self.__logger = logging.getLogger()
        stream_handler = logging.StreamHandler()
        stream_debug_formatter = logging.Formatter('%(levelname)s  ::  %(message)s')
        stream_handler.setFormatter(stream_debug_formatter)

        self.__logger.setLevel(logging.INFO)
        stream_handler.setLevel(logging.INFO)

        if debug:
            self.__logger.setLevel(logging.DEBUG or logging.INFO)
            stream_handler.setLevel(logging.DEBUG or logging.INFO)

        self.__logger.addHandler(stream_handler)
        self.banner()

    def banner(self):
        self.__logger.info("Hydra NFC python driver version : %s" % self.__version)
        self.__logger.info("\tSupported hydra firmware %s" % self.__hydrafw_version_supported)
        self.__logger.info("\tISO 14443 A only")
        self.__logger.info("\tOnly one card in the field during a transaction (anticollision not yet finished)")
        self.__logger.info("")

    def connect(self):
        self.__logger.info("Connect to HydraNFC")
        self.__logger.info("")
        self.__ser = serial.Serial(self.__port, self.___baudrate, timeout=self.__timeout_sect)

    def getLogger(self):
        return self.__logger

    def reset(self):
        self.__logger.info("Reset HydraNFC")
        self.__logger.info("")
        resp = ["", "", ""]
        while resp[1] != "Invalid command.\r\n":
            resp = self.send("exit\n")

    def send(self, cmd):

        self.__logger.debug("|--- Send cmd : %s" % cmd)
        self.__ser.write(cmd + "\n")
        line = ""
        lines = []
        while line not in [ "> ", "spi2> "]:
            line = self.__ser.readline()
            lines.append(line)
            self.__logger.debug("\t%s" % line.strip())
        lines.append(line)
        self.__logger.debug("\t%s" % line.strip())
        self.__logger.debug("---|")
        self.__logger.debug("")
        return lines

    def configure(self):
        self.__logger.info("Configure HydraNFC")
        self.__logger.info("\tConfigure gpio to communicate with the hydra nfc shield in spi...")
        self.__configure_gpio_spi()
        self.__logger.info("\tConfigure hydra bus spi 2...")
        self.__configure_spi2()
        self.__logger.info("\tReset hydra nfc...")
        self.__reset_hydra_nfc()
        self.__logger.info("")


    def __configure_gpio_spi(self):
        cmd_lst = ["gpio pa3 mode out off",
               "gpio pa2 mode out on",
               "gpio pc0 mode out on",
               "gpio pc1 mode out on",
               "gpio pb11 mode out off",
               "gpio pb11 mode out on"]
        for hit in cmd_lst:
            self.send(hit)

    def __configure_spi2(self):
        """
        We configure the hydrabus spi 2 used by the nfc shield.
        [REF_DS_TRF7970A], chapter 7.2.1 indicates that DATA_CLK line shall be 2Mhz.
        Hydranfc spi 2 clock can be 1.31Mhz, 2.62Mhz and 5.25Mhz. 2.62 works correctly
        If communication error arises, 1.31 shall be used.
        """
        cmd_lst = [ "spi device 2 frequency 2.62mhz polarity 0 phase 1"]
        for hit in cmd_lst:
            self.send(hit)

    def __reset_hydra_nfc(self):
        """
        We reset the TRF7970A chip used by the nfc shield.
        """
        cmd_lst = [ "[ 0x83 0x83 ] % [ 0x80 0x80 ] %"]
        for hit in cmd_lst:
            self.send(hit)


    def set_mode_iso14443A(self):
        """
        ISO Control register - 0x01 - see Table 6-6, [REF_DS_TRF7970A]
        """
        # [ 0x83] : command 0x03 : Software reinitialization => Power On Reset
        #
        # [0x09 0x31] *0x09 = 0x31
        #   Modulator and SYS_CLK Control register : 13.56 and 00K 100%
        #
        # [0x01 0x88]
        #   *0x01 = 0x88
        #   ISO Control Register :
        #       80 : Receiving without CRC : true
        #       08 : Active Mode
        #

        cmd_lst = [ "[ 0x83 ] % [ 0x09 0x31 ]",
            "[ 0x01 0x88 ]"
        ]
        self.__logger.info("Set HydraNFC to ISO 14443 A mode")
        self.__logger.info("")
        for hit in cmd_lst:
            self.send(hit)

    def set_mode_iso14443B(self):
        """
        ISO Control register - 0x01 - see Table 6-6, [REF_DS_TRF7970A]
        """
        cmd_lst = [ "[ 0x83 ] % [ 0x09 0x31 ] [ 0x49 r ]",
            "[ 0x01 0x0C ] [ 0x41 r ]"
        ]
        self.__logger.info("Set HydraNFC to ISO 14443 B mode")
        self.__logger.info("")
        for hit in cmd_lst:
            self.send(hit)

    def field_on(self):
        cmd_lst = [ "[ 0x00 0x20 ]",
                    ]
        for hit in cmd_lst:
            resp = self.send(hit)

    def field_off(self):
        cmd_lst = [ "[ 0x00 0x00 ]",
                    ]
        for hit in cmd_lst:
            resp = self.send(hit)

    def send_wupa(self):
        cmd_lst = [ "[ 0x8F 0x90 0x3D 0x00 0x0F 0x52 ] %:10 [ 0x6C r:2 ] [ 0x5C r ]",
                    "[ 0x7F r:2 ]",
                    ]
        for hit in cmd_lst:
            resp = self.send(hit)

        resp = self.extract_resp(resp)
        self.__logger.debug("\t<%s" % resp)
        self.__logger.debug("")
        return [int(hit, 16) for hit in resp.split("0x")[1:]]

    def send_reqa(self):
        cmd_lst = [ "[ 0x8F 0x90 0x3D 0x00 0x0F 0x26 ] %:100 [ 0x6C r:2 ] [ 0x5C r ]",
                    "[ 0x7F r:2 ]",
                    ]
        for hit in cmd_lst:
            resp = self.send(hit)

        resp = self.extract_resp(resp)
        self.__logger.debug("\t<%s" % resp)
        self.__logger.debug("")
        return [int(hit, 16) for hit in resp.split("0x")[1:]]


    def send_reqb(self):
        cmd_lst = [ "[ 0x01 0x0C ] [ 0x41 r ] [ 0x00 0x20 ] [ 0x40 r ]",
                    "[ 0x01 0x0C ] ",
                    ]
        for hit in cmd_lst:
            resp = self.send(hit)

        # self.send_raw([0x05, 0x00, 0x00, 0x04], crc_in_cmd=False)
        self.raw([0x8F, 0x91, 0x3D, 0x00, 0x30, 0x05, 0x00, 0x00])
        # self.send_raw([0x05, 0x00, 0x00, 0x71, 0xFF])

        cmd_lst = [ " [ 0x6C r:2 ] [ 0x5C r ]",
                    "[ 0x7F r:2 ]",
                    ]
        for hit in cmd_lst:
            resp = self.send(hit)

        self.send("[ 0x01 0x8C ]")
        resp = self.extract_resp(resp)
        self.__logger.debug("\t<%s" % resp)
        self.__logger.debug("")
        return [int(hit, 16) for hit in resp.split("0x")[1:]]

    def raw(self, data, resp_len=32):

        data_field = "0x" + " 0x".join(("%02X" % hit) for hit in data)

        self.__logger.debug("send_raw")
        self.__logger.debug("\t>%s" % data)

        self.send("[ " + data_field + " ] %:10")

        resp = self.send("[ 0x7F r:%d ]" % resp_len)

        resp = self.extract_resp(resp)

        self.__logger.debug("\t<%s" % resp)
        self.__logger.debug("")

        return [int(hit, 16) for hit in resp.split("0x")[1:]]

    def send_raw(self, data, resp_len=32, crc_in_cmd=True):

        data = "0x" + " 0x".join(("%02X" % hit) for hit in data)

        self.__logger.debug("send_raw")
        self.__logger.debug("\t>%s" % data)
        bitslen = len(data.split(" ")) << 4
        bitslen = "0x%02X 0x%02X" % (bitslen >> 8, bitslen & 0xFF)
        data_field = "%s %s" % (bitslen, data)

        if crc_in_cmd:
            crc_field = "0x90"
        else:
            crc_field = "0x91"

        self.send("[ 0x8F " + crc_field + " 0x3D " + data_field + " ]")

        resp = self.send("[ 0x7F r:%d ]" % resp_len)

        resp = self.extract_resp(resp)

        self.__logger.debug("\t<%s" % resp)
        self.__logger.debug("")

        return [int(hit, 16) for hit in resp.split("0x")[1:]]

    def extract_resp(self, resp):
        for hit in resp:
            try:
                return hit.strip().split("READ: ")[1]
            except:
                continue
        return ""