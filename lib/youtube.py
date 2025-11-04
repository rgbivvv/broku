import re
import logging
from typing import Optional
from .roku_request import send_request

logger = logging.getLogger(__name__)

YOUTUBE_APP_ID = "837"
YOUTUBE_ID_RE = re.compile(
    r"""(?x)
    (?:v=|/v/|youtu\.be/|/embed/|/watch\?.*v=)?
    (?P<id>[A-Za-z0-9_-]{11})
    """
)

def extract_youtube_id(s: str) -> Optional[str]:
    s = s.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s):
        return s
    m = YOUTUBE_ID_RE.search(s)
    if m:
        return m.group("id")
    return None

def launch_youtube(roku_ip: str, video_or_url: str) -> bool:
    vid = extract_youtube_id(video_or_url)
    if not vid:
        logger.error(f"Could not extract YouTube ID from {video_or_url}")
        return False
    logger.info(f"Launching YouTube video {vid} on Roku {roku_ip}")
    send_request(roku_ip, f"launch/{YOUTUBE_APP_ID}", params={"contentID": vid}, method="POST")
    return True
