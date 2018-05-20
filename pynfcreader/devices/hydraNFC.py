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
import time

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

    def __init__(self, port="C0M8", timeout_sec=0.3, debug=True):

        self.__hydrafw_version_supported = "13.10.2016 - [HydraFW v0.8 Beta]"
        self.__version = "1.2.1 - Proof of concept"

        self.__port = port
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
        self.__logger.info("\tSupported protocols : ISO 14443 A, ISO 15693")
        self.__logger.info("\tOnly one card in the field during a transaction (anticollision not yet finished)")
        self.__logger.info("")

    def connect(self):
        self.__logger.info("Connect to HydraNFC")
        self.__logger.info("")
        self.__ser = serial.Serial(self.__port, timeout=self.__timeout_sect)

    def getLogger(self):
        return self.__logger

    def reset_and_configure(self):
        self.__logger.info("Check if HydraNFC already configured")

        if self.cs_off():
            self.__logger.info("\tOK. Skip configuration...")
            self.__logger.info("")
        else:
            self.__logger.info("\tNOK. Reset and configuration will be performed...")
            self.reset()
            self.configure()

    def reset(self):
        self.__logger.info("Reset HydraNFC")
        self.__logger.info("")
        self.__ser.write('\x00')
        self.__ser.write('\x0F\n')
        self.__ser.readline()
        self.__ser.readline()

    def configure(self):
        self.__logger.info("Configure HydraNFC")
        self.__logger.info("\tConfigure gpio to communicate with the hydra nfc shield in spi...")
        self.__configure_gpio_spi()

        if not self.__spi_configuration():
            raise Exception("Spi configuration failure!!!")

        self.__logger.info("\tReset hydra nfc...")
        self.__reset_hydra_nfc()
        self.__logger.info("")

    def __spi_configuration(self):
        for spi_conf_byte in [ '\x83', '\x80']:
            self.__logger.info("\tConfigure hydra bus spi 2 with value 0x%2X..." % ord(spi_conf_byte))
            self.__configure_spi2(spi_conf_byte)

            self.__logger.info("\tCheck hydra bus spi 2 configuration...")
            if self.trf7970a_read_modulator():
                return True

        return False

    def __configure_gpio_spi(self):
        self.__logger.debug("Configure NFC/TRF7970A in SPI mode with Chip Select")
        self.__ser.write("exit\n")
        self.__ser.readline()
        self.__ser.readline()
        self.__ser.readline()
        self.__ser.readline()
        self.__ser.write("\n")
        self.__ser.readline()
        self.__ser.readline()

        self.__ser.write("gpio pa3 mode out off\n")
        self.__ser.readline()
        self.__ser.readline()
        self.__ser.write("gpio pa2 mode out on\n")
        self.__ser.readline()
        self.__ser.readline()
        self.__ser.write("gpio pc0 mode out on\n")
        self.__ser.readline()
        self.__ser.readline()
        self.__ser.write("gpio pc1 mode out on\n")
        self.__ser.readline()
        self.__ser.readline()
        self.__ser.write("gpio pb11 mode out off\n")
        self.__ser.readline()
        self.__ser.readline()

        time.sleep(0.02);

        self.__ser.write("gpio pb11 mode out on\n");
        self.__ser.readline()
        self.__ser.readline()

        time.sleep(0.01);

        self.__ser.write("gpio pa2-3 pc0-1 pb11 r\n");
        for cmpt in range(8):
            self.__ser.readline()

    def __configure_spi2(self, spi_conf_byte):
        """
        We configure the hydrabus spi 2 used by the nfc shield.
        [REF_DS_TRF7970A], chapter 7.2.1 indicates that DATA_CLK line shall be 2Mhz.
        Hydranfc spi 2 clock can be 1.31Mhz, 2.62Mhz and 5.25Mhz. 2.62 works correctly
        If communication error arises, 1.31 shall be used.
        """

        for i in xrange(20):
            self.__ser.write("\x00")

        if "BBIO1" in self.__ser.read(5):
            self.__logger.debug("Into BBIO mode: OK")
            self.__ser.readline()
        else:
            raise Exception("Could not get into bbIO mode")

        self.__logger.debug("Switching to SPI mode:")
        self.__ser.write('\x01')
        self.__ser.read(4),
        self.__ser.readline()

        self.__logger.debug("Configure SPI2 polarity 0 phase 1:")
        self.__ser.write(spi_conf_byte)
        status=self.__ser.read(1) # Read Status
        self.cmd_check_status(status)

        self.__logger.debug("Configure SPI2 speed to 2620000 bits/sec:")
        self.__ser.write('\x63')
        status=self.__ser.read(1) # Read Status
        self.cmd_check_status(status)

    def cmd_check_status(self, status):
        if status != '\x01':
            print status.encode('hex'),
            self.__logger.info("Check status error")
            return False
        self.__logger.debug("Check status OK")
        return True

    def __reset_hydra_nfc(self):
        """
        We reset the TRF7970A chip used by the nfc shield.
        """
        cmd_lst = [ [ 0x83, 0x83 ],
                    [ 0x00, 0x21 ],
                    [ 0x09, 0x00 ],
                    [ 0x0B, 0x87 ],
                    [ 0x0B, 0x87 ],
                    [ 0x8D, ],
                    [ 0x00, 0x00 ],
                    [ 0x0D, 0x3E ],
                    [ 0x14, 0x0F ],
                    ]

        self.trf7970a_software_init()
        self.trf7970a_write_idle()
        for hit in cmd_lst:
            self.send(hit)
            time.sleep(0.1)

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
        cmd_lst = [[ 0x83 ], [ 0x09, 0x31 ],
                   [ 0x01, 0x88 ]]

        self.__logger.info("Set HydraNFC to ISO 14443 A mode")
        self.__logger.info("")
        for hit in cmd_lst:
            self.send(hit)
        self.send([0x41], 1)

    def set_mode_iso15693(self):
        cmd_lst = [[ 0x83 ], [ 0x09, 0x31 ],
                   [ 0x01, 0x02 ]]

        self.__logger.info("Set HydraNFC to ISO 15693 mode")
        self.__logger.info("")
        for hit in cmd_lst:
            self.send(hit)
        self.send([0x41], 1)

    def field_on(self):
        self.__logger.debug("Field on")
        self.send([0x00, 0x20])
        time.sleep(0.1)

    def field_off(self):
        self.__logger.debug("Field off")
        self.send([0x00, 0x00])
        time.sleep(0.1)

    def send_reqa(self, nb_try = 5):
        cmd_lst = [ [ 0x8F, 0x90, 0x3D, 0x00, 0x0F, 0x26 ] ]

        for hit in cmd_lst:
            resp = self.send(hit)

        resp = self.send([ 0x6C ], 2)

        time.sleep(0.1)

        resp = self.send([ 0x5C ], 1)

        if resp[0] == 0:
            return None

        resp = self.send([ 0x7F ], 2)

        self.__logger.debug("\t<%s" % self.array_to_str(resp))
        self.__logger.debug("")
        return resp

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

    def send_raw(self, data, resp_len=None, crc_in_cmd=True):

        self.__logger.debug("send_raw")
        self.__logger.debug("\t>%s" % str(data))
        bitslen = len(data) << 4
        bitslen = [ bitslen >> 8, bitslen & 0xFF]
        bitslen.extend(data)

        crc_field = 0x91
        if crc_in_cmd:
            crc_field = 0x90
        data = [0x8F, crc_field, 0x3D]
        data.extend(bitslen)

        self.send(data)

        # Todo : I shall read "IRQ Status Register" to be sure the transmission
        #  and the reception are finished. But... I'm lazzy, so I just wait 100 ms :) (as it works...)
        time.sleep(0.1)

        resp = self.send([0x5C], 1)

        resp = self.send([0x7F], resp[0])

        self.__logger.debug("\t<%s" % str(resp))
        self.__logger.debug("")

        return resp

    def extract_resp(self, resp):
        for hit in resp:
            try:
                return hit.strip().split("READ: ")[1]
            except:
                continue
        return ""

    def extract_resp_lst(self, resp):
        lst = []
        for hit in resp:
            try:
                lst.append(hit.strip().split("READ: ")[1])
            except:
                continue
        return lst

    def cs_on(self):
        self.__logger.debug("CS On")
        self.__ser.write('\x02')
        status=self.__ser.read(1)
        if status != '\x01':
            self.__logger.debug("CS-ON:")
            self.__logger.debug(status.encode('hex'))
            self.__logger.debug("Error")
            self.__logger.debug("")

    def cs_off(self):
        self.__logger.debug("CS Off")
        self.__ser.write('\x03')
        status=self.__ser.read(1)
        if status != '\x01':
            self.__logger.debug("CS-OFF:")
            self.__logger.debug(status.encode('hex'))
            self.__logger.debug("Error")
            self.__logger.debug("")
            return False
        return True

    def array_to_str(self, cmd):
        my_str = ""
        for hit in cmd:
            my_str += chr(hit)
        return my_str

    def str_to_array(self, cmd):
        my_str = []
        for hit in cmd:
            my_str.append(ord(hit))
        return my_str


    def send(self, cmd, read_len = None):
        self.__logger.debug("|--- Send cmd : %s" % self.array_to_str(cmd))
        self.cs_on()
        length = chr(len(cmd))

        resp_length = '\x00\x00'
        if read_len != None:
            resp_length = '\x00' + chr(read_len)

        self.__ser.write('\x05\x00' + length + resp_length)
        self.__ser.write(self.array_to_str(cmd))
        status = self.__ser.read(1)
        self.cmd_check_status(status)

        resp = None
        if read_len:
            resp = self.str_to_array(self.__ser.read(read_len))

        self.cs_off()
        self.__logger.debug("---|")
        self.__logger.debug("")
        return resp

    def trf7970a_software_init(self):
        self.cs_on()
        self.__logger.debug("Write TRF7970A Software Initialization 0x83 0x83 (no read):")
        self.__ser.write('\x05\x00\x02\x00\x00')
        self.__ser.write('\x83\x83')
        status=self.__ser.read(1)
        self.cmd_check_status(status)
        self.cs_off()

    def trf7970a_write_idle(self):
        self.cs_on()
        self.__logger.debug("Write TRF7970A Idle 0x80 0x80 (no read):")
        self.__ser.write('\x05\x00\x02\x00\x00')
        self.__ser.write('\x80\x80')
        status=self.__ser.read(1)
        self.cmd_check_status(status)
        self.cs_off()

    def trf7970a_read_modulator(self):
        self.cs_on()
        self.__logger.debug("Read TRF7970A Modulator/SYS_CLK Control Register (0x09):")
        self.__ser.write('\x05\x00\x01\x00\x01') # Write 1 data, read 1 data
        self.__ser.write('\x49') # Data
        self.__ser.read(1) # Read Status
        modulator = self.__ser.read(1)
        if modulator == '\x91':
            self.__logger.debug("OK")

        else:
            self.__logger.info("Demodulator Reading Error...")
        self.cs_off()
        if modulator == '\x91':
            return 1
        else:
            return 0

