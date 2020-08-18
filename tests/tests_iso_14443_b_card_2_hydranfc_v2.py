import time

from pynfcreader.sessions.iso14443.iso14443b import Iso14443BSession


def test_iso_14443_a_card_1_generic(hydranfc_connection):
    hn = Iso14443BSession(drv=hydranfc_connection, block_size=120)

    hn.connect()
    hn.field_off()
    time.sleep(0.1)
    hn.field_on()
    hn.polling()

    r = hn.send_apdu("00 a4 04 00   0E   32 50 41 59 2E 53 59 53 2E 44 44 46 30 31   00")
    assert b'o[\x84\x0e2PAY.S.DDF01\xa5I\xbf\x0cFO\x07\xa0\x00\x00\x00B\x10\x10P\x02\x87\x01\x01\x9f*\x01\x02\x9f\n\x08\x00\x01\x00\x00\x00\x00a#O\x07\xa0\x00\x04\x10\x10P\nMASTERRD\x87\x01\x01\x9f\n\x08\x00\x01\x05\x00\x00\x00' == r

    hn.field_off()
