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
    """Return parsed device-info dict from Roku"""
    raw_xml = send_request(roku_ip, "query/device-info")
    if not raw_xml:
        return {}
    try:
        return convert_basic_types(xmltodict.parse(raw_xml))
    except xmltodict.expat.ExpatError:
        return {"response": raw_xml}
    
def get_app_info(roku_ip: str) -> list[dict]:
    """Return parsed app info list from Roku"""
    raw_xml = send_request(roku_ip, "query/apps")
    if not raw_xml:
        return []
    try:
        parsed_dict = convert_basic_types(xmltodict.parse(raw_xml))
        app_list = parsed_dict['apps']['app']
        result = []
        for app in app_list:
            result.append({
                'text': app['#text'],
                'id': app['@id'],
                'type': app['@type'],
                'version': app['@version']
            })
        return sorted(result, key=lambda x: x['text'])
    except xmltodict.expat.ExpatError:
        return []

def launch_app(roku_ip: str, app_id: int):
    """Launch an app with a particular ID"""
    send_request(roku_ip, f'launch/{app_id}', params={}, method='POST')