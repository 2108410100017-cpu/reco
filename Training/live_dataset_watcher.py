import time
import sys
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PY = sys.executable

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        # Only retrain when the CSV file changes, ignore metadata/embeddings
        if event.is_directory:
            return
        filename = os.path.basename(event.src_path)
        if filename == "styles.csv":
            print("Dataset changed → retrain")
            os.system(f"{PY} retrain.py")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(Handler(), path="myntradataset", recursive=True)
    observer.start()
    print("Watching for dataset changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
