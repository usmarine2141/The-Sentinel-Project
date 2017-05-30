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
        self.exec = lambda command, args = []: loader.load(os.path.join(self.location, command + ".py")).parse_args(args)
        if readline:
            readline.set_completer(self.complete)
            readline.parse_and_bind("tab: complete")
        print(colored(intro.format(**locals()), "green"))
        self.exec("help")
    
    def scripts(self):
        scripts = set()
        for name in os.listdir(self.location):
            if name.lower().endswith(".py"):
                try:
                    module = loader.load(os.path.join(self.location, name))
                    name = name.rsplit(".", 1)[0]
                    if hasattr(module, "parse_args"):
                        scripts.add(name.lower())
                except:
                    pass
        return scripts
    
    def loop(self):
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
            except SystemExit:
                pass
            except Exception as e:
                print(f"[!] {type(e).__name__}:")
                if str(e):
                    print(f" -  {e}")
    
    def complete(self, text: str, state: int):
        if state == 0:
            if text:
                self.matches = [s for s in self.scripts() if s.startswith(text)]
            else:
                self.matches = list(self.scripts())
        try:
            return self.matches[state]
        except IndexError:
            return None

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
        c.loop()
    except Exception as e:
        print(colored(f"[!] {type(e).__name__}:", "red"))
        print(colored(f" -  {e}", "red", True))
