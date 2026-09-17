from dataclasses import dataclass, field, asdict
import datetime
from pathlib import Path
import subprocess

duration_type = datetime.timedelta

@dataclass
class ClipRange:
    start: duration_type
    end: duration_type
    filename: str

@dataclass
class Inventory:
    inventory_path: Path | None = None
    media_path: Path | None = None
    export_path: Path | None = None
    clips: list[ClipRange] = field(default_factory=list)

    def display(self):
        print("=== Inventory of timestamps ===")
        if self.inventory_path:
            print("Inventory autosaved at:", str(self.inventory_path))
        else:
            print("Inventory not saved to a file")

        if self.media_path:
            print("Media to clip:", str(self.media_path))
        else:
            print("No media selected")

        if self.export_path:
            print("Clips set to be saved at:", str(self.export_path))
        else:
            print("No destination folder selected")

        if self.clips:
            print("Timestamps (format: hh:mm:ss.000):")
            for idx, clip in enumerate(self.clips):
                print(f"Clip no. {idx+1}")
                print("    Start timestamp :", clip.start)
                print("    End timestamp   :", clip.end)
                print("    To be saved as  :", clip.filename)
        else:
            print("No timestamps yet")

def main():
    inventory = Inventory()
    repl_is_running = True
    while repl_is_running: 
        print("Hello from timestamp-clipper-repl!")
        inventory.display()
        repl_is_running = False

if __name__ == "__main__":
    main()
