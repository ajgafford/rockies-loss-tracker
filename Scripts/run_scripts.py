import subprocess
import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))

scrape_games_path = os.path.join(base_dir, 'scrape_games.py')
merge_schedules_path = os.path.join(base_dir, 'merge_schedules.py')
app_path = os.path.join(base_dir, '../app.py')

subprocess.run([sys.executable, scrape_games_path], check=True)
subprocess.run([sys.executable, merge_schedules_path], check=True)
subprocess.run([sys.executable, app_path], check=True)