# pyNFCReader

A little python client to use as a low level contactless smart card reader the Hydra NFC, developped by Benjamin Vernoux (https://github.com/bvernoux/hydranfc). 

The communication with the Hydra NFC is based on the tutorial : https://github.com/bvernoux/hydrafw/wiki/HydraFW-HydraNFC-TRF7970A-Tutorial.
Now, the binary SPI mode is used (https://github.com/bvernoux/hydrafw/wiki/HydraFW-Binary-SPI-mode-guide).

## Status

  - It must be used at least with the firmware [Hydrafw_v0_7-beta-21].
  - It works with ISO 14443 A smart card.
  - The PCD frame size is currently limited to 16 bytes.
  - The anti collision is not entirely implemented, so only one card must be set in the field.


## Example

The file  pynfcreader/examples/reader_hydranfc_iso14443_a.py contains an example.
You can customize :
  - the port com and baudrate
  - the debug mode. 

It enables test several AIDs to select MasterCard or VISA cards.

Here's a log (where I've changed the UID and the historical bytes of the card. It is also PAN-free :) )

INFO  ::  Hydra NFC python driver version : 1.0.1 - POC
INFO  ::  	Supported hydra firmware 11.02.2015 - [HydraFW v0.7 Beta 21]
INFO  ::  	ISO 14443 A only
INFO  ::  	Only one card in the field during a transaction (anticollision not yet finished)
INFO  ::
INFO  ::  Connect to HydraNFC
INFO  ::
INFO  ::  Reset HydraNFC
INFO  ::
INFO  ::  Configure HydraNFC
INFO  ::  	Configure gpio to communicate with the hydra nfc shield in spi...
INFO  ::  	Configure hydra bus spi 2...
INFO  ::  	Reset hydra nfc...
INFO  ::
INFO  ::  Set HydraNFC to ISO 14443 A mode
INFO  ::
INFO  ::  field off
INFO  ::  field on
INFO  ::  REQA (7 bits):
INFO  ::  		26                                                     &
INFO  ::
INFO  ::  ATQA:
INFO  ::  		04 00                                                  ..
INFO  ::
INFO  ::  Select cascade level 1:
INFO  ::  		93 20                                                  ..
INFO  ::
INFO  ::  Select cascade level 1 response:
INFO  ::  		XX XX XX XX XX                                         .....
INFO  ::
INFO  ::  Select cascade level 1:
INFO  ::  		93 70 XX XX XX XX B4                                   .......
INFO  ::
INFO  ::  Select cascade level 1 response:
INFO  ::  		28 B4 FC                                               (..
INFO  ::
INFO  ::  Request for Answer To Select (RATS):
INFO  ::  	PCD selected options:
INFO  ::  		FSDI : 0x0 => max PCD frame size : 16 bytes
INFO  ::  		CID  : 0x0
INFO  ::  RATS
INFO  ::  		E0 00                                                  ..
INFO  ::
INFO  ::  Answer to Select (ATS = RATS response):
INFO  ::  		0A 78 80 82 02 XX XX XX   XX XX 92 43                  .x......   ...C
INFO  ::
INFO  ::  	T0 : 0x78
INFO  ::  		FSCI : 0x8 => max card frame size : 256 bytes
INFO  ::  		TA(1) present
INFO  ::  		TB(1) present
INFO  ::  		TC(1) present
INFO  ::  	TA(1) : 0x80
INFO  ::  		Interpretation : TODO...
INFO  ::  	TB(1) : 0x82
INFO  ::  		Interpretation : TODO...
INFO  ::  	TC(1) : 0x02
INFO  ::  		NAD not supported
INFO  ::  		CID supported
INFO  ::  	Historical bytes : XX XX XX XX XX
INFO  ::  	CRC : 92 43
INFO  ::
INFO  ::
INFO  ::
INFO  ::  PPS
INFO  ::  	PCD selected options:
INFO  ::  	CID : 0x0
INFO  ::  	PPS1 not transmitted
INFO  ::  PPS:
INFO  ::  		D0                                                     .
INFO  ::
INFO  ::  PPS response:
INFO  ::  		D0 73 87                                               .s.
INFO  ::
INFO  ::  	PPS accepted
INFO  ::
INFO  ::  APDU command:
INFO  ::  		00 A4 04 00 0E 32 50 41   59 2E 53 59 53 2E 44 44      .....2PA   Y.SYS.DD
INFO  ::  		46 30 31 00                                            F01.
INFO  ::
INFO  ::  Block chaining, 2 blocks to send
INFO  ::  		TPDU command:
INFO  ::  			1A 00 00 A4 04 00 0E 32   50 41 59 2E 53 59 53 2E      .......2   PAY.SYS.
INFO  ::  			44 44                                                  DD
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			AA 00 2F 4C                                            ../L
INFO  ::
INFO  ::  		TPDU command:
INFO  ::  			0B 00 46 30 31 00                                      ..F01.
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			1B 00 6F 3B 84 0E 32 50   41 59 2E 53 59 53 1C 74      ..o;..2P   AY.SYS.t
INFO  ::
INFO  ::  		TPDU command:
INFO  ::  			A2                                                     .
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			12 2E 44 44 46 30 31 A5   29 BF 0C 26 61 10 34 A0      ..DDF01.   )..&a.4.
INFO  ::
INFO  ::  		TPDU command:
INFO  ::  			A3                                                     .
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			13 4F 07 A0 00 00 00 42   10 10 50 02 43 42 89 27      .O.....B   ..P.CB.'
INFO  ::
INFO  ::  		TPDU command:
INFO  ::  			A2                                                     .
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			12 87 01 01 61 12 4F 07   A0 00 00 00 03 10 39 84      ....a.O.   ......9.
INFO  ::
INFO  ::  		TPDU command:
INFO  ::  			A3                                                     .
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			03 10 50 04 56 49 53 41   87 01 02 90 00 5D 96         ..P.VISA   .....].
INFO  ::
INFO  ::  APDU response:
INFO  ::  		6F 3B 84 0E 32 50 41 59   2E 53 59 53 2E 44 44 46      o;..2PAY   .SYS.DDF
INFO  ::  		30 31 A5 29 BF 0C 26 61   10 4F 07 A0 00 00 00 42      01.)..&a   .O.....B
INFO  ::  		10 10 50 02 43 42 87 01   01 61 12 4F 07 A0 00 00      ..P.CB..   .a.O....
INFO  ::  		00 03 10 10 50 04 56 49   53 41 87 01 02 90 00         ....P.VI   SA.....
INFO  ::
INFO  ::  APDU command:
INFO  ::  		00 A4 04 00 07 A0 00 00   00 42 10 10 00               ........   .B...
INFO  ::
INFO  ::  		TPDU command:
INFO  ::  			0A 00 00 A4 04 00 07 A0   00 00 00 42 10 10 00         ........   ...B...
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			0A 00 69 85 46 EB                                      ..i.F.
INFO  ::
INFO  ::  APDU response:
INFO  ::  		69 85                                                  i.
INFO  ::
INFO  ::  APDU command:
INFO  ::  		00 A4 04 00 07 A0 00 00   00 04 10 10 00               ........   .....
INFO  ::
INFO  ::  		TPDU command:
INFO  ::  			0B 00 00 A4 04 00 07 A0   00 00 00 04 10 10 00         ........   .......
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			0B 00 6A 82 2A A9                                      ..j.*.
INFO  ::
INFO  ::  APDU response:
INFO  ::  		6A 82                                                  j.
INFO  ::
INFO  ::  APDU command:
INFO  ::  		00 A4 04 00 07 A0 00 00   00 03 10 10 00               ........   .....
INFO  ::
INFO  ::  		TPDU command:
INFO  ::  			0A 00 00 A4 04 00 07 A0   00 00 00 03 10 10 00         ........   .......
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			0A 00 69 85 46 EB                                      ..i.F.
INFO  ::
INFO  ::  APDU response:
INFO  ::  		69 85                                                  i.
INFO  ::
INFO  ::  APDU command:
INFO  ::  		00 A4 04 00 05 A0 00 00   00 03 00                     ........   ...
INFO  ::
INFO  ::  		TPDU command:
INFO  ::  			0B 00 00 A4 04 00 05 A0   00 00 00 03 00               ........   .....
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			1B 00 6F 33 84 07 A0 00   00 00 03 10 10 A5 4E DF      ..o3....   ......N.
INFO  ::
INFO  ::  		TPDU command:
INFO  ::  			A2                                                     .
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			12 28 9F 38 18 9F 66 04   9F 02 06 9F 03 06 95 0E      .(.8..f.   ........
INFO  ::
INFO  ::  		TPDU command:
INFO  ::  			A3                                                     .
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			13 9F 1A 02 95 05 5F 2A   02 9A 03 9C 01 9F 47 6A      ......_*   ......Gj
INFO  ::
INFO  ::  		TPDU command:
INFO  ::  			A2                                                     .
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			12 37 04 BF 0C 0A DF 60   02 0B 32 9F 4D 02 63 88      .7.....`   ..2.M.c.
INFO  ::
INFO  ::  		TPDU command:
INFO  ::  			A3                                                     .
INFO  ::
INFO  ::  		TPDU response:
INFO  ::  			03 0B 32 90 00 C4 F7                                   ..2....
INFO  ::
INFO  ::  APDU response:
INFO  ::  		6F 33 84 07 A0 00 00 00   03 10 10 A5 28 9F 38 18      o3......   ....(.8.
INFO  ::  		9F 66 04 9F 02 06 9F 03   06 9F 1A 02 95 05 5F 2A      .f......   ......_*
INFO  ::  		02 9A 03 9C 01 9F 37 04   BF 0C 0A DF 60 02 0B 32      ......7.   ....`..2
INFO  ::  		9F 4D 02 0B 32 90 00                                   .M..2..
INFO  ::
INFO  ::  field off