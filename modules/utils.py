import sys

global colorama, termcolor
try:
    import colorama, termcolor
    colorama.init(autoreset=True)
except Exception as e:
    termcolor = colorama = None

__all__ = ["colored", "pprint"]
__doc__ = "Basic terminal utils ..."


def colored(text, color="", dark=False):
    try:
        return termcolor.colored(text, color or "white", attrs=["dark"] if dark else [])
    except:
        return text

def pprint(obj, depth=0, check = None, color="", dark=True, title=True):
    if not check:
        check = lambda x: str(x).strip()
    prefix = ""
    if depth == 0:
        prefix = " -  "
    elif depth == 1:
        prefix = "    - "
    else:
        prefix = "    " + ("  " * (depth-1)) + "- "
    
    if isinstance(obj, dict):
        for key, value in obj.copy().items():
            if title:
                if key.islower():
                    key = key.replace("_", "-").title()
                elif "_" not in key:
                    key = f"{key[0].upper()}{key[1:]}"
            if check(value):
                if isinstance(value, (dict, list, tuple)):
                    print(colored(f"{prefix}{key}:", color))
                    pprint(value, depth+1, check, color, dark, title)
                else:
                    print(colored(f"{prefix}{key}: ", color) + colored(f"{value}", color, dark))
    elif isinstance(obj, (tuple, list)):
        for value in obj:
            pprint(value, depth, check, color, dark, title)
            print("")
    else:
        if check(obj):
            print(colored(f"{prefix}{obj}", color, dark))
