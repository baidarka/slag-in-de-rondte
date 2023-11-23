# README

## Intro

Speel jij het fantastische [Slag in de Rondte spel](https://www.slaginderondte.nl/spel) en mis je de vuurtorens?  
Dan is dit jouw project!!

Imagine a map, with multiple lighthouses, that light up!  
This repo contains MicroPython code to fade multiple LEDs independently.  
The fading patterns match real world lighthouse characteristics.  
Written in MicroPython for Raspberry Pi Pico.  
Inspired by the excellent board game: <https://www.slaginderondte.nl/spel>

![Board game Slag in de Rondte](/img/SlagInDeRondte-bordspel-small.jpg)

## Getting started

Make sure you can connect to your RPI Pico using your favorite editor.
E.g. Thonny or VSCode.

- Wire up your RaspberryPi Pico according to the Fritzing diagram.
- Save the script 'slag-in-de-rondte.py' to your Pico as 'main.py'
- Restart your Pico

If all works:  

- Gently punch holes in the game board at the 5 island lighthouses.
- Place the LED's in the board game.  
- Solder wires to connect the LEDs + resistors
- Use the red and green LED for Harlingen Haven
  (when arriving at the harbor the red harbor light is on your port side)

Or, for lookenspeepers, just build this project and  
watschen der Blinkenlichten!

[Slag in de Rondte RPI Pico project](https://youtu.be/appXGaQrQTM) op YouTube.

## Software

The code uses Pulse Width Modulation (PWM) and async I/O:

- PWM allows fading of a LED on a digital port.
- the `uasyncio` library allows for cooperative concurrent task execution.

## Hardware

![Lighthouse LEDs](/img/lighthouse-leds-rpi-pico_bb.png)

## Contributions

Feel free to contribute, in bite-size PR's. :)  
Please be nice!
