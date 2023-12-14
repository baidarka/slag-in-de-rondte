# README

## Intro

The board game '[Slag in de Rondte](https://www.slaginderondte.nl/spel)' is played on a map of the Dutch Wadden Sea.  
This project lights up its lighthouses!

![Slag in de Rondte extension](/img/slag-in-de-rondte-project-result-small.png)

The repo contains MicroPython code to fade multiple LEDs independently.  
The fading patterns match real world lighthouse characteristics.  
Written for, and tested on, [Raspberry Pi Pico](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html).

The board game uses a day/night cycle of about eight minutes.
Switch off your room lights when the lighthouses come on.
And turn your room lights back on, when the lighthouses switch off.  
(this day/night cycle can be bypassed)

![Board game Slag in de Rondte](/img/SlagInDeRondte-bordspel-small.jpg)

## Getting started

Get started with your RPI Pico: <https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico>

### part 1

For lookenspeepers, build this project and watschen der Blinkenlichten!

- Wire up your Raspberry Pi Pico according to the Fritzing diagram
- (optional: ground GPIO2 with a resistor to bypass the 8 minutes day/night cycle and be 'always on')
- Save the script 'slag-in-de-rondte.py' to your Pico as 'main.py'
- Restart your Pico

YouTube [Slag in de Rondte, plain RPI Pico project](https://youtu.be/appXGaQrQTM).

### part 2

After finishing part 1, install the LED's in the game board.

- Solder cheap speaker cable to the LEDs, to extend their connectors
- Gently punch holes in the game board at the 5 island lighthouses, and Harlingen Harbor
- Place the LED's in the board game
  (use the red and green LEDs at Harlingen Haven)
- Connect the LED wires to your breadboard as before
  (do not change the circuit, leave the resistors in place)

YouTube [Slag in de Rondte, the complete game board install](https://youtu.be/sG-JDIeeyXA)

## Software

The code uses Pulse Width Modulation (PWM) and async I/O:

- `PWM` allows fading of a LED on a digital port.
- the `uasyncio` library allows for cooperative concurrent task execution.

Tested on a RPI Pico, using MicroPython 1.21.0.

Tip: check for MicroPython linting
<https://github.com/Josverl/micropython-stubber#boost-micropython-productivity-in-vscode>

## Parts, wiring, pinout

| item                  | quantity |
| ---                   | ---      |
| RaspberryPi Pico H    | 1        |
| LED white (5mm)       | 5        |
| LED red   (5mm)       | 1        |
| LED green (5mm)       | 1        |
| resistor 1kΩ          | 7        |
| breadboard            | 1        |
| hollow pipe tool 4mm  | 1        |
| speaker cable (thin)  | 3 meters |

A [RPI Pico](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)
costs about €6.- at [Kiwi](https://www.kiwi-electronics.com/nl/raspberry-pi-pico-h-10939),
a breadboard (400 points) costs about €4.-.  
A hollow pipe tool (Dutch: holpijp) is only needed if you want to punch holes in your game board, to fit the LEDs.  

![Lighthouse LEDs](/img/lighthouse-leds-rpi-pico_bb.png)

![Hollow pipe tool](/img/holpijp.png)

| pin | pin name | in/out   | description                  |
| --- | ---      | ---      | ---                          |
|  3  | GND      |          | ground                       |
|  4  | GPIO 2   | in       | disables night-and-day cycle |
| 21  | GPIO 16  | out 3.3V | LED Texel                    |
| 22  | GPIO 17  | out 3.3V | LED Vlieland                 |
| 24  | GPIO 18  | out 3.3V | LED Terschelling             |
| 25  | GPIO 19  | out 3.3V | LED Ameland                  |
| 26  | GPIO 20  | out 3.3V | LED Schiermonnikoog          |
| 39  | VSYS     | 5V       | LED Red + Green Harlingen    |

CAUTION:
Drawing too much power from the board may damage the board.  
Thus use resistors to drive the LEDs.  
For tinkering only. Use at your own risk.

If you want to 'separate the controller from the power', you can add a PCA9685 in the mix.  
The PCA9685 (a servo driver) has it's own power, can be controlled using I2C, and supports PWM.  
I picked one up for €8.-. Possibly more on that later.

## Contributions

Feel free to contribute, in bite-size PR's. :)  
Please be nice!

Sound? Listen in on [VHF Brandaris](http://www.tbandsma.nl/index.php/scanner/).  :)
To all board players, seamen, skippers, schippers and Schiffer:
Fair winds and following seas!
