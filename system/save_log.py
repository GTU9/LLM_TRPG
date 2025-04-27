import os
from datetime import datetime

def save_log(play_log):
    folder_path = "data"
    os.makedirs(folder_path, exist_ok=True)
    
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"log_{timestamp}.txt"
    file_path = os.path.join(folder_path, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(play_log)
