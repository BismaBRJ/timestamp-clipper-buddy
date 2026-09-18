from utils_storage import Inventory
import subprocess

def main():
    inventory = Inventory()
    repl_is_running = True
    while repl_is_running: 
        print("Hello from timestamp-clipper-repl!")
        inventory.display()
        repl_is_running = False

if __name__ == "__main__":
    main()
