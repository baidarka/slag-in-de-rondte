#######################################################################################
# Slag in de Rondte
# https://www.slaginderondte.nl
#
# Speel jij dit fantastische spel en mis je de vuurtorens?
# Dan is dit jouw project!!
#
# De vuurtorens van het Nederlands deel van de Waddenzee staan op de Waddeneilanden
# Texel, Vlieland, Terschelling, Ameland en Schiermonnikoog.
# Dit MicroPython project laat LED's oplichten met de lichtkarakters van deze vuurtorens. 
#
# For the daring!!
# Gently punch holes in the game board at the 5 island lighthouses.
# Place the LEDs. Wire up, and GO!!
#
# The lighthouses on the Dutch part of the Wadden Sea are found on the isles
# Texel, Vlieland, Terschelling, Ameland en Schiermonnikoog.
# This MicroPython project lights LED's with the proper characteristics of lights.
#
# Written in MicroPython.
# Tested on Raspberry Pi Pico with MicroPython 1.21.0.
# https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html
#
# For each lighthouse use one white LED.
# I use regular 5mm LED's (about 3.2V and about 20mA).
# Each LED has a resistor attached, i use 1kOhm resistors.
# Although 1kOhm is too much, it nicely reduces the overall light intensity.
#
# Author:  @baidarka 2023
#
######################################################################################### 
# Warning: For tinkering only!
# Use at your own risk.
# Drawing too much power from the GPIO pins may damage the RPI Pico board.
# Use a separate controller, PCA9685 ? to separate the LED power from the board.
# The setup used here (without controller) works fine for me. Your mileage may vary.
#
#########################################################################################
# Lichtkarakters:
#   Texel           FL(2) W 10s
#   Vlieland        ISO W 4s
#   Terschelling    FL(1) W 5s
#   Ameland         FL(3) W 15s
#   Schiermonnikoog FL(4) W 20s
#########################################################################################
import math
import time
import uasyncio
from machine import Pin, PWM
from time import sleep

# Just pick a reasonable frequency. (At least higher than the human eye can detect.)
f = 1000

# Each lighthouse has a light; a PWM object (a LED on a GPIO pin, and a frequency)
# (the characteristics of each lighthouse are defined in separate coroutines)
texel           = PWM(Pin(16), f)
vlieland        = PWM(Pin(17), f)
terschelling    = PWM(Pin(18), f)
ameland         = PWM(Pin(19), f)
schiermonnikoog = PWM(Pin(20), f)

# Coroutine: Flash a LED, once
# Glow the LED on and off, using PWM (Pulse Width Modulation).
async def flash(pwm):
    # A lighthouse 'flash' may take 2 seconds or more
    # According to RaspberryPi.org the max PWM duty cycle: 65025
    # Light off ==> 'duty cycle = 0'
    # Light on  ==> 'duty cycle = 65025'
    
    # Turn light on and off, using fractions of the duty cycle (PWM)
    for i in range(100):
        # Using sin() is just a snazzy way of getting increasing and descreasing fractions in one loop...
        fraction = math.sin(i/100 * math.pi)
        pwm.duty_u16(round(fraction * 65025))
        await uasyncio.sleep_ms(12)
    # Force light off
    pwm.duty_u16(0)
    await uasyncio.sleep_ms(1600)

# Corouting: Isophase a LED; first half of the duration 'on', second half of the duration 'off'
# Glow the LED on and off, using PWM (Pulse Width Modulation).
async def isophase(pwm, d):
    # Light on
    for i in range(0, 100, 5):
        pwm.duty_u16(round(i/100 * 65025))
        await uasyncio.sleep_ms(10)
    await uasyncio.sleep_ms(round(d/2) * 1000)
    
    # Light off
    for i in range(100, 0, -5):
        pwm.duty_u16(round(i/100 * 65025))
        await uasyncio.sleep_ms(10)
    pwm.duty_u16(0)
    await uasyncio.sleep_ms(round(d/2) * 1000)

# Coroutine: characteristics of light: Texel FL(2) W 10s
async def characteristics_texel(texel):
    while True:
        time_begin = time.ticks_ms()
        await flash(texel)
        await flash(texel)
        time_elapsed = time.ticks_ms() - time_begin
        await uasyncio.sleep_ms(10000 - time_elapsed)

# Coroutine: characteristics of light: Vlieland ISO W 4s
async def characteristics_vlieland(vlieland):
    while True:
        await isophase(vlieland, 4)

# Coroutine: characteristics of light: Terschelling FL(1) W 5s
async def characteristics_terschelling(terschelling):
    while True:
        time_begin = time.ticks_ms()
        await flash(terschelling)
        time_elapsed = time.ticks_ms() - time_begin
        await uasyncio.sleep_ms(5000 - time_elapsed)

#Coroutine: characteristics of light: Ameland FL(3) W 15s
async def characteristics_ameland(ameland):
    while True:
        time_begin = time.ticks_ms()
        await flash(ameland)
        await flash(ameland)
        await flash(ameland)
        time_elapsed = time.ticks_ms() - time_begin
        await uasyncio.sleep_ms(15000 - time_elapsed)

# Coroutine: characteristics of light: Schiermonnikoog FL(4) W 20s
async def characteristics_schiermonnikoog(schiermonnikoog):
    while True:
        time_begin = time.ticks_ms()
        await flash(schiermonnikoog)
        await flash(schiermonnikoog)
        await flash(schiermonnikoog)
        await flash(schiermonnikoog)
        time_elapsed = time.ticks_ms() - time_begin
        await uasyncio.sleep_ms(20000 - time_elapsed)

# Coroutine: entry point for uasyncio program
async def main():
    uasyncio.create_task(characteristics_texel(texel))
    uasyncio.create_task(characteristics_vlieland(vlieland))
    uasyncio.create_task(characteristics_terschelling(terschelling))
    uasyncio.create_task(characteristics_ameland(ameland))
    uasyncio.create_task(characteristics_schiermonnikoog(schiermonnikoog))

    while True:
        # do nothing, while tasks run :)
        await uasyncio.sleep_ms(10000)

# Start event loop
uasyncio.run(main())