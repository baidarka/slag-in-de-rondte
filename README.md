# README

## Intro

Speel jij het fantastische [Slag in de Rondte spel](https://www.slaginderondte.nl/spel) en mis je de vuurtorens?  
Dan is dit jouw project!!

Imagine a map, with multiple lighthouses, that light up!  
This repo contains MicroPython code to fade multiple LEDs independently.
The fading patterns match real world characteristics of light.  
Written for Raspberry Pi Pico.  
Inspired by the excellent board game: <https://www.slaginderondte.nl/spel>

![Board game Slag in de Rondte](/img/SlagInDeRondte-bordspel-small.jpg)

## Purpose

Gently punch holes in the game board at the 5 island lighthouses.  
Place the LEDs. Wire up, and GO!!

Or, for lookenspeepers, just build this project and  
watschen der Blinkenlichten!

## Software

The code uses Pulse Width Modulation (PWM) and async I/O:

- PWM allows fading of a LED on a digital port.
- the `uasyncio` library allows for cooperative concurrent task execution.

Use Thonny or VSCode to save the `slag-in-de-rondte.py` file to your RPI Pico.

Save it to your Pico as 'main.py' to run it on startup.

## Hardware

![Lighthouse LEDs](/img/lighthouse-leds-rpi-pico_bb.png)

## Contributions

Feel free to contribute, in bite-size PR's. :)  
Please be nice!
