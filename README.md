# README

## Intro

When looking at a map, imagine multiple lighthouses to light up.
MicroPython to fade multiple LEDs, independently.
The fading patterns match real world characteristics of light.
Written for Raspberry Pi Pico.
Inspired by the board game: <https://www.slaginderondte.nl/spel>

Gently punch holes in the game board at the 5 island lighthouses.  
Place the LEDs. Wire up, and GO!!

Or, for lookenspeepers, just build this project and  
watschen der Blinkenlichten!

The code uses PWM and uasyncio:

- PWM allows fading of a LED on a digital port.
- uasyncio allows for cooperative concurrent task execution.

## Software

Use Thonny or VSCode to save the slag-in-de-rondte.py file to your RPI Pico.

If you save it as 'main.py' in your Pico, it will be run on startup.

## Hardware

![Lighthouse LEDs](/img/lighthouse-leds-rpi-pico_bb.png)

## Contributions

Feel free to contribute, in bite-size PR's. :)

Please be nice!
