# example-name v3.0.0 hardware 

| View | Top | Bottom |
| ---- | --- | ------ |
| <img src="doc/t-view.png" alt="drawing" width="300"> | <img src="doc/t-view-top.png" alt="drawing" width="300"/> | <img src="doc/t-view-bottom.png" alt="drawing" width="300"/> |
|  | <img src="doc/r-view-top.jpg" alt="drawing" width="300"/> | <img src="doc/r-view-bottom.jpg" alt="drawing" width="300"/> |

## Features

## Wiring

Schematic features. Schematic can be provided via issue.

**Connectors**

The node has connectors which are described in the table below.

| N | Connector | Description |
| - | - | - |
| 1 | DEBUG? |  |
| 2 | SWD1 |  |

[Here](https://docs.raccoonlab.co/guide/wires/) you can find manufacturer part number of connectors it self and its mates.

## Pin configuration and functions

| Pin N | DEBUG? | Pin N | SWD1 |
| ----- | ---------------- | ----- | ---------------- |
| 1 | 3.3 | 1 | GND |
| 2 | DEBUG_TX | 2 | SWLK |
| 3 | DEBUG_RX | 3 | SWDIO |
| 4 | SWDIO | 4 | 3.3 |
| 5 | SWCLK | | |
| 6 | GND | | |
| S1 | GND | | |
| S2 | GND |


Here you can see all connections of MCU.

<img src="doc/pinout.png" alt="pinout"/>

| MCU PIN         | PIN Numer | NET Name | Description |
| ---------- |  -- | --------------  | - |
| PA7            |  18 | VERSION     |  |
| PA14-BOOT0     |  36 | SWLK        |  |
| PA13           |  35 | SWDIO       |  |
| PA12_[PA10]    |  34 | STM_USB_DP  |  |
| PA11_[PA9]     |  33 | STM_USB_DM  |  |
| PF2-NRST       |  10 | STM_NRST    |  |
| PB7            |  46 | SDA         |  |
| PB6            |  45 | SCL         |  |
| PA10           |  32 | RX          |  |
| PF1-OSC_OUT    |  9  | OSC_OUT     |  |
| PF0-OSC_IN     |  8  | OSC_IN      |  |
| PC13           |  1  | LED_RED     |  |
| PC14-OSC32_IN  |  2  | LED_GREEN   |  |
| PC15-OSC32_OUT |  3  | LED_BLUE    |  |
| VSS/VSSA       |  7  | GND         |  |
| VSS            |  49 | GND         |  |
| PD3            |  41 | DEBUG_TX    |  |
| PD2            |  40 | DEBUG_RX    |  |
| VBAT           |  4  | 3.3         |  |
| VREF+          |  5  | 3.3         |  |
| VDD/VDDA       |  6  | 3.3         |  |


## Specifications

**Mechanical**

Scheme is shown on the picture below. CAN model can be provided via email request or issue on github or downloaded on GrabCAD (opens new window).

<img src="doc/drw.png" alt="drawing" height="400"/>

|       | Width, mm | Length, mm | Height, mm |
| ----- | --------- | ---------- | ---------- |
|Outline|      18.2 |       18.9 |        6.0 |
|PCB    |     15.97 |      18.85 |        2.0 |

Total weight of device less than 50 g.

### Housing

Information about case presented here.

### Absolute Maximum Ratings

### Recommended operating conditions

### ESD ratings

### MTFF

## Integration

**Recommended mechanical mounting**

**Connection example diagram**

### Power Supply Recommendations

Device is designed to operate from an input voltage supply range between 4.5 V and 5.5 V over CAN2 or CAN3 connector, or 5.5 - 30 V from CAN1. This input supply must be able to withstand the maximum input current and maintain a stable voltage. The resistance of the input supply rail should be low enough that an input current transient does not cause a high enough drop that can cause a false UVLO fault triggering and system reset. The amount of bulk capacitance is not critical, but a 47-uF or 100-uF electrolytic capacitor is a typical choice.

## Revision history

|View |Version| Date| Description|
|-    |-      |-    |-           |



## Order details

### PCB Specification Selection

- Board type : Panel by PCBWay
- Break-away rail: Yes
- Instructions:
~~~
Final size is larger ( 18.2 x 18.9 mm ) than board it self ( 15.97 x 18.85 mm), 
take a look at the picure in attachements. 
Panel should be designed to be able to install PWM1, PWM2 while assembly.
~~~
- Route Process: Panel as PCBWay prefer
- X-out Allowance in Panel:  Accept

- Size (single): 15.97 x 18.85 mm
- Quantity (single): 200
- Layers: 4 -   ['L1', 'L2', 'L3', 'L4'] check [PCBway layer stack](https://www.pcbway.com/multi-layer-laminated-structure.html)

- Material: FR-4
- FR4-TG: TG 150-160
- Thickness: 2.0
- Min Track/Spacing: 5/5mil (0.127 mm)
- Min Hole Size: 0.25 mm
- Solder Mask: Black
- Silkscreen: White
- Edge connector: No
- Surface Finish: HASL with lead
- Yes - Tick means you accept we might change "HASL" to "ENIG" at our discretion without extra charge.
- Via Process: Tenting vias
- Finished Copper: 1 oz Cu
- Other Special request:
~~~
Final size is larger ( 18.2 x 18.9 mm ) than board it self ( 15.97 x 18.85 mm )
~~~

### Assembly Service

- Turnkey
- Board type : Panelized PCBs
-  Assembly Side(s): Both sides
- Quantity: 200
- Contains Sensitive components/parts - No; 
- Do you accept alternatives/substitutes made in China? - Yes

- Number of Unique Parts: 0
- Number of SMD Parts: 0
- Number of BGA/QFP Parts: 0
- Number of Through-Hole Parts: 0

### Additional Options

- Firmware loading: Yes
- Detailed information of assembly:
~~~
Firmware is in attachements.
Take a look at the picure in attachements should be installed from the side.
~~~

## Device and Documentation Support

- [User manual]()
- [Hardware docs](doc/doc.pdf)

## Device Support

- [Firmware sources]()
- [Firmware binary]()

## TERMS OF USAGE / LICENCE

The material provided in this Github repository is subject to the following conditions. 

Firmware files: All firmwares are free (but not open source). Besides unlimited private use you are also granted the permission to use them for commercial purposes under the condition that (1) you dont modify the firmware, e.g. remove or change copyright statements, (2) provide it for free, i.e. dont charge any explicit or implicit fees to your customers, and (3) correctly and clearly cite the origin of the firmware and the project web page in any product documentation or web page. 

Hardware files: All hardware, for which material is provided, is open source hardware, under the terms of the TAPR Open Hardware License as published by the Free Hardware Foundation, see http://www.tapr.org/ohl.html. The TAPR license explicitly permits essentially unlimited commercial use, with only few conditions such as that copyright logos are not removed.

