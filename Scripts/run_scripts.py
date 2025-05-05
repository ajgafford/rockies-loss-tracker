import subprocess

subprocess.run(["/usr/bin/python3", "/Users/ajgafford/Documents/Projects/Reached_on_Error/Rockies_Loss_Tracker/Scripts/scrape_games.py"])
subprocess.run(["/usr/bin/python3", "/Users/ajgafford/Documents/Projects/Reached_on_Error/Rockies_Loss_Tracker/Scripts/merge_schedules.py"])
subprocess.run(["streamlit", "run", "/Users/ajgafford/Documents/Projects/Reached_on_Error/Rockies_Loss_Tracker/Scripts/rockies_tracker.py"])
