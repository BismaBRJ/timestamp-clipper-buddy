from pathlib import Path
import subprocess

def is_media_valid(media_path: Path) -> bool:
    command = [
            "ffmpeg",
            "-v", "quiet",
            "-i", str(media_path),
            "-c", "copy",
            "-f", "null", "-"
        ]
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
