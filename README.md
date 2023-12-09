# README

## Intro

Speel jij het fantastische [Slag in de Rondte spel](https://www.slaginderondte.nl/spel) en mis je de vuurtorens?  
Dan is dit jouw project!!

Imagine a map, with multiple lighthouses, that light up!  
This repo contains MicroPython code to fade multiple LEDs independently.  
The fading patterns match real world lighthouse characteristics.  
The board game uses a day and night cycle of 8 minutes.  
The lighthouse LEDs follow this day/night cycle.  

Written in MicroPython for Raspberry Pi Pico.  
Inspired by the excellent board game: <https://www.slaginderondte.nl/spel>

![Board game Slag in de Rondte](/img/SlagInDeRondte-bordspel-small.jpg)

## Getting started

Make sure you can connect to your RPI Pico using your favorite editor.
E.g. Thonny or VSCode.

### part 1

For lookenspeepers, build this project and watschen der Blinkenlichten!

- Wire up your RaspberryPi Pico according to the Fritzing diagram.
- Save the script 'slag-in-de-rondte.py' to your Pico as 'main.py'
- Restart your Pico

YouTube [Slag in de Rondte, plain RPI Pico project](https://youtu.be/appXGaQrQTM).

### part 2

After finishing part 1, optionally install the LED's in the game board.

- Gently punch holes in the game board at the 5 island lighthouses, and Harlingen Harbor
- Place the LED's in the board game
- Solder wires to connect the LEDs
- Use the red and green LED for Harlingen Haven
  (when arriving at the harbor the red harbor light is on your port side)
- Connect the LED wires to your board, replacing the LED's
  (do not change the circuit, leave the resistors in place)

YouTube [Slag in de Rondte, the complete game board install](https://youtu.be/C6d0tgwr8xE)

## Software

The code uses Pulse Width Modulation (PWM) and async I/O:

- `PWM` allows fading of a LED on a digital port.
- the `uasyncio` library allows for cooperative concurrent task execution.

Tested on a RPI Pico, using MicroPython 1.21.0.

Tip: check for MicroPython linting
<https://github.com/Josverl/micropython-stubber#boost-micropython-productivity-in-vscode>

## Parts, wiring, pinout

| item                  | quantity |
| ---                   | --- |
| RaspberryPi Pico H    | 1 |
| LED white (5mm)       | 5 |
| LED red   (5mm)       | 1 |
| LED green (5mm)       | 1 |
| resistor 1kΩ          | 7 |
| breadboard            | 1 |
| hollow pipe tool 4mm  | 1 |

An [RPI Pico](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)
costs about €6.- at [Kiwi](https://www.kiwi-electronics.com/nl/raspberry-pi-pico-h-10939),
a breadboard (400 points) costs about €4.-.  
A hollow pipe tool (Dutch: holpijp) is only needed if you want to punch holes in your game board, to fit the LEDs.  

![Lighthouse LEDs](/img/lighthouse-leds-rpi-pico_bb.png)

![Hollow pipe tool](/img/holpijp.png)

| pin | pin name | in/out   | description         |
| --- | ---      | ---      | ---                 |
|  3  | GND      |          | ground              |
|  4  | GPIO 2   | in       | (future use)        |
| 21  | GPIO 16  | out 3.3V | LED Texel           |
| 22  | GPIO 17  | out 3.3V | LED Vlieland        |
| 24  | GPIO 18  | out 3.3V | LED Terschelling    |
| 25  | GPIO 19  | out 3.3V | LED Ameland         |
| 26  | GPIO 20  | out 3.3V | LED Schiermonnikoog |
| 39  | VSYS     | 5V       | LED Red + Green Harlingen |

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
