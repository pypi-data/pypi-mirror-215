import json
import re
from . import maening
def name_search(name):
    c = 0
    text = ""
    for item in maening.name_maening:
        if re.search(str(name), item["word"], re.IGNORECASE):
            text += f"{item['word']} - {item['example']}\n\n"
            if text.count('-') > 10:
                return text
    return text
#Qqk_sAamgR%T.89
