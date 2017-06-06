import os, sys, argparse
from modules import loader
from modules.utils import colored
try:
    import readline
except:
    readline = None


class Console(object):
    def __init__(self, name: str = "", prompt: str = "", intro: str = "[i] Welcome to the {name} console!"):
        self.location = os.path.abspath(os.path.dirname(__file__))
        
        self.name = name
        self.prompt = prompt or f"#{name}> "
        self.exec = lambda command, args = []: loader.load(self.scripts()[command.lower()]).parse_args(args)
        if readline:
            readline.set_completer(self.complete)
            readline.parse_and_bind("tab: complete")
        print(colored(intro.format(**locals()), "green"))
        self.exec("help")
    
    def scripts(self):
        scripts = {}
        for name in sorted(set(os.listdir(self.location))):
            path = os.path.join(self.location, name)
            if not name.startswith("_") and name not in ["modules", "console.py"]:
                if os.path.isdir(path) and os.path.isfile(os.path.join(path, "main.py")):
                    path = os.path.join(path, "main.py")
                if os.path.isfile(path) and path.endswith(".py"):
                    try:
                        module = loader.load(path)
                        name = name.rsplit(".", 1)[0].lower()
                        if hasattr(module, "parse_args"):
                            scripts[name] = path
                    except:
                        pass
        return dict(sorted(set(scripts.items()), key=lambda x: x[0]))
    
    def complete(self, text: str, state: int):
        text = text.lstrip()
        words = text.split(" ")
        if state == 0:
            self.matches = [s for s in self.scripts() if s.startswith(text)]
            words = readline.get_line_buffer().split()
            if len(words) >= 2:
                if "/" in words[-1] or "\\" in words[-1]:
                    path = os.path.abspath(words[-1]).replace("\\", "/")
                    if os.path.isdir(path):
                        directory = path
                        filename = ""
                    else:
                        directory = os.path.dirname(path)
                        filename = os.path.basename(path)
                    self.matches += [name for name in os.listdir(directory) if name.startswith(filename)]
        try:
            return self.matches[state]
        except IndexError:
            return None
    
    def interact(self):
        while True:
            try:
                command, *args = input("\n" + colored(self.prompt, "yellow")).strip().split(" ")
                command = command.lower()
                args = [arg.strip() for arg in args if arg.strip()]
                if command:
                    if command in self.scripts():
                        self.exec(command, args)
                    else:
                        raise ValueError(f"{repr(command)} is not recognized as an internal command or script ...")
            except SystemExit:
                pass
            except KeyboardInterrupt as e:
                print("\n" + colored(f"[!] Are you sure you want to quit {self.name}? (enter 'Y' to confirm)", "yellow"))
                _quit = False
                while True:
                    try:
                        if input(colored(">>> ", "yellow", True)).strip().lower() == "y":
                            _quit = True
                        break
                    except:
                        pass
                if _quit:
                    break
            except Exception as e:
                print(colored(f"[!] {type(e).__name__}:", "red"))
                if str(e):
                    print(colored(f" -  {e}", "red", True))


if __name__ == "__main__":
    try:
        c = Console("Sentinella", intro="""
      _________              __  .__              .__  .__          
     /   _____/ ____   _____/  |_|__| ____   ____ |  | |  | _____   
     \_____  \_/ __ \ /    \   __\  |/    \_/ __ \|  | |  | \__  \  
     /        \  ___/|   |  \  | |  |   |  \  ___/|  |_|  |__/ __ \_
    /_______  /\___  >___|  /__| |__|___|  /\___  >____/____(____  /
            \/     \/     \/             \/     \/               \/
            
                    We can see you ...
    """)
        c.interact()
    except Exception as e:
        print(colored(f"[!] {type(e).__name__}:", "red"))
        print(colored(f" -  {e}", "red", True))
