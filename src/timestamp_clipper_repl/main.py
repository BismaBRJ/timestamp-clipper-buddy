from .utils_storage import Inventory
from pathlib import Path
import subprocess

def main():
    inventory = Inventory()
    repl_is_running = True
    print("Hello from timestamp-clipper-repl!")
    while repl_is_running: 
        inventory.display()
        print("=== Actions ===")
        print("i: set inventory path")
        print("m: set media path")
        print("c: set folder for saving clips")
        print("n: new timestamp")
        print("e: edit timestamp")
        print("d: delete timestamp")
        print("r: run clipping")
        print("q: quit")
        next_action = input("Enter next action: ")
        if next_action[0] == "i":
            action_done = False
            while not action_done:
                given = input("Enter path for inventory, end in .json (or \"c\" to cancel): ")
                if (given == "c") or (given == "\"c\""):
                    break
                try:
                    inventory_path = Path(given)
                except:
                    print("Invalid path.")
                else:
                    if not inventory_path.suffix.lower() == ".json":
                        print("Please specify a .json file path (file doesn't have to exist yet)")
                    elif not inventory_path.is_file():
                        given = input("File doesn't exist yet. Create? (y/n): ")
                        if given[0].lower() == "y":
                            inventory_path.touch()
                            inventory.inventory_path = inventory_path
                            inventory.overwrite(inventory_path)
                            print("Inventory saved successfully.")
                        else:
                            print("Setting inventory path canceled.")
                        action_done = True
                    else:
                        print("File found! What now?")
                        print("l: load saved file")
                        print("o: overwrite saved file")
                        print("(anything else): cancel")
                        given = input("Enter action: ")
                        if given == "i":
                            success = inventory.load(inventory_path)
                            if success:
                                print("Inventory loaded successfully.")
                            else:
                                print("Loading failed, file likely corrupted.")
                        elif given == "o":
                            inventory.inventory_path = inventory_path
                            inventory.overwrite(inventory_path)
                            print("Inventory overwritten successfully.")
                        else:
                            print("Setting inventory path canceled.")
                        action_done = True
        elif next_action[0] == "q":
            repl_is_running = False
        else:
            print("Sorry, action unknown.")

if __name__ == "__main__":
    main()
