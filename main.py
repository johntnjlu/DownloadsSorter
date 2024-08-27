import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directories to be watched and sorted
watched_dir = r'/Users/johnt/Downloads'
images_dir = r'/Users/johnt/Pictures'
documents_dir = r'/Users/johnt/Documents/Files'
music_dir = r'/Users/johnt/Music'
# File type categories
images = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
documents = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'}
music = {'.mp3', '.wav'}
category = {'images': images, 'documents': documents, 'music': music}

category_dirs = {'images': images_dir, 'documents': documents_dir, 'music': music_dir}

class FileSorterHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.sort_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.sort_file(event.src_path)

    def sort_file(self, file_path):
        # Ignore .DS_Store files
        if os.path.basename(file_path) == '.DS_Store':
            return
        
        _, file_extension = os.path.splitext(file_path)
        file_name = os.path.basename(file_path)
        file_extension = file_extension.lower()
        
        for category_name, extensions in category.items():
            if file_extension in extensions:
                target_dir = category_dirs[category_name]
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                shutil.move(file_path, os.path.join(target_dir, file_name))
                print(f"Moved '{file_path}' to '{target_dir}'")
                break

def start_watching():
    event_handler = FileSorterHandler()
    observer = Observer()
    observer.schedule(event_handler, watched_dir, recursive=False)
    observer.start()
    print(f"Watching directory: {watched_dir}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watching()