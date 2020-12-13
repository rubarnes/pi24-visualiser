#!/usr/bin/python3

# Some globals
DEBUG = False

try:
	import liquidcrystal_i2c as i2c
except ImportError:
	print("pythonliquidcrystal_i2c Missing, Assuming a debug environment with no hardware!")
	DEBUG = True

import time
import json
import argparse


def make_data_string(craft):
	out = ""

	if "flight" in craft.keys():
		out += craft["flight"]
	if "altitude" in craft.keys():
		out += str(craft["altitude"]) + "ft "
	if "speed" in craft.keys():
		out += str(craft["speed"]) + "kn "

	return out

def clear_display(disp):
	if not DEBUG:
		disp.clear()

def print_to_display(disp, line, string):
	if not DEBUG:
		# TODO: hard-coded 20 character limit, there must be some way to ask the library what the screen allows.
		#		That, or we can just add a command-line argument.
		disp.printline(line, string[:20])
	else:
		print(string)

def display(data, disp, sleeptime=5):
	clear_display(disp)

	aircraft = data["aircraft"]

	if not aircraft:
		print_to_display(disp, 0, "No Aircraft.")

	j = 0
	for i in range(len(aircraft)):
		craft = aircraft[i]

		if i % 4 == 0 and i > 0: # TODO: Hard-coded 4 per-page limit, there must be some way to ask the library what the screen allows.
								 #       Could also just make it an argument.
			j = 0
			time.sleep(sleeptime)
			clear_display(disp)

		if not "flight" in craft.keys():
			print_to_display(disp, j, "Unkown Aircraft.")
			j += 1
			continue

		print_to_display(disp, j, make_data_string(craft))

		j += 1


if __name__ == "__main__":
	args = argparse.ArgumentParser(description="Tools to display data from FlightRadar24's Pi24 on LCD displays over GPIO.")
	
	args.add_argument("-t", "--test", type=bool,
						help="Enables test mode, Forcing it to use stdout rather than actual hardware.")
	args.add_argument("-d", "--data", type=str, required=True,
						help="The file path of the data to use.")
	args.add_argument("-w", "--wait", type=int, default=5,
						help="The time to wait between each 'page' of text.")
	args.add_argument("-l", "--loop", type=bool, default=False,
						help="Enables looping, re-opening the file and displaying updated results.")

	args = args.parse_args()

	if args.test:
		DEBUG = True
	
	json_file = open(args.data, 'r')
	data = json.load(json_file)
	json_file.close()

	if not DEBUG:
		# TODO: What is 0x27?
		disp = i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)
	else:
		disp = None
	
	# Python doesn't have Do ... While, so this is a kind-of hack to get the same outcome.
	while True: # DO
		display(data, disp, args.wait)

		if not args.loop: # WHILE
			break

		time.sleep(args.wait)
		
		json_file = open(args.data, 'r')
		data = json.load(json_file)
		json_file.close()

