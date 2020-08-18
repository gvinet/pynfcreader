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

import time
from pynfcreader.devices.hydra_nfc_v2 import HydraNFCv2
from pynfcreader.sessions.iso14443.iso14443b import Iso14443BSession

hydra_nfc = HydraNFCv2(port="/dev/ttyACM0", debug=False)
hn = Iso14443BSession(drv=hydra_nfc, block_size=120)

hn.connect()
hn.field_off()
time.sleep(0.1)
hn.field_on()
hn.polling()
print(hn.pupi)

r = hn.send_apdu("00 a4 04 00   0E   32 50 41 59 2E 53 59 53 2E 44 44 46 30 31   00")
print(r)
r =  hn.send_apdu("00 a4 04 00   07   A0 00 00 00 42 10 10  00")
print(r)
r = hn.send_apdu("00 a4 04 00   07   A0 00 00 00 04 10 10   00")
print(r)

hn.field_off()
