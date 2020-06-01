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
from pynfcreader.devices.hydra_nfc import HydraNFC
from pynfcreader.sessions.iso15693.iso15693 import Iso15693Session

hydra_nfc = HydraNFC(port="/dev/ttyACM0", debug=False)
hn = Iso15693Session(drv=hydra_nfc)
hn.connect()
hn.field_off()
time.sleep(0.2)
hn.field_on()
hn.get_all_auto()
