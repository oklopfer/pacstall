import os
import json
from git import Repo
from datetime import datetime, timezone

# Path to the JSON file storing tag names and hex codes
json_file_path = 'hexes.json'

# Load the dictionary from the JSON file
if os.path.exists(json_file_path):
    with open(json_file_path, 'r') as file:
        tag_hex_codes = json.load(file)

def list_tag_durations(repo_path):
    global tag_hex_codes  # Use the global dictionary
    repo = Repo(repo_path)
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)

    if not tags:
        print("No tags found in the repository.")
        return

    tag_info = []
    now = datetime.now(timezone.utc)

    for i, tag in enumerate(tags):
        tag_date = tag.commit.committed_datetime
        tag_name = tag.name
        if i < len(tags) - 1:
            next_tag_date = tags[i + 1].commit.committed_datetime
            duration = next_tag_date - tag_date
        else:
            duration = now - tag_date
            if tag_name not in tag_hex_codes or tag_hex_codes[tag_name] == ("", ""):
                name = input(f"Name for {tag_name}: ")
                hex_code = input(f"Hex for {tag_name}: ")
                tag_hex_codes[tag_name] = (name, hex_code)
        
        tag_info.append((tag_name, tag_date, duration, tag_hex_codes[tag_name]))

    print(f"{'Release':<10} {'Name':<20} {'Hex Code':<10} {'Lifespan'}")
    for i, info in enumerate(tag_info):
        tag_name, tag_date, duration, (name, hex_code) = info
        if i == len(tag_info) - 1:
            duration_str = "Current"
        else:
            total_seconds = int(duration.total_seconds())
            days, remainder = divmod(total_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            day_str = f"{days}d"
            if len(day_str) == 2:
                day_str += "  "
            elif len(day_str) == 3:
                day_str += " "
            duration_str = f"{day_str} {hours:02}h {minutes:02}m {seconds:02}s"
        print(f"{tag_name:<10} {name:<20} {hex_code:<10} {duration_str}")

    # Save the updated dictionary back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(tag_hex_codes, file, indent=4)

if __name__ == "__main__":
    repo_path = os.getcwd()
    if os.path.exists(repo_path) and os.path.isdir(repo_path):
        list_tag_durations(repo_path)
    else:
        print("Invalid repository path.")
