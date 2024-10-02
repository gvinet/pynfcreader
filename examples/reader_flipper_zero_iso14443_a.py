# Copyright (C) 2015-2024 Guillaume VINET
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

from pynfcreader.devices import flipper_zero
from pynfcreader.sessions.iso14443.iso14443a import Iso14443ASession

fz = flipper_zero.FlipperZero("/dev/ttyACM0", debug=False)

hn = Iso14443ASession(drv=fz, block_size=120)

hn.connect()
hn.field_off()
time.sleep(0.1)
hn.field_on()
hn.polling()
r = hn.send_apdu("00 a4 04 00   0E   32 50 41 59 2E 53 59 53 2E 44 44 46 30 31   00")
