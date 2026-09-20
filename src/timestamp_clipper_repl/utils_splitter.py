from pathlib import Path
import subprocess
from .utils_storage import Inventory

def is_media_valid(media_path: Path) -> bool:
    command = (
            "ffmpeg",
            "-v", "quiet",
            "-i", str(media_path),
            "-c", "copy",
            "-f", "null", "-"
        )
    is_valid = True
    if not media_path.is_file():
        is_valid = False
    else:
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            return_code = e.returncode
            if return_code != 0:
                is_valid = False
    return is_valid

def run_clipper(inventory: Inventory):
    success = True
    if (inventory.media_path is None) or (inventory.export_path is None):
        success = False
    else:
        file_extension = inventory.media_path.suffix
        command_intro = (
                "ffmpeg",
                "-v", "error",
                "-i", str(inventory.media_path)
            )
        command_rest = (
                ("-ss", str(c.start), "-to", str(c.end),
                 "-c", "copy",
                 str(inventory.export_path / c.filename) + file_extension)
                for c in inventory.clips
                if c.filename is not None
            )
        command = sum(command_rest, command_intro)
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            return_code = e.returncode
            if return_code != 0:
                success = False
    return success
