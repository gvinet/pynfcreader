import time

from pynfcreader.sessions.iso14443.iso14443a import Iso14443ASession


def test_iso_14443_a_card_1_generic(hydranfc_connection):
    hn = Iso14443ASession(drv=hydranfc_connection, block_size=120)

    hn.connect()
    hn.field_off()
    time.sleep(0.1)
    hn.field_on()
    hn.polling()

    r = hn.send_apdu("00 a4 04 00   0E   32 50 41 59 2E 53 59 53 2E 44 44 46 30 31   00")
    assert b'oW\x84\x0e2PAY.S.DDF01\xa5E\xbf\x0cBO\x07\xa0\x00\x00\x00B\x10\x10P\x02\x87\x01\x01\x9f(\x08@\x02\x00\x00\x00\x00a#O\x07\xa0\x00\x00\x00\x04\x10\nMASTERCARD\x02\x9f(\x08@\x00 \x00\x00\x00\x00' == r

    r = hn.send_apdu("00 a4 04 00   07   A0 00 00 00 42 10 10  00")
    assert b'o?\x84\x07\xa0\x00\x00\x00B\x104P\x02CB\x87\x01\x01\x9f\x11\x01\x12\x0eTransacti CB_-\x04fren\xbf\xdf`\x02\x0b\x14\x9fM\x02\x0b\x14\xdf\x04' == r

    r = hn.send_apdu("00 a4 04 00   07   A0 00 00 00 04 10 10   00")
    assert b'o?\x84\x07\xa0\x00\x00\x00\x04\x104P\nMASTERCA\x87\x01\x02\x9f\x11\x01\x01\x9f\x12\nMTERCARD_-\x04fn\xbf\x0c\n\xdf`\x02\x0b\x14\x9fM\x14' == r

    hn.field_off()
