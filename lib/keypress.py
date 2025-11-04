from .roku_request import send_request
import logging

logger = logging.getLogger(__name__)

KEY_MAP = {
    " ": "Lit_%20",
    "\n": "Enter",
    # add more mappings if needed
}

def send_command(roku_ip: str, command: str):
    """Send a raw Roku command path."""
    send_request(roku_ip, f'keypress/{command}', method="POST")

def send_keypress_string(roku_ip: str, s: str):
    """Send each character in a string as a keypress."""
    for char in s:
        key = KEY_MAP.get(char, f"Lit_{char}")
        logger.debug(f"Sending keypress: {key}")
        send_request(roku_ip, f"keypress/{key}", method="POST")
