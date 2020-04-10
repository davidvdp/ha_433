import argparse
import csv
import logging
from datetime import timedelta, datetime
from pathlib import Path

raspberry = True
try:
    import RPi.GPIO as GPIO
except ImportError:
    raspberry = False


def transmit(input_file: Path, pin):
    if not raspberry:
        logging.warning('Signal can only be transmitted using Raspberry pi.')
        return
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    signal_to_send = [[], []]
    with open(str(input_file), 'r') as file:
        spamreader = csv.reader(file, delimiter=';')
        for row in spamreader:
            time, value = row
            signal_to_send[0].append(timedelta(seconds=float(time) / 1000000))
            signal_to_send[1].append(int(value))

    time_start = datetime.now()

    print('Transmission started.')
    for time, value in zip(signal_to_send[0], signal_to_send[1]):
        while datetime.now() - time_start < time:
            pass
        GPIO.output(pin, value)

    print('Transmission stopped.')
    GPIO.cleanup()

