import sys, os

global colorama, termcolor
try:
    import colorama, termcolor
    colorama.init(autoreset=True)
except Exception as e:
    termcolor = colorama = None

__all__ = ["colored", "pprint"]
__doc__ = "Basic terminal utils ..."
term_size = os.get_terminal_size().columns


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
                    value = str(value)
                    text = ""
                    for word in value.split():
                        if len(word) < term_size and len(text.split("\n")[-1]) >= term_size - (len(key) + len(prefix) + 2) or len(text.split("\n")[-1] + word + " ") >= term_size - (len(key) + len(prefix) + 2):
                            text += "\n" + (" " * (len(key) + 2 + len(prefix)))
                        text += word + " "
                    print(colored(f"{prefix}{key}: ", color) + colored(f"{text}", color, dark))
    elif isinstance(obj, (tuple, list, set)):
        for value in obj:
            pprint(value, depth, check, color, dark, title)
            if isinstance(value, dict):
                print("")
    else:
        if check(obj):
            obj = str(obj)
            text = ""
            for word in obj.split():
                if len(word) < term_size and len(text.split("\n")[-1]) >= term_size - (len(prefix) + 2) or len(text.split("\n")[-1] + word + " ") >= term_size - (len(prefix) + 2):
                    text += "\n" + (" " * len(prefix))
                text += word + " "
            print(colored(f"{prefix}{text}", color, dark))
