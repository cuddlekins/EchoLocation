from flask import Flask
from flask_ask import Ask, statement, convert_errors
import RPi.GPIO as GPIO
import logging

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.intent('GPIOControlIntent', mapping={'status': 'status', 'pin': 'pin'})
def gpio_control(status, pin):

    try:
        pinNum = int(pin)
    except Exception as e:
        return statement('Pin number not valid.')

    GPIO.setup(pinNum, GPIO.OUT)

    if status in ['on', 'high']:    GPIO.output(pinNum, GPIO.HIGH)
    if status in ['off', 'low']:    GPIO.output(pinNum, GPIO.LOW)

    return statement('Turning pin {} {}'.format(pin, status))


@ask.intent('LocationControlIntent', mapping={'status': 'status', 'location': 'location'})
def location_control(status, location):

    locationDict = {
        'car': 21,
        'motor': 21
    }

    targetPin = locationDict[location]

    GPIO.setup(targetPin, GPIO.OUT)

    if status in ['on', 'high']:        GPIO.output(targetPin, GPIO.HIGH)
    if status in ['off', 'low']:        GPIO.output(targetPin, GPIO.LOW)

    return statement('Turning {} {}!'.format(location, status))

@ask.intent('CircleControlIntent')
def circle_control():

    locationDict = {
        'threesixty': 20
    }

    targetPin = 20

    GPIO.setup(targetPin, GPIO.OUT)
    GPIO.output(targetPin, GPIO.HIGH)
    GPIO.output(targetPin, GPIO.LOW)

    return statement('Doing a three sixty!')

@ask.intent('ChaChaControlIntent')
def chacha_control():

    locationDict = {
        'chacha': 19
    }

    targetPin = 19

    GPIO.setup(targetPin, GPIO.OUT)
    GPIO.output(targetPin, GPIO.HIGH)
    GPIO.output(targetPin, GPIO.LOW)

    return statement('Doing the chacha!')
