#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as gpio
import sys
import datetime

# gpio		pin no
gpio0		= 11
gpio1		= 12
gpio2		= 13
gpio3		= 15
gpio4		= 16
gpio5		= 18
gpio6		= 22
gpio7		= 7
gpio8		= 3
gpio9		= 5
gpio10		= 24
gpio11		= 26
gpio12		= 19

# fabryczne przyciski w stole, które będziemy "nasiskać"
factory_button_up = gpio0
factory_button_down = gpio1
factory_button_1 = gpio2
factory_button_2 = gpio3
factory_button_3 = gpio4

# przyciski lego, których naciśnięcie będziemy wykrywać
lego_button_up = gpio5
lego_button_down = gpio6
lego_button_stop = gpio7
lego_button_1 = gpio8
lego_button_2 = gpio9
lego_button_3 = gpio10

# 2 przekaźniki będą slużyły jako powiadomienie o uruchomieniu serwisu -> gotowości stołu do działania
notification_relay_switch_1 = gpio11
notification_relay_switch_2 = gpio12

gpio.setmode(gpio.BOARD)

gpio.setup(factory_button_up, gpio.OUT)
gpio.setup(factory_button_down, gpio.OUT)
gpio.setup(factory_button_1, gpio.OUT)
gpio.setup(factory_button_2, gpio.OUT)
gpio.setup(factory_button_3, gpio.OUT)

gpio.setup(lego_button_up, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(lego_button_down, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(lego_button_stop, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(lego_button_1, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(lego_button_2, gpio.IN, pull_up_down = gpio.PUD_UP)
gpio.setup(lego_button_3, gpio.IN, pull_up_down = gpio.PUD_UP)

gpio.setup(notification_relay_switch_1, gpio.OUT)
gpio.setup(notification_relay_switch_2, gpio.OUT)

max_ride_time = 18				# ile czasu zajmuje przejechanie stołowi z samej góry na doł lub odwrotnie (~17), plus jeszcze sekunda (+1)
default_sleep_interval = 0.1
sleep_interval = default_sleep_interval
shortened_sleep_interval = 0.05
current_action_duration = 0		# ile czasu trwa obecna akcja (inicjowana przyciskiem lego; akcja = "naciśnięcie" przycisku fabrycznego)
current_action = ""
prev_action = ""
tick_count = 0
max_tick_count = 1000000
press_tick = 0
just_pressed_action = ""
at_least_two_ticks = False

press_button = False			# stan niski na gpio -> wejscie relay switch board: powoduje włączenie przekaźnika
unpress_button = True			# analogicznie jak wyżej: wyłączenie przekaźnika

def zero_factory_buttons():
	# "zerujemy" przyciski fabryczne
	gpio.output(factory_button_up, unpress_button)
	gpio.output(factory_button_down, unpress_button)
	gpio.output(factory_button_1, unpress_button)
	gpio.output(factory_button_2, unpress_button)
	gpio.output(factory_button_3, unpress_button)
	log_factory_buttons_zeroed()

def press_factory_button(factory_button_pin_no):
	gpio.output(factory_button_pin_no, press_button)

def do_log(text):
	print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + text)
	sys.stdout.flush()

def log_lego_button_pressed(action, tick):
	do_log("lego button pressed, action = " + action + ", tick = " + str(tick))

def log_factory_buttons_zeroed():
	do_log("factory buttons zeroed")

def log_factory_button_press_emulated(action):
	do_log("factory button press emulated, action = " + action)

def log_action_timeout(action):
	do_log("action timeout, action = " + action)

def let_the_fanfare_sound():
	gpio.output(notification_relay_switch_1, press_button)
	time.sleep(0.15)
	gpio.output(notification_relay_switch_2, press_button)
	time.sleep(0.15)
	gpio.output(notification_relay_switch_1, unpress_button)
	time.sleep(0.15)
	gpio.output(notification_relay_switch_2, unpress_button)
	gpio.output(notification_relay_switch_1, press_button)
	time.sleep(0.15)
	gpio.output(notification_relay_switch_1, unpress_button)

do_log("====== Hi! ======")

zero_factory_buttons()

let_the_fanfare_sound()

# jezeli nacisniemy przycisk lego up|down|1|2|3 to akcja
# jezeli nacisniemy przycisk lego up|down|1|2|3 w trakcie gdy trwa inna akcja odpowiadajaca przyciskowi z tego zbioru, to nowa akcja
# jezeli nacisniemy przycisk lego w trakcie gdy trwa juz akcja odpowiadajaca danemu przyciskowi, to nic nie robimy
# jezeli nacisniemy przycisk lego stop gdy trwa jakas akcja, to zatrzymujemy akcje
# jezeli akcja trwa max_ride_time sekund, to konczymy akcje
while True:
	if not gpio.input(lego_button_up):
		just_pressed_action = "up"
	elif not gpio.input(lego_button_down):
		just_pressed_action = "down"
	elif not gpio.input(lego_button_stop):
		just_pressed_action = "stop"
	elif not gpio.input(lego_button_1):
		just_pressed_action = "1"
	elif not gpio.input(lego_button_2):
		just_pressed_action = "2"
	elif not gpio.input(lego_button_3):
		just_pressed_action = "3"
		
	if just_pressed_action != "":
		log_lego_button_pressed(just_pressed_action, tick_count)
		if prev_action == just_pressed_action and tick_count - press_tick == 1:
			# 2018-01-03 by wiele: musiałem wprowadzić sprawdzenie czy przycisk jest naciśnięty przez 2 obiegi pętly pod rząd z powodu samoistnych
			# randomowych "naciśnięć"; więcej tutaj: https://raspberrypi.stackexchange.com/questions/69820/doorbell-gpio-to-ground-randomly-triggers
			prev_action = ""
			current_action = just_pressed_action
			at_least_two_ticks = True
		else:
			press_tick = tick_count
			prev_action = just_pressed_action
			just_pressed_action = ""
			# skracamy czas do następnego obiegu pętli, żeby krócej trzeba było przytrzymywać przycisk
			sleep_interval = shortened_sleep_interval
		
	if current_action != "" and current_action != prev_action and at_least_two_ticks:
		prev_action = current_action
		current_action_duration = 0
		at_least_two_ticks = False
		zero_factory_buttons()
		if current_action == "stop":
			pass
		elif current_action == "up":
			press_factory_button(factory_button_up)
		elif current_action == "down":
			press_factory_button(factory_button_down)
		elif current_action == "1":
			press_factory_button(factory_button_1)
		elif current_action == "2":
			press_factory_button(factory_button_2)
		elif current_action == "3":
			press_factory_button(factory_button_3)
		log_factory_button_press_emulated(current_action)
		
	if current_action != "" and current_action != "stop":
		current_action_duration += sleep_interval
		if current_action_duration >= max_ride_time:
			current_action_duration = 0
			log_action_timeout(current_action)
			current_action = ""
			zero_factory_buttons()
		
	time.sleep(sleep_interval)
	# jeżeli sleep_interval został [tymczasowo] zmieniony, to powracamy do starego
	if sleep_interval != default_sleep_interval:
		sleep_interval = default_sleep_interval
	
	tick_count += 1
	if tick_count == max_tick_count:
		tick_count = 0
