from datetime import datetime, timedelta
from pathlib import Path
from time import sleep
import csv
import argparse

raspberry = True
try:
    import RPi.GPIO as GPIO
except ImportError:
    raspberry = False

from dvdp.recorder_433 import Action, RECORDINGS_DIR


def record(pin, time):
    if not raspberry:
        raise RuntimeError(
            'Raspberry is required to record files. Cannot import RPi.GPIO',
        )

    received_signal = [[], []]  # [[time of reading], [signal reading]]

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)

    print('Count down')
    for i in range(5, 0, -1):
        print(i)
        sleep(1)
        GPIO.input(pin)

    print('**Started recording**')
    sample_time = datetime.now()
    begin_time = sample_time
    delta_time = timedelta(seconds=0)
    while delta_time.total_seconds() < time:
        delta_time = datetime.now() - begin_time
        received_signal[0].append(delta_time)
        received_signal[1].append(GPIO.input(pin))

    print('**Ended recording**')
    print(len(received_signal[0]), 'samples recorded')
    GPIO.cleanup()

    print('**Processing results**')
    previous_value = 0
    previous_time = timedelta(seconds=0)
    processed_signal = [[0], [0]]
    for time, value in zip(received_signal[0], received_signal[1]):
        if value != previous_value:
            processed_signal[0].append(previous_time.total_seconds() * 1000000)
            processed_signal[1].append(previous_value)
            processed_signal[0].append(time.total_seconds() * 1000000)
            processed_signal[1].append(value)
        previous_value = value
        previous_time = time
    return processed_signal


def main():
    parser = argparse.ArgumentParser(
        'Record 433 signals and save to disk.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        'name',
        help='Name of device to record signal for. e.g. "bedroom_light"',
        type=str,
    )
    parser.add_argument(
        'action',
        help='Action to record."',
        type=Action,
        choices=list(Action),
    )
    parser.add_argument(
        '--pin',
        '-p',
        help='BCM pin number of Raspberry Pi pin receiving signals.',
        type=int,
        default=15,
    )
    parser.add_argument(
        '--directory',
        '-d',
        help='Output directory for recordings.',
        default=RECORDINGS_DIR,
        type=Path,
    )
    parser.add_argument(
        '--time',
        '-t',
        default=3,
        type=int,
        help='Recording time in seconds.'
    )
    parser.add_argument(
        '--remove',
        '-r',
        default=False,
        help='Remove all old recordings in recordings directory.',
        action='store_true',
    )

    args = parser.parse_args()
    name = args.name
    pin = args.pin
    dir_out: Path = args.directory
    time = args.time
    remove = args.remove
    action = args.action

    dir_out.mkdir(parents=True, exist_ok=True)

    if remove:
        for filename in dir_out.glob('*.csv'):
            filename.unlink()

    output_file = dir_out / (name + '_' + action.value + '.csv')

    print(f'Recording to file {output_file}.')
    processed_signal = record(pin, time)

    with open(output_file, 'w') as file:
        writer = csv.writer(file, delimiter=';')
        for time, value in zip(processed_signal[0], processed_signal[1]):
            writer.writerow([time, value])


if __name__ == '__main__':
    main()
