# pyNFCReader

[![PyPI version](https://badge.fury.io/py/pyNFCReader.svg)](https://github.com/gvinet/pynfcreader)

A Python client for using the [Hydra NFC v1/v2](https://hydrabus.com/) as a low level contactless smart card reader:

  - It works with :
  
     - ISO 14443 A  & ISO 15693 card.
     - ISO 14443 B only for hydra NFC v2

## Getting started

### Install from source

Clone this repository, then run the following command :

```
$ python setup.py install --user
```

### Install with `pip`

```
$ pip install pyNFCReader
```

### Requirements

* pip install crcmod pyscard

### Help

* [ISO 14443 B](./wiki/iso14443/iso_14443_b.md)

## Example

The file  pynfcreader/examples/reader_hydranfc_iso14443_a.py contains an example.
You can customize :
  - the port com and baudrate
  - the debug mode. 

It enables :
  - to select a Master Card card
  - to read the first 0x19 response bytes
  - to send the Get Processing Options and get the response

Here's a log (where I've changed the UID and the historical bytes of the card :) )

    INFO  ::  Hydra NFC python driver version : 0.0.1 - beta
    INFO  ::  	Supported hydra firmware 11.02.2015 - [HydraFW v0.5 Beta]
    INFO  ::  	ISO 14443 A only
    INFO  ::  	Only one card in the field during a transaction
    INFO  ::  
    INFO  ::  Connect to HydraNFC
    INFO  ::  
    INFO  ::  Reset HydraNFC
    INFO  ::  
    INFO  ::  Configure HydraNFC
    INFO  ::  	Configure gpio and spi...
    INFO  ::  	Configure spi2...
    INFO  ::  
    INFO  ::  Set HydraNFC to ISO 14443 A mode
    INFO  ::  
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
    INFO  ::  		XX XX XX XX 17                                         .....   
    INFO  ::  	
    INFO  ::  Select cascade level 1:
    INFO  ::  		93 70 XX XX XX XX 17                                   .p.....   
    INFO  ::  	
    INFO  ::  Select cascade level 1 response:
    INFO  ::  		20 FC 70                                               ..p   
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
    INFO  ::  		00 A4 04 00 07 A0 00 00   00 04 10 10 19               ........   .....
    INFO  ::  	
    INFO  ::  		TPDU command:
    INFO  ::  			0A 00 00 A4 04 00 07 A0   00 00 00 04 10 10 19         ........   .......
    INFO  ::  		
    INFO  ::  		TPDU response:
    INFO  ::  			1A 00 6F 3F 84 07 A0 00   00 00 04 10 10 A5 7A 14      ..o?....   ......z.
    INFO  ::  		
    INFO  ::  		TPDU command:
    INFO  ::  			A3                                                     .   
    INFO  ::  		
    INFO  ::  		TPDU response:
    INFO  ::  			13 34 50 0A 4D 41 53 54   45 52 43 41 52 44 69 1C      .4P.MAST   ERCARDi.
    INFO  ::  		
    INFO  ::  		TPDU command:
    INFO  ::  			A2                                                     .   
    INFO  ::  		
    INFO  ::  		TPDU response:
    INFO  ::  			02 90 00 F1 09                                         .....   
    INFO  ::  		
    INFO  ::  APDU response:
    INFO  ::  		6F 3F 84 07 A0 00 00 00   04 10 10 A5 34 50 0A 4D      o?......   ....4P.M
    INFO  ::  		41 53 54 45 52 43 41 52   44 90 00                     ASTERCAR   D..
    INFO  ::  	
    INFO  ::  APDU command:
    INFO  ::  		80 A8 00 00 02 83 00 00                                ........   
    INFO  ::  	
    INFO  ::  		TPDU command:
    INFO  ::  			0B 00 80 A8 00 00 02 83   00 00                        ........   ..
    INFO  ::  		
    INFO  ::  		TPDU response:
    INFO  ::  			1B 00 77 16 82 02 19 80   94 10 08 01 01 00 C6 3D      ..w.....   .......=
    INFO  ::  		
    INFO  ::  		TPDU command:
    INFO  ::  			A2                                                     .   
    INFO  ::  		
    INFO  ::  		TPDU response:
    INFO  ::  			12 10 01 01 01 18 01 02   00 20 01 02 00 90 99 5B      ........   .......[
    INFO  ::  		
    INFO  ::  		TPDU command:
    INFO  ::  			A3                                                     .   
    INFO  ::  		
    INFO  ::  		TPDU response:
    INFO  ::  			03 00 C8 34                                            ...4   
    INFO  ::  		
    INFO  ::  APDU response:
    INFO  ::  		77 16 82 02 19 80 94 10   08 01 01 00 10 01 01 01      w.......   ........
    INFO  ::  		18 01 02 00 20 01 02 00   90 00                        ........   ..
    INFO  ::  	
