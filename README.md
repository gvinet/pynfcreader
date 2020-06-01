# pyNFCReader

A python 3 client to use the Hydra NFC as contactless smart card reader. (https://hydrabus.com/):

  - It must be used with the firmware at least from commit b2176d21ae3f8cf52565a1da4c6bc268896beb04 (May 29 2020).
  - It works with ISO 14443 A and ISO 15693 smart card.
  
## Installing

### From source

Clone this repository, then run the following command :

```
$ python setup.py install --user
```

## Example
 
### ISO 14443 A card

The file  pynfcreader/examples/reader_hydranfc_iso14443_a.py contains an example.
You can customize :
  - the port com
  - the debug mode.

It tests several AIDs to select either MasterCard or VISA cards.

Here's a log (where I've changed the UID and the historical bytes of the card. It is also PAN-free :) )
```
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
```

### ISO 15693 card

The file  pynfcreader/examples/reader_hydranfc_iso15693.py contains an example.
You can customize :
  - the port com and baudrate
  - the debug mode.

Here's a log of a ICODE SLI/SLIX card.

```
/home/aqw/01_Executables/conda/python3.8/bin/python3 /home/aqw/08_MyProjects/hydranfc/pynfcreader/examples/reader_hydranfc_iso15693.py
INFO  ::  Connect to HydraNFC
INFO  ::  
INFO  ::  field off
INFO  ::  
INFO  ::  field on
INFO  ::  
INFO  ::  Command Inventory
INFO  ::  26 01 00                                               &..   
INFO  ::  	flags               : 26
INFO  ::  	command             : 01
INFO  ::  	mask_len            : 00
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 E7 44 40 02 50 01   04 E0                        ...D@.P.   ..
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	dsfid                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	uid                      : E7 44 40 02 50 01 04 E0
INFO  ::  	                         : E0 04 01 50 02 40 44 E7
INFO  ::  
INFO  ::  Command Get system information
INFO  ::  22 2B E7 44 40 02 50 01   04 E0                        "+.D@.P.   ..
INFO  ::  	flags               : 22
INFO  ::  	command             : 2B
INFO  ::  	uid_opt             : E7 44 40 02 50 01 04 E0
INFO  ::  
INFO  ::  Response:
INFO  ::  00 0F E7 44 40 02 50 01   04 E0 00 00 1B 03 01         ...D@.P.   .......
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	info_flags               : 0F
INFO  ::  	                         : DSFID is supported. DSFID field is present
AFI is supported. AFI field is present
Information on VICC memory s ize is supported. Memory size field is present.
Information on IC reference is supported. IC reference field is present.

INFO  ::  	uid                      : E7 44 40 02 50 01 04 E0
INFO  ::  	                         : E0 04 01 50 02 40 44 E7
INFO  ::  	dsfid                    : 00
INFO  ::  	                         : 00
INFO  ::  	afi                      : 00
INFO  ::  	                         : 00
INFO  ::  	vicc_memory_size         : 1B 03
INFO  ::  	                         : 28 blocks of 28
INFO  ::  	ic_reference             : 01
INFO  ::  	                         : Unknown code
INFO  ::  
INFO  ::  Get and print all memory
INFO  ::  	Get all memory
INFO  ::  Command Read single block
INFO  ::  42 20 00                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 00
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 E1 40 0E 01                                      ...@..   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : E1 40 0E 01
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 01                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 01
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 03 00 FE 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 03 00 FE 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 02                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 02
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 03                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 03
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 04                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 04
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 05                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 05
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 06                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 06
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 07                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 07
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 08                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 08
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 09                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 09
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 0A                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 0A
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 0B                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 0B
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 0C                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 0C
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 0D                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 0D
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 0E                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 0E
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 0F                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 0F
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 10                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 10
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 11                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 11
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 12                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 12
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 13                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 13
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 14                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 14
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 15                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 15
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 16                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 16
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 17                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 17
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 18                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 18
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 19                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 19
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 1A                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 1A
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  Command Read single block
INFO  ::  42 20 1B                                               B .   
INFO  ::  	flags               : 42
INFO  ::  	command             : 20
INFO  ::  	block_nb            : 1B
INFO  ::  
INFO  ::  Response:
INFO  ::  00 00 00 00 00 00                                      ......   
INFO  ::  	flags                    : 00
INFO  ::  	                         : 0x00
INFO  ::  	block_security_status    : 00
INFO  ::  	                         : Unlocked (00)
INFO  ::  	data                     : 00 00 00 00
INFO  ::  
INFO  ::  	Memory dump
INFO  ::  
INFO  ::  		[  0] - Unlocked -  E1 40 0E 01 | .@..
INFO  ::  		[  1] - Unlocked -  03 00 FE 00 | ....
INFO  ::  		[  2] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[  3] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[  4] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[  5] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[  6] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[  7] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[  8] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[  9] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 10] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 11] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 12] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 13] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 14] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 15] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 16] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 17] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 18] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 19] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 20] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 21] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 22] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 23] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 24] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 25] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 26] - Unlocked -  00 00 00 00 | ....
INFO  ::  		[ 27] - Unlocked -  00 00 00 00 | ....

Process finished with exit code 0

```