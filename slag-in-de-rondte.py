#######################################################################
# Board game: Slag in de Rondte
# https://www.slaginderondte.nl
#
# https://github.com/baidarka/slag-in-de-rondte
# Raspberry Pi Pico.
# Fade five white LEDs independently,
# based on the characteristics of five Dutch lighthouses.
#
# For the daring!!
# Gently punch holes in the game board at the 5 island lighthouses.
# Place the LEDs. Wire up, and GO!!
#
# Tested on Raspberry Pi Pico with MicroPython 1.21.0.
# https://www.raspberrypi.com/documentation/microcontrollers
#
# I use regular 5mm LED's (about 3.2V and about 20mA).
# Each LED has a resistor attached, i use 1kOhm resistors.
# Although 1kOhm is too much, it nicely reduces the
# overall light intensity.
#
# Author: @baidarka 2023
#
####################################################################### 
# Warning: For tinkering only. Use at your own risk.
# Add an I/O controller to separate the LED power from the board.
# Your mileage may vary.
#######################################################################
from machine import ADC, Pin, PWM
from time import sleep
import math
import time
import uasyncio

# Just pick a reasonable frequency.
# (At least higher than the human eye can detect.)
f = 1000

# Assign each lighthouse a PWM object (a LED on a GPIO pin)
texel           = PWM(Pin(16), f)
vlieland        = PWM(Pin(17), f)
terschelling    = PWM(Pin(18), f)
ameland         = PWM(Pin(19), f)
schiermonnikoog = PWM(Pin(20), f)

adc = machine.ADC(4)

# Coroutine: Flash a LED, once
async def flash(pwm):
  """Fade a LED on and off, using Pulse Width Modulation

  A lighthouse 'flash' may take 2 seconds or more. 
  The max PWM duty cycle: 65025 (see RaspberryPi.org) 
  Light off ==> 'duty cycle = 0'. 
  Light on  ==> 'duty cycle = 65025'. 

  Parameters
  ----------
  pwm : PWM
      The PWM object representing a LED.
      
  Returns
  -------
  None
  """
  for i in range(100):
    # Using sin() is just a snazzy way of getting increasing and
    # descreasing fractions in one loop...
    fraction = math.sin(i/100 * math.pi)
    pwm.duty_u16(round(fraction * 65025))
    await uasyncio.sleep_ms(12)
  
  # Force light off
  pwm.duty_u16(0)
  await uasyncio.sleep_ms(1600)

# Corouting: Isophase a LED
async def isophase(pwm, d):
  """Isophase a LED on and off, using Pulse Width Modulation

  Isophase means: 
  first half of the duration 'on', second half of the duration 'off'

  Parameters
  ----------
  pwm : PWM
      The PWM object representing a LED.
  d : int
      Duration of the entire on-and-off cycle in seconds.
      
  Returns
  -------
  None
  """    
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

# Corouting: Fade out a LED
async def fade_out(pwm):

  # Get the current duty cycle and fade out from there.
  current_duty_cycle = pwm.duty_u16()
  current_duty_cycle_fraction = (current_duty_cycle // 650.25)
  
  # Light off
  for i in range(current_duty_cycle_fraction, 0, -2):
    pwm.duty_u16(round(i/100 * 65025))
    await uasyncio.sleep_ms(12)
  pwm.duty_u16(0)  

# Coroutine: characteristics of light: Texel FL(2) W 10s
async def characteristics_texel(texel):
  while True:
    try:
      time_begin = time.ticks_ms()
      await flash(texel)
      await flash(texel)
      time_elapsed = time.ticks_ms() - time_begin
      await uasyncio.sleep_ms(10000 - time_elapsed)
      
    except (uasyncio.CancelledError):
      # Switch off
      await fade_out(texel)
      print('Task Texel cancelled')
      raise

# Coroutine: characteristics of light: Vlieland ISO W 4s
async def characteristics_vlieland(vlieland):
  while True:
    try:
      await isophase(vlieland, 4)

    except (uasyncio.CancelledError):
      # Switch off
      await fade_out(vlieland)
      print('Task Vlieland cancelled')
      raise

# Coroutine: characteristics of light: Terschelling FL(1) W 5s
async def characteristics_terschelling(terschelling):
  while True:
    try:
      time_begin = time.ticks_ms()
      await flash(terschelling)
      time_elapsed = time.ticks_ms() - time_begin
      await uasyncio.sleep_ms(5000 - time_elapsed)

    except (uasyncio.CancelledError):
      # Switch off
      await fade_out(terschelling)
      print('Task Terschelling cancelled')
      raise

#Coroutine: characteristics of light: Ameland FL(3) W 15s
async def characteristics_ameland(ameland):
  while True:
    try:
      time_begin = time.ticks_ms()
      await flash(ameland)
      await flash(ameland)
      await flash(ameland)
      time_elapsed = time.ticks_ms() - time_begin
      await uasyncio.sleep_ms(15000 - time_elapsed)

    except (uasyncio.CancelledError):
      # Switch off
      await fade_out(ameland)
      print('Task Ameland cancelled')
      raise

# Coroutine: characteristics of light: Schiermonnikoog FL(4) W 20s
async def characteristics_schiermonnikoog(schiermonnikoog):
  while True:
    try:
      time_begin = time.ticks_ms()
      await flash(schiermonnikoog)
      await flash(schiermonnikoog)
      await flash(schiermonnikoog)
      await flash(schiermonnikoog)
      time_elapsed = time.ticks_ms() - time_begin
      await uasyncio.sleep_ms(20000 - time_elapsed)
      
    except (uasyncio.CancelledError):
      # Switch off
      await fade_out(schiermonnikoog)
      print('Task Schiermonnikoog cancelled')
      raise

# Coroutine: entry point for uasyncio program
async def main():

  # Half a day contains roughly a tidal cycle, high water + low water
  # In the board game this cycle takes 8 minutes (480 seconds)
  tidal_cycle = 480
  while True:
    
    # A night of sailing starts. Switch on all five lighthouses
    print('Night')
    task_tx  = uasyncio.create_task(characteristics_texel(texel))
    task_vl  = uasyncio.create_task(characteristics_vlieland(vlieland))
    task_ts  = uasyncio.create_task(characteristics_terschelling(terschelling))
    task_am  = uasyncio.create_task(characteristics_ameland(ameland))
    task_sch = uasyncio.create_task(characteristics_schiermonnikoog(schiermonnikoog))
    
    # Leave lighthouses on for the night
    await uasyncio.sleep(tidal_cycle)
    
    # Print the temperature. (keep an eye on the board)
    ADC_voltage = adc.read_u16() * (3.3/65536)
    temp_celcius = 27 - (ADC_voltage - 0.706)/0.001721
    print('Temperature: {}'.format(round(temp_celcius)))

    # After a night of sailing comes...  a day of sailing :)
    # Switch off all five lighthouses
    print('Day')
    task_tx.cancel()
    task_vl.cancel()
    task_ts.cancel()
    task_am.cancel()
    task_sch.cancel()
    
    ## Leave lighthouses off for the day
    await uasyncio.sleep(tidal_cycle)

# Start event loop
uasyncio.run(main())