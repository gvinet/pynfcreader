import pytest
from pynfcreader.devices.hydra_nfc_v2 import HydraNFCv2


@pytest.fixture
def hydranfc_connection():
    return HydraNFCv2(port="/dev/ttyACM0", debug=False)
