import pyperclip
from urllib.parse import urlparse
from easygui import enterbox
import sys


def askURL():
    if not pyperclip.is_available():
        txt = pyperclip.paste()
    else:
        txt = ''
    url = enterbox(
        title='',
        msg='Enter Youtube URL',
        strip=True,
        default=txt if urlparse(txt).netloc.endswith('youtube.com') else ''
    )
    if url is None:
        sys.exit('Cancelled')
    return url

