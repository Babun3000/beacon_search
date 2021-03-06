#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Copyright {2018} {Bluebird Mountain | Moritz Obermeier}

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import time
import RPi.GPIO as GPIO

BEACON_INPUT_PIN = 17 #GPIO PIN Raspberry Zero

def setup_buttons():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(BEACON_INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def main():
  start_time_ms = int(round(time.time() * 1000))

  def interrupt_button_1(channel):
    if GPIO.input(BEACON_INPUT_PIN) == 1:
      #beacon found
      now_ms = int(round(time.time() * 1000))
      hits = 0
      for x in range(0, 140):
        if GPIO.input(BEACON_INPUT_PIN) == 1:
          hits = hits+1
        time.sleep(0.0005) #lowest on raspi zero
      if hits > 85:
        print(str(now_ms-start_time_ms) + "ms; hits: " + str(hits) + " Signal detected!")
      else:
        print(str(now_ms-start_time_ms) + "ms; hits: " + str(hits) + " ignored")
  try:
    print("Starting Signal detector")
    setup_buttons()
    #add the interupt event here
    GPIO.add_event_detect(BEACON_INPUT_PIN, GPIO.RISING,
      callback = interrupt_button_1, bouncetime = 70)
    while True:
      time.sleep(1)
  except Exception as e:
    print("Caught exeption")
    print(traceback.format_exc())
    sys.exit(1)

if __name__ == "__main__":
  main()
