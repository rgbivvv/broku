import xmltodict
from typing import Any
from .roku_request import send_request

def convert_basic_types(obj: Any) -> Any:
    """Convert booleans and integers in XML-parsed dict."""
    if isinstance(obj, dict):
        return {k: convert_basic_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_basic_types(v) for v in obj]
    elif isinstance(obj, str):
        val = obj.strip().lower()
        if val == "true":
            return True
        elif val == "false":
            return False
        if val.isdigit() or (val.startswith('-') and val[1:].isdigit()):
            try:
                return int(val)
            except ValueError:
                pass
    return obj

def get_device_info(roku_ip: str) -> dict:
    """Return parsed device-info dict from Roku."""
    raw_xml = send_request(roku_ip, "query/device-info")
    if not raw_xml:
        return {}
    try:
        return convert_basic_types(xmltodict.parse(raw_xml))
    except xmltodict.expat.ExpatError:
        return {"response": raw_xml}
