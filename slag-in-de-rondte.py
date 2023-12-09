#######################################################################
# Board game: Slag in de Rondte
# https://www.slaginderondte.nl
#
# https://github.com/baidarka/slag-in-de-rondte
# Fade five LEDs independently.
# Fading patterns are the characteristics of five Dutch lighthouses.
#
# Tested on Raspberry Pi Pico with MicroPython 1.21.0.
#
# Author: @baidarka 2023
#######################################################################
from machine import ADC, Pin, PWM
from time import sleep
import gc
import math
import time
import uasyncio

duty_max = 65535  # max duty cycle of RPI RP2xxx; MicroPython quickref
f = 1000 # frequency (Hz), just pick one quicker than the human eye 

# Assign each lighthouse a PWM object (a LED on a GPIO pin)
texel           = PWM(Pin(16), f)
vlieland        = PWM(Pin(17), f)
terschelling    = PWM(Pin(18), f)
ameland         = PWM(Pin(19), f)
schiermonnikoog = PWM(Pin(20), f)

# Optionally, run without night_n_day cycle
#  - pin not grounded = night and day cycle of 8 minutes
#  - pin grounded     = continuously use LEDs 
night_n_day     = Pin(2, Pin.IN, Pin.PULL_UP)

# Coroutine: Flash a LED, once
async def flash(pwm):
  """Fade a LED on and off, using Pulse Width Modulation

  A lighthouse 'flash' may take 2 seconds or more. 
  Light off ==> 'duty cycle = 0'. 
  Light on  ==> 'duty cycle = duty_max'. 

  Parameters
  ----------
  pwm : PWM
      A PWM object representing a LED.
      
  Returns
  -------
  None
  """
  for i in range(100):
    # Using sin() is just a snazzy way of getting increasing and
    # descreasing fractions in one loop...
    fraction = math.sin(i/100 * math.pi)
    pwm.duty_u16(round(fraction * duty_max))
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
      A PWM object representing a LED.
  d : int
      Duration of the entire on-and-off cycle in seconds.
      
  Returns
  -------
  None
  """    
  # Light on
  for i in range(0, 100, 5):
    pwm.duty_u16(round(i/100 * duty_max))
    await uasyncio.sleep_ms(10)
  await uasyncio.sleep_ms(round(d/2) * 1000)
    
  # Light off
  for i in range(100, 0, -5):
    pwm.duty_u16(round(i/100 * duty_max))
    await uasyncio.sleep_ms(10)
  pwm.duty_u16(0)
  await uasyncio.sleep_ms(round(d/2) * 1000)

# Corouting: Fade out a LED, to stop a cycle for the day
async def fade_out(pwm):

  # Get the current duty cycle and fade out from there.
  current_duty_cycle = pwm.duty_u16()
  current_duty_cycle_fraction = (current_duty_cycle // (duty_max/100))
  
  # Light off
  for i in range(current_duty_cycle_fraction, 0, -2):
    pwm.duty_u16(round(i/100 * duty_max))
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

  # Switch on all lighthouses (night)
  lighthouses = [
    uasyncio.create_task(characteristics_texel(texel)),
    uasyncio.create_task(characteristics_vlieland(vlieland)),
    uasyncio.create_task(characteristics_terschelling(terschelling)),
    uasyncio.create_task(characteristics_ameland(ameland)),
    uasyncio.create_task(characteristics_schiermonnikoog(schiermonnikoog))
  ]

  while True:

    # Leave lighthouses on for the night
    await uasyncio.sleep(tidal_cycle)
    
    # Enable night_n_day cycle? (is Pin grounded?)
    if night_n_day.value() == 0:
      print('pin grounded: no night_n_day')
      continue
    else:
      print('pin not grounded: night_n_day')

    # After a night of sailing comes...  a day of sailing :)
    # Switch off all five lighthouses
    print('day')
    for task in lighthouses:
      task.cancel()

    # Run the GC
    gc.collect()

    # Leave lighthouses off for the day
    await uasyncio.sleep(tidal_cycle)

    # Switch the lighthouses on for the night
    print('night')
    lighthouses = [
      uasyncio.create_task(characteristics_texel(texel)),
      uasyncio.create_task(characteristics_vlieland(vlieland)),
      uasyncio.create_task(characteristics_terschelling(terschelling)),
      uasyncio.create_task(characteristics_ameland(ameland)),
      uasyncio.create_task(characteristics_schiermonnikoog(schiermonnikoog))
    ]

# Start event loop
uasyncio.run(main())