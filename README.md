# broku

***This tool is under active development, so expect bugs and idiosyncrasies. If you encounter problems, please open an issue.***

A simple CLI tool for Roku devices. Discovers Roku devices on your local network using SSDP, then leverages the [External Control Protocol (ECP)](https://developer.roku.com/docs/developer-program/dev-tools/external-control-api.md) to control and interact with those devices.

**NOTE**: For *most* Roku devices, you will need manually enable ECP interaction in the device's settings. This should be under Settings > System > Advanced System Settings > Control by mobile apps > Enabled

## Installation

Create a virtual environment called `venv` and activate it.

```sh
python -m venv venv
source venv/bin/activate
```

Then, install dependencies.

```
pip install -r requirements.txt
```

## Usage

Usage is as follows:

```sh
options:
  -h, --help            show this help message and exit
  -t, --target TARGET   Target Roku IP
  --debug               Enable debug logging
  -c, --command COMMAND
                        Send a Roku command
  -s, --string STRING   Type a string on the Roku
  -y, --youtube YOUTUBE
                        Play a YouTube video on Roku
```

For `-c`, you can pass any command as defined in the Roku docs [here](https://developer.roku.com/docs/developer-program/dev-tools/external-control-api.md#keypress-key-values). These commands generally correspond to buttons that you may find on a typical Roku remote.