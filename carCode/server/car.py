import RPi.GPIO as GPIO
import PCA9685 as p
import time

int speed = 50;

def initialize():
	motor.setup()
	car_dir.setup()

def go():
	motor.ctrl(1)
	motor.setspeed(speed)

def backup():
	motor.ctrl(1, -1)
	motor.setspeed(speed)

def stop():
	motor.ctrl(0)

def hardRight():
	car_dir.turn_right()

def hardLeft():
	car_dir.turn_left()

def softRight():
	car_dir.soft_right()

def softLeft():
	car_dir.soft_left()

def straight():
	car_dir.home()

def pedal(speedIn):
	motor.setSpeed(speedIn)
	speed = speedIn

def chacha():
	stop()
	hardLeft()
	go()
	time.sleep(3)
	backup()
	time.sleep(3)
	stop()
	hardRight()
	go()
	time.sleep(3)
	backup()
	time.sleep(3)
	stop()

def threeSixty():
