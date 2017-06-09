import argparse, binascii, sqlite3, sys, os
from modules.utils import colored


__doc__ = ""
term_size = os.get_terminal_size().columns

def hexdump(data: bytes, prefix=""):
    for b in range(0, len(data), 16):
        try:
            line = [char for char in data[b: b + 16]]
            print(colored(prefix + "{:04x}: {:48} |{}|".format(b, " ".join(f"{char:02x}" for char in line), "".join((chr(char) if 32 <= char <= 126 else ".") for char in line)), dark=True))
        except KeyboardInterrupt:
            print(colored("[!] Keyboard Interrupted! (Ctrl+C Pressed)", "red"))
            break

def parse_args(args: list = sys.argv[1:]):
    parser = argparse.ArgumentParser("vir-s", description=__doc__)
    parser.add_argument("directory", type=str, help="Directory to be scanned.")
    args = parser.parse_args(args)
    
    virus_db = sqlite3.connect(os.path.join(os.path.abspath(os.path.dirname(__file__)), "resources/virus-signatures.db"))
    viruses = virus_db.cursor()
    print(colored(f"[i] Virus Signature database currently have {sum(list(viruses.execute('SELECT COUNT(*) FROM signatures'))[0])} valid signatures ..."))
    
    for dirpath, dirnames, filenames in os.walk(os.path.abspath(args.directory)):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename).replace("\\", "/")
            print(colored(f"[i] Checking {repr(filepath[:term_size - 25] + ('[...]' if len(filepath) > term_size - 25 else ''))}".ljust(term_size - 1)), end="\r")
            for name, signature in viruses.execute("select name, signature from signatures"):
                signature = binascii.unhexlify(signature)
                sig_size = len(signature)
                try:
                    file = open(filepath, "rb")
                    data = file.read(512 + sig_size)
                    file.close()
                    if data.startswith(signature):
                        print(colored(f"[!] {repr(name)} have been detected:".ljust(term_size - 1)))
                        print(colored(f" -  File: ") + colored(f"{repr(filepath)}", dark=True))
                        print(colored(f" -  Signature: ({sig_size} bytes)"))
                        hexdump(signature, "    ")
                        first_bytes = data[sig_size:]
                        print(colored(f" -  First {len(first_bytes)} bytes of file (from byte #{sig_size} to #{len(first_bytes)}):"))
                        hexdump(first_bytes, "    ")
                        print("")
                        print(colored(f"[?] Do you want to delete this malicious file from your computer ?", "yellow"))
                        print(colored(" -  Enter 'Y' or 'Yes' (without quotes) to confirm.", "yellow", True))
                        try:
                            if input(colored(">>> ", "yellow")).lower() in ["y", "yes"]:
                                os.remove(filepath)
                                print(colored("[i] Malicious file successfully deleted!", "green"))
                        except Exception as e:
                            print(colored(f"[!] {type(e).__name__}:", "red"))
                            print(colored(f" -  {e}", "red", True))
                        print("")
                except KeyboardInterrupt:
                    print(colored("[!] Keyboard Interrupted!", "red").ljust(term_size - 1))
                    exit()
                except:
                    pass
    viruses.close()


if __name__ == "__main__":
    parse_args()
