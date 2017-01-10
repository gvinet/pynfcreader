# pyNFCReader

A little python client to use as a low level contactless smart card reader the Hydra NFC, developped by Benjamin Vernoux (https://github.com/bvernoux/hydranfc). 

The communication with the Hydra NFC is based on the tutorial : https://github.com/bvernoux/hydrafw/wiki/HydraFW-HydraNFC-TRF7970A-Tutorial.
Now, the binary SPI mode is used (https://github.com/bvernoux/hydrafw/wiki/HydraFW-Binary-SPI-mode-guide).

## Status

  - It must be used at least with the firmware [Hydrafw_v0_7-beta-21].
  - It works with ISO 14443 A and ISO 15693 smart card.
  - The PCD frame size is currently limited to 16 bytes.
  - The anti collision is not entirely implemented, so only one card must be set in the field.


## Example - ISO 14443 A card

The file  pynfcreader/examples/reader_hydranfc_iso14443_a.py contains an example.
You can customize :
  - the port com and baudrate
  - the debug mode.

It tests several AIDs to select either MasterCard or VISA cards.

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

    ## Example - ISO 15693 card

The file  pynfcreader/examples/reader_hydranfc_iso15693.py contains an example.
You can customize :
  - the port com and baudrate
  - the debug mode.

Here's a log a 2017 "Bordeaux fête le vin" card.

    INFO  ::  Hydra NFC python driver version : 1.2.0 - Proof of concept
    INFO  ::  	Supported hydra firmware 11.02.2015 - [HydraFW v0.7 Beta 21]
    INFO  ::  	Supported protocols : ISO 14443 A, ISO 15693
    INFO  ::  	Only one card in the field during a transaction (anticollision not yet finished)
    INFO  ::
    INFO  ::  Connect to HydraNFC
    INFO  ::
    INFO  ::  Check if HydraNFC already configured
    INFO  ::  	NOK. Reset and configuration will be performed...
    INFO  ::  Reset HydraNFC
    INFO  ::
    INFO  ::  Configure HydraNFC
    INFO  ::  	Configure gpio to communicate with the hydra nfc shield in spi...
    INFO  ::  	Configure hydra bus spi 2...
    INFO  ::  	Reset hydra nfc...
    INFO  ::
    INFO  ::  Set HydraNFC to ISO 15693 mode
    INFO  ::
    INFO  ::
    INFO  ::
    INFO  ::  field on
    INFO  ::
    INFO  ::  Inventory
    INFO  ::  Command:
    INFO  ::  		26 01 00                                               &..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 F5 3F CC 6F 50 01   04 E0                        ...?.oP.   ..
    INFO  ::
    INFO  ::
    INFO  ::  Get System Info
    INFO  ::  Command:
    INFO  ::  		22 2B F5 3F CC 6F 50 01   04 E0                        "+.?.oP.   ..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 0F F5 3F CC 6F 50 01   04 E0 00 00 1B 03 01         ...?.oP.   .......
    INFO  ::
    INFO  ::  	UID..........: E0 04 01 50 6F CC 3F F5
    INFO  ::  	DSFID........: 00
    INFO  ::  	AFI..........: 00
    INFO  ::  	Memory size..: 112 bytes : 28 blocks of 4 bytes (1B 03)
    INFO  ::  	IC Reference.: Motorola (01)
    INFO  ::
    INFO  ::  Get and print all memory
    INFO  ::  	Get all memory
    INFO  ::  Read Single Block 00
    INFO  ::  Command:
    INFO  ::  		42 20 00                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 3E 6B 83 17                                      ..>k..
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 01
    INFO  ::  Command:
    INFO  ::  		42 20 01                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 3E 6B 83 17                                      ..>k..
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 02
    INFO  ::  Command:
    INFO  ::  		42 20 02                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 40 00 00 00                                      ..@...
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 03
    INFO  ::  Command:
    INFO  ::  		42 20 03                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 00 07 00 00                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 04
    INFO  ::  Command:
    INFO  ::  		42 20 04                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 00 00 00 36                                      .....6
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 05
    INFO  ::  Command:
    INFO  ::  		42 20 05                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 BE 3E 38 C0                                      ...>8.
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 06
    INFO  ::  Command:
    INFO  ::  		42 20 06                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 83 00 00 00                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 07
    INFO  ::  Command:
    INFO  ::  		42 20 07                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 00 F8 34 B8                                      ....4.
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 08
    INFO  ::  Command:
    INFO  ::  		42 20 08                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 81 00 5F 04                                      ...._.
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 09
    INFO  ::  Command:
    INFO  ::  		42 20 09                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 00 00 00 80                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 0A
    INFO  ::  Command:
    INFO  ::  		42 20 0A                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 79 39 09 06                                      ..y9..
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 0B
    INFO  ::  Command:
    INFO  ::  		42 20 0B                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 08 22 00 00                                      ..."..
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 0C
    INFO  ::  Command:
    INFO  ::  		42 20 0C                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 00 00 04 FC                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 0D
    INFO  ::  Command:
    INFO  ::  		42 20 0D                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 45 40 40 19                                      ..E@@.
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 0E
    INFO  ::  Command:
    INFO  ::  		42 20 0E                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 01 00 00 00                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 0F
    INFO  ::  Command:
    INFO  ::  		42 20 0F                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 E0 E5 BF 82                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 10
    INFO  ::  Command:
    INFO  ::  		42 20 10                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 02 EE 08 00                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 11
    INFO  ::  Command:
    INFO  ::  		42 20 11                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 00 00 80 E9                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 12
    INFO  ::  Command:
    INFO  ::  		42 20 12                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 0A 0F 18 90                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 13
    INFO  ::  Command:
    INFO  ::  		42 20 13                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 43 00 00 00                                      ..C...
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 14
    INFO  ::  Command:
    INFO  ::  		42 20 14                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 00 18 51 C4                                      ....Q.
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 15
    INFO  ::  Command:
    INFO  ::  		42 20 15                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 12 43 28 C1                                      ...C(.
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 16
    INFO  ::  Command:
    INFO  ::  		42 20 16                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 84 10 00 00                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 17
    INFO  ::  Command:
    INFO  ::  		42 20 17                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 00 00 00 00                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 18
    INFO  ::  Command:
    INFO  ::  		42 20 18                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 00 00 00 00                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 19
    INFO  ::  Command:
    INFO  ::  		42 20 19                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 00 00 00 00                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 1A
    INFO  ::  Command:
    INFO  ::  		42 20 1A                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 5D 22 71 C9                                      ..]"q.
    INFO  ::
    INFO  ::
    INFO  ::  Read Single Block 1B
    INFO  ::  Command:
    INFO  ::  		42 20 1B                                               B..
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 FC AD 8B 88                                      ......
    INFO  ::
    INFO  ::
    INFO  ::  	Get lock status
    INFO  ::  Get block security status - first_block_number 00 - number of block to read 28
    INFO  ::  Command:
    INFO  ::  		22 2C F5 3F CC 6F 50 01   04 E0 00 1B                  ",.?.oP.   ....
    INFO  ::
    INFO  ::  Response:
    INFO  ::  		00 00 00 00 00 00 00 00   00 00 00 00 00 00 00 00      ........   ........
    INFO  ::  		00 00 00 00 00 00 00 00   00 00 00 00 00               ........   .....
    INFO  ::
    INFO  ::
    INFO  ::  	Memory dump
    INFO  ::
    INFO  ::  	UID..........: E0 04 01 50 6F CC 3F F5
    INFO  ::  	DSFID........: 00
    INFO  ::  	AFI..........: 00
    INFO  ::  	Memory size..: 112 bytes : 28 blocks of 4 bytes (1B 03)
    INFO  ::  	IC Reference.: Motorola (01)
    INFO  ::  		[00] - Unlocked -  3E 6B 83 17 | >k..
    INFO  ::  		[01] - Unlocked -  3E 6B 83 17 | >k..
    INFO  ::  		[02] - Unlocked -  40 00 00 00 | @...
    INFO  ::  		[03] - Unlocked -  00 07 00 00 | ....
    INFO  ::  		[04] - Unlocked -  00 00 00 36 | ...6
    INFO  ::  		[05] - Unlocked -  BE 3E 38 C0 | .>8.
    INFO  ::  		[06] - Unlocked -  83 00 00 00 | ....
    INFO  ::  		[07] - Unlocked -  00 F8 34 B8 | ..4.
    INFO  ::  		[08] - Unlocked -  81 00 5F 04 | .._.
    INFO  ::  		[09] - Unlocked -  00 00 00 80 | ....
    INFO  ::  		[0A] - Unlocked -  79 39 09 06 | y9..
    INFO  ::  		[0B] - Unlocked -  08 22 00 00 | ."..
    INFO  ::  		[0C] - Unlocked -  00 00 04 FC | ....
    INFO  ::  		[0D] - Unlocked -  45 40 40 19 | E@@.
    INFO  ::  		[0E] - Unlocked -  01 00 00 00 | ....
    INFO  ::  		[0F] - Unlocked -  E0 E5 BF 82 | ....
    INFO  ::  		[10] - Unlocked -  02 EE 08 00 | ....
    INFO  ::  		[11] - Unlocked -  00 00 80 E9 | ....
    INFO  ::  		[12] - Unlocked -  0A 0F 18 90 | ....
    INFO  ::  		[13] - Unlocked -  43 00 00 00 | C...
    INFO  ::  		[14] - Unlocked -  00 18 51 C4 | ..Q.
    INFO  ::  		[15] - Unlocked -  12 43 28 C1 | .C(.
    INFO  ::  		[16] - Unlocked -  84 10 00 00 | ....
    INFO  ::  		[17] - Unlocked -  00 00 00 00 | ....
    INFO  ::  		[18] - Unlocked -  00 00 00 00 | ....
    INFO  ::  		[19] - Unlocked -  00 00 00 00 | ....
    INFO  ::  		[1A] - Unlocked -  5D 22 71 C9 | ]"q.
    INFO  ::  		[1B] - Unlocked -  FC AD 8B 88 | ....