from .utils_storage import Inventory, duration_type, duration_from_str
from .utils_clipper import is_media_valid, run_clipper
from pathlib import Path
from pathvalidate import is_valid_filename 

def main():
    inventory = Inventory()
    repl_is_running = True
    print("Hello from timestamp-clipper-repl!")
    while repl_is_running: 
        inventory.display_inventory()
        print("=== Actions ===")
        print("i: set inventory path")
        print("m: set media path")
        print("c: set folder for saving clips")
        print("n: new timestamp")
        print("e: edit timestamp")
        print("d: delete timestamp")
        print("x: delete ALL timestamps")
        print("r: run clipping")
        print("q: quit")
        next_action = input("Enter next action: ")
        if next_action[0] == "i":
            action_done = False
            while not action_done:
                given = input("Enter path for inventory, end in .json (or \"c\" to cancel): ")
                if (given == "c") or (given == "\"c\""):
                    action_done = True
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
                            inventory_path.parent.mkdir(parents=True, exist_ok=True)
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
                        if given == "l":
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
        elif next_action[0] == "m":
            action_done = False
            while not action_done:
                given = input("Enter path for media file (or \"c\" to cancel): ")
                if (given == "c") or (given == "\"c\""):
                    action_done = True
                try:
                    media_path = Path(given)
                except:
                    print("Invalid path.")
                else:
                    if not media_path.is_file():
                        print("File doesn't exist.")
                    else:
                        print("File found! Checking validity...")
                        if is_media_valid(media_path):
                            print("Valid media file.")
                            inventory.media_path = media_path
                        else:
                            print("Invalid media file, may be corrupted.")
                        action_done = True
        elif next_action[0] == "c":
            action_done = False
            while not action_done:
                given = input("Enter path for saving clips (or \"c\" to cancel: ")
                if (given == "c") or (given == "\"c\""):
                    action_done = True
                try:
                    clips_path = Path(given)
                except:
                    print("Invalid path.")
                else:
                    if not clips_path.is_dir():
                        given = input("Folder doesn't exist yet. Create? (y/n): ")
                        if given[0].lower() == "y":
                            clips_path.mkdir(parents=True, exist_ok=True)
                            inventory.export_path = clips_path
                            print("Folder created.")
                        else:
                            print("Setting clips path canceled.")
                    else:
                        print("Folder found.")
                        inventory.export_path = clips_path
                    action_done = True
        elif next_action[0] == "n":
            action_done = False
            start = duration_type()
            end = duration_type()
            filename = ""
            while not action_done:
                input_start_done = False
                while not input_start_done:
                    print("Timestamp format: [hh:]mm:ss[.xxx]")
                    print("h: hours (optional)")
                    print("m: minutes")
                    print("s: seconds")
                    print("x: milliseconds (optional)")
                    given = input("Enter start timestamp (or \"c\" to cancel): ")
                    if (given == "c") or (given == "\"c\""):
                        action_done = True
                        input_start_done = True
                    else:
                        parsed = duration_from_str(given)
                        if parsed is not None:
                            start = parsed
                            print("Start timestamp set to", str(start))
                            input_start_done = True
                        else:
                            print("Invalid timestamp.")
                input_end_done = False
                while (not input_end_done) and (not action_done):
                    print("Timestamp format: [hh:]mm:ss[.xxx]")
                    print("h: hours (optional)")
                    print("m: minutes")
                    print("s: seconds")
                    print("x: milliseconds (optional)")
                    given = input("Enter end timestamp (or \"c\" to cancel): ")
                    if (given == "c") or (given == "\"c\""):
                        action_done = True
                        input_end_done = True
                    else:
                        parsed = duration_from_str(given)
                        if parsed is not None:
                            if start < parsed:
                                end = parsed
                                print("End timestamp set to", str(end))
                                input_end_done = True
                            else:
                                print(f"End timestamp must be after start ({str(start)}).")
                        else:
                            print("Invalid timestamp.")
                input_filename_done = False
                while (not input_filename_done) and (not action_done):
                    print("File extension will be the same as the original media.")
                    given = input("Enter filename without extension (or \"/\" to cancel): ")
                    if (given == "/") or (given == "\"/\""):
                        action_done = True
                        input_filename_done = True
                    elif is_valid_filename(given):
                        filename = given
                        print("Filename set to:", filename)
                        input_filename_done = True
                    else:
                        print("Invalid filename. Check for forbidden characters or reserved keywords.")
                if not action_done:
                    success = inventory.add_clip(start, end, filename)
                    if success:
                        action_done = True
                        print("Timestamp added!")
                    else:
                        print("Adding timestamp failed.")
        elif next_action[0] == "e":
            action_done = False
            len_clips = len(inventory.clips)
            if len_clips == 0:
                print("No timestamps yet! Add a new one instead.")
                action_done = True
            while not action_done:
                clip = None
                select_done = False
                while not select_done:
                    print("Here are the stored clips:")
                    inventory.display_clips()
                    given = input(f"Enter clip number from 1 to {len_clips} (or \"c\" to cancel): ")
                    clip_no = None
                    if (given == "c") or (given == "\"c\""):
                        select_done = True
                        action_done = True
                    else:
                        try:
                            clip_no = int(given)
                            clip_idx = clip_no - 1
                            if clip_idx < 0:
                                raise IndexError
                            clip = inventory.clips[clip_idx]
                        except ValueError:
                            print("Please enter a number.")
                        except IndexError:
                            print(f"Clip no. {clip_no} doesn't exist!")
                        else:
                            print(f"Clip no. {clip_no} selected.")
                            select_done = True
                edit_done = False
                while (not edit_done) and (not action_done):
                    if clip is None:
                        print("Clip doesn't exist; selection error occurred.")
                        edit_done = True
                    else:
                        clip.display(prepend=("1. ", "2. ", "3. "))
                        given = input("Select field to edit (1/2/3): ")
                        if given == "1":
                            replace_done = False
                            while not replace_done:
                                print("Timestamp format: [hh:]mm:ss[.xxx]")
                                print("h: hours (optional)")
                                print("m: minutes")
                                print("s: seconds")
                                print("x: milliseconds (optional)")
                                print("Old start timestamp:", str(clip.start))
                                given = input("Enter new start timestamp (or \"c\" to cancel): ")
                                if (given == "c") or (given == "\"c\""):
                                    replace_done = True
                                else:
                                    parsed = duration_from_str(given)
                                    if parsed is not None:
                                        if (clip.end is not None) and (parsed >= clip.end):
                                            print(f"Start timestamp must be before end ({str(clip.end)}).")
                                        else:
                                            clip.start = parsed
                                            print("Start timestamp set to", str(parsed))
                                            replace_done = True
                                    else:
                                        print("Invalid timestamp.")
                        elif given == "2":
                            replace_done = False
                            while not replace_done:
                                print("Timestamp format: [hh:]mm:ss[.xxx]")
                                print("h: hours (optional)")
                                print("m: minutes")
                                print("s: seconds")
                                print("x: milliseconds (optional)")
                                print("Old end timestamp:", str(clip.end))
                                given = input("Enter new end timestamp (or \"c\" to cancel): ")
                                if (given == "c") or (given == "\"c\""):
                                    replace_done = True
                                else:
                                    parsed = duration_from_str(given)
                                    if parsed is not None:
                                        if (clip.start is not None) and (clip.start >= parsed):
                                            print(f"End timestamp must be after start ({str(clip.start)}).")
                                        else:
                                            clip.end = parsed
                                            print("End timestamp set to", str(parsed))
                                            replace_done = True
                                    else:
                                        print("Invalid timestamp.")
                        elif given == "3":
                            replace_done = False
                            while not replace_done:
                                print("File extension will be the same as the original media.")
                                print("Old filename:", str(clip.filename))
                                given = input("Enter new filename without extension (or \"/\" to cancel): ")
                                if (given == "/") or (given == "\"/\""):
                                    replace_done = True
                                elif is_valid_filename(given):
                                    clip.filename = given
                                    print("Filename set to:", given)
                                    replace_done = True
                                else:
                                    print("Invalid filename. Check for forbidden characters or reserved keywords.")
                        else:
                            print("Unknown field.")
                        given = input("Edit another field? (y/n): ")
                        if given.lower() != "y":
                            edit_done = True
                if not action_done:
                    given = input("Edit another clip? (y/n): ")
                    if given.lower() != "y":
                        print("Returning to menu...")
                        action_done = True
        elif next_action[0] == "d":
            action_done = False
            len_clips = len(inventory.clips)
            if len_clips == 0:
                print("No timestamps yet!")
                action_done = True
            while not action_done:
                clip = None
                clip_idx = len_clips
                select_done = False
                while not select_done:
                    print("Here are the stored clips:")
                    inventory.display_clips()
                    given = input(f"Enter clip number from 1 to {len_clips} (or \"c\" to cancel): ")
                    clip_no = None
                    if (given == "c") or (given == "\"c\""):
                        select_done = True
                        action_done = True
                    else:
                        try:
                            clip_no = int(given)
                            clip_idx = clip_no - 1
                            if clip_idx < 0:
                                raise IndexError
                            clip = inventory.clips[clip_idx]
                        except ValueError:
                            print("Please enter a number.")
                        except IndexError:
                            print(f"Clip no. {clip_no} doesn't exist!")
                        else:
                            print(f"Clip no. {clip_no} selected.")
                            select_done = True
                if not action_done:
                    if clip is None:
                        print("Clip doesn't exist; selection error occurred.")
                    else:
                        print("Here is the selected clip:")
                        clip.display(prepend="    ")
                        if inventory.inventory_path is None:
                            print("Deletion cannot be undone!")
                        else:
                            print("Deletion cannot be undone and is immediately autosaved!")
                        given = input("Are you sure you want to delete it? (y/n): ")
                        if given.lower() == "y":
                            try:
                                del inventory.clips[clip_idx]
                            except:
                                print("Clip doesn't exist; selection error occurred.")
                            else:
                                print("Clip deleted.")
                        else:
                            print("Deletion canceled.")
                    given = input("Delete another clip? (y/n): ")
                    if given.lower() != "y":
                        action_done = True
        elif next_action[0] == "x":
            len_clips = len(inventory.clips)
            if len_clips == 0:
                print("No timestamps yet!")
            else:
                if inventory.inventory_path is None:
                    print("Clip deletion cannot be undone!")
                else:
                    print("Clip deletion cannot be undone and is immediately autosaved!")
                given = input("Are you sure you want to delete ALL timestamps? (y/n): ")
                if given.lower() == "y":
                    inventory.clips = []
                    print("All clips deleted.")
                else:
                    print("Mass deletion canceled. Phew!")
        elif next_action[0] == "r":
            len_clips = len(inventory.clips)
            if len_clips == 0:
                print("No timestamps yet!")
            elif inventory.media_path is None:
                print("No media selected yet!")
            elif inventory.export_path is None:
                print("No folder selected yet for saving clips!")
            else:
                print("Running clipper...")
                success = run_clipper(inventory)
                if success:
                    print("Clipping successful!")
                else:
                    print("Clipping failed; see error above.")
        elif next_action[0] == "q":
            repl_is_running = False
        else:
            print("Sorry, action unknown.")
        # Autosave
        if inventory.inventory_path is not None:
            inventory.overwrite(inventory.inventory_path)

if __name__ == "__main__":
    main()
