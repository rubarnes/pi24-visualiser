#!/usr/bin/python

import liquidcrystal_i2c as i2c
import time
import json


def make_data_string(craft):
	out = ""

	if "flight" in craft.keys():
		out += craft["flight"]
	if "altitude" in craft.keys():
		out += str(craft["altitude"]) + "ft "
	if "speed" in craft.keys():
		out += str(craft["speed"]) + "kn "

	return out
JSONFILE_FP = "/var/run/dump1090-mutability/aircraft.json"
#JSONFILE_FP = "aircraft.json" # TESTING DATA
DISPLAY = i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
while True:
	DISPLAY.clear()

	JSONFILE = open(JSONFILE_FP, 'r')
	data = json.load(JSONFILE)
	JSONFILE.close()

	aircraft = data["aircraft"]
	if not aircraft:
		DISPLAY.printline(0, "No Aircraft.")
	j=0
	for i in range(len(aircraft)):
		print(i, j)
		craft = aircraft[i]
		if i % 4 == 0 and i > 0:
			j = 0
			time.sleep(5)
			DISPLAY.clear()
		if not "flight" in craft.keys():
			DISPLAY.printline(j, "Unkown Aircraft.")
			j += 1
			continue
		DISPLAY.printline(j, make_data_string(craft)[:20])
		j += 1

	time.sleep(5)
