from .utils_storage import Inventory
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
        if next_action[0] == "q":
            repl_is_running = False
        else:
            inventory.execute(next_action)

if __name__ == "__main__":
    main()
