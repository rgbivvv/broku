#!/usr/bin/env python3
import logging
import argparse
import ipaddress
from lib.device import get_device_info
from lib.keypress import send_keypress_string, send_command
from lib.youtube import launch_youtube
from lib.ssdp_discover import discover_roku_devices

logger = logging.getLogger(__name__)

def setup_logging(debug: bool = False):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [+] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def main():
    parser = argparse.ArgumentParser(description="A simple Roku CLI tool")
    parser.add_argument('-t', '--target', type=ipaddress.IPv4Address, help='Target Roku IP')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--command', help='Send a Roku command')
    group.add_argument('-s', '--string', help='Type a string on the Roku')
    group.add_argument('-y', '--youtube', help='Play a YouTube video on Roku')

    args = parser.parse_args()
    setup_logging(args.debug)

    targets = []
    if args.target is None:
        logger.info('Discovering Roku devices using SSDP...')
        devices = discover_roku_devices()
        if not devices:
            logger.info("No Roku devices found.")
            return
        logger.info(f'Found {len(devices)} Roku devices:')
        for ip in devices:
            logger.info(f'  - {ip}')
        targets = devices
    else:
        targets.append(str(args.target))

    for roku_ip in targets:

        logger.info(f'Querying device info at {roku_ip}...')
        device_info = get_device_info(roku_ip)
        device_info = device_info.get('device-info', {})

        print()
        title_str = f'DEVICE INFO ({roku_ip})'
        print(title_str)
        print('=' * len(title_str))
        print(f"ECP Mode:            {device_info.get('ecp-setting-mode', 'unknown')} {':)' if device_info.get('ecp-setting-mode') != 'limited' else ':('}")
        print(f"Power Mode:          {'ON' if device_info.get('power-mode') == 'PowerOn' else 'OFF'}")
        print(f"Friendly Device Name:{device_info.get('friendly-device-name')}")
        print(f"Default Device Name: {device_info.get('default-device-name')}")
        print(f"Device ID:           {device_info.get('device-id')}")
        print(f"Device Location:     {device_info.get('user-device-location')}")
        print(f"Model Name:          {device_info.get('model-name')}")
        print(f"Model Number:        {device_info.get('model-number')}")
        print(f"Software Version:    {device_info.get('software-version')}")
        print(f"Network Type:        {device_info.get('network-type')}")
        print(f"Network Name:        {device_info.get('network-name')}")
        print(f"Wifi MAC Address:    {device_info.get('wifi-mac')}")
        print()

        if args.command:
            logger.info(f'Sending command: {args.command}')
            send_command(roku_ip, args.command)

        if args.string:
            logger.info(f'Typing string: {args.string}')
            send_keypress_string(roku_ip, args.string)

        if args.youtube:
            logger.info(f'Launching YouTube video: {args.youtube}')
            launch_youtube(roku_ip, args.youtube)

if __name__ == '__main__':
    main()
