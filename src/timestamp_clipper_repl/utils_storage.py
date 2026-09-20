from dataclasses import dataclass, field, asdict
import datetime
import re
from pathlib import Path
import json

duration_type = datetime.timedelta
duration_pattern = re.compile(
    r"(?:(?P<h>\d\d):)?(?P<m>\d\d):(?P<s>\d\d)(?:.(?P<ms>\d\d\d))?"
    # ( ... ) is a capture group
    # (?P<name> ... ) is a named capture group
    # (?: ... ) is a non-capture group
    # (?: ... )? is an optional non-capture group
    # so basically, [hh:]mm:ss[.xxx] where x is a millisecond digit
)

def duration_from_str(duration_str):
    parsed = duration_pattern.match(duration_str)
    if parsed is not None:
        parsed_dict = parsed.groupdict()
        h = parsed_dict["h"]
        h = int(h) if h is not None else 0
        m = int(parsed_dict["m"])
        s = int(parsed_dict["s"])
        ms = parsed_dict["ms"]
        ms = int(ms) if ms is not None else 0
        result = duration_type(
                hours=h,
                minutes=m,
                seconds=s,
                milliseconds=ms
            )
    else:
        result = None
    return result

@dataclass
class ClipRange:
    start: duration_type | None = None
    end: duration_type | None = None
    filename: str | None = None

    def as_dict(self):
        result = asdict(self)
        result["start"] = str(result["start"]) if result["start"] else None
        result["end"] = str(result["end"]) if result["end"] else None
        return result

@dataclass
class Inventory:
    inventory_path: Path | None = None
    media_path: Path | None = None
    export_path: Path | None = None
    clips: list[ClipRange] = field(default_factory=list)

    def as_dict(self):
        result = {
                "inventory_path":
                    str(self.inventory_path)
                        if self.inventory_path
                    else None,
                "media_path":
                    str(self.media_path)
                        if self.media_path
                    else None,
                "export_path":
                    str(self.export_path)
                        if self.export_path
                    else None,
                "clips": [clip.as_dict() for clip in self.clips]
            }
        return result

    def as_dict_precise(self):
        result = asdict(self)
        return result

    def overwrite(self, target_path: Path):
        data = self.as_dict()
        del data["inventory_path"]
        with open(target_path, "w") as f:
            json.dump(data, f, indent=4)
    
    def load(self, source_path: Path):
        success = False
        backup = self.as_dict_precise()
        with open(source_path, "r") as f:
            data = json.load(f)
        try:
            self.inventory_path = source_path
            self.media_path = data["media_path"]
            self.export_path = data["export_path"]
            self.clips = []
            for clip_dict in data["clips"]:
                new_clip = ClipRange(
                        start = duration_from_str(clip_dict["start"]),
                        end = duration_from_str(clip_dict["end"]),
                        filename = clip_dict["filename"]
                    )
                self.clips.append(new_clip)
            success = True
        except:
            self.inventory_path = backup["inventory_path"]
            self.media_path = backup["media_path"]
            self.export_path = backup["export_path"]
            self.clips = backup["clips"]
        return success

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
            print("No folder selected for saving clips")

        if self.clips:
            print("Timestamps (format: hh:mm:ss.000):")
            for idx, clip in enumerate(self.clips):
                print(f"Clip no. {idx+1}")
                print("    Start timestamp :", clip.start)
                print("    End timestamp   :", clip.end)
                print("    To be saved as  :", clip.filename)
        else:
            print("No timestamps yet")

    def add_clip(self, start, end, filename):
        success = True
        try:
            new_clip = ClipRange(start, end, filename)
        except:
            success = False
        else:
            self.clips.append(new_clip)
        return success

    def len_clips(self):
        return len(self.clips)
