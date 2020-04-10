import argparse
from pathlib import Path

from dvdp.recorder_433 import RECORDINGS_DIR, Action, get_recordings
from dvdp.transmitter_433 import transmit


def available_options_str(recordings):
    result = ''
    for device_option, actions in recordings.items():
        result += f'\tdevice: {device_option}, actions: {actions}\n'
    return result


def main():
    recordings = get_recordings(RECORDINGS_DIR)
    parser = argparse.ArgumentParser(
        'Transmit signal from recordings.\n\n'
        'Recordings available in '
        f'{RECORDINGS_DIR}: \n'
        f'{available_options_str(recordings)}\n\n',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        'device',
        help=f'Name of device to transmit signal for. Available devices in'
             f' {RECORDINGS_DIR}:\n'
             f'{recordings.keys()}',
        type=str
    )
    parser.add_argument(
        'action',
        help=f'Action to perforn. Possible actions:\n '
             f'{",".join(action.value for action in list(Action))}',
        type=str
    )
    parser.add_argument(
        '--pin',
        '-p',
        default=14,
        help='BCM pin on rasberry pi used for transmission',
        type=int,
    )
    parser.add_argument(
        '--recordings',
        '-r',
        help='Directory containing recordings.',
        type=Path,
        default=RECORDINGS_DIR,
    )

    args = parser.parse_args()
    device = args.device
    action = args.action
    pin = args.pin
    source_dir = args.recordings
    recordings = get_recordings(source_dir)

    input_file = source_dir / (device + '_' + action + '.csv')
    if not input_file.exists():
        print(f'File {input_file} does not exist.\n\nAvailable Options:\n'
              f'{available_options_str(recordings)}')
        exit(1)

    transmit(input_file, pin)


if __name__ == '__main__':
    main()
