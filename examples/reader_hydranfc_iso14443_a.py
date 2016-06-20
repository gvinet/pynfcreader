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

from pynfcreader.reader.reader_iso14443a import ReaderHydraNFC

hn = ReaderHydraNFC(port="COM8", baudrate=230400, debug_mode=False, block_size = 16)
hn.connect()
hn.field_off()
hn.field_on()
exit(1)
hn.polling()
hn.send_apdu("00 a4 04 00   07   A0 00 00 00 04 10 10   19")
hn.send_apdu("80 A8 00 00   02   83 00   00")
hn.field_off()
