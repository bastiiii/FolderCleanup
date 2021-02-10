from watchdog.observers import Observer
import time
from watchdog.events import FileSystemEventHandler
import os
from pathlib import Path

# folder that should be tracked
folder_to_track = "/Users/Basti/Downloads/"

# documents
document_destination = folder_to_track + "Dokumente"
document_extensions = [".doc", ".docx", ".txt", ".pdf", ".xls", ".xlsx", ".ppt"]

# images
image_destination = folder_to_track + "Bilder"
image_extensions = [".png", ".jpg", ".jpeg", ".bmp", ".heic"]

# install files
install_destination = folder_to_track + "Installer"
install_extensions = [".dmg"]

# video files
video_destination = folder_to_track + "Videos"
video_extensions = [".avi", ".mov", ".mp4"]

def main():
    # create folders if not existent
    create_folders_if_dont_exist()

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

class MyHandler(FileSystemEventHandler):
    i = 1
    def on_modified(self, event):
        for filename in os.listdir(folder_to_track):
            src = folder_to_track + "/" + filename
            if filename.lower().endswith(tuple(document_extensions)):
                filename = validate_filename(document_destination, filename)
                new_destination = document_destination + "/" + filename             
                os.rename(src, new_destination)
            elif filename.lower().endswith(tuple(image_extensions)):  
                filename = validate_filename(image_destination, filename)             
                new_destination = image_destination + "/" + filename
                os.rename(src, new_destination)
            elif filename.lower().endswith(tuple(install_extensions)): 
                filename = validate_filename(install_destination, filename)              
                new_destination = install_destination + "/" + filename
                os.rename(src, new_destination)
            elif filename.lower().endswith(tuple(video_extensions)):  
                filename = validate_filename(video_destination, filename)             
                new_destination = video_destination + "/" + filename
                os.rename(src, new_destination)

def validate_filename(path_to_folder, filename):
    path = path_to_folder + "/" + filename
    if Path(path).is_file():
        print(f"{path_to_folder} contains {filename}")
        return "copy_" + filename 
    else:
        return filename

def create_folders_if_dont_exist():
        if not os.path.exists(image_destination):
            os.makedirs(image_destination)
        if not os.path.exists(document_destination):
            os.makedirs(document_destination)
        if not os.path.exists(install_destination):
            os.makedirs(install_destination) 
        if not os.path.exists(video_destination):
            os.makedirs(video_destination) 

if __name__ == '__main__':
    main()