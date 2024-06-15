import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileCreatedHandler1(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"Файл створено: {event.src_path}")
            self.run_script()

    def run_script(self):
        try:
            subprocess.run(["python", "method_1.py"], check=True)
            print("Скрипт успішно запущений")
        except subprocess.CalledProcessError as e:
            print(f"Помилка при запуску скрипта: {e}")

class FileCreatedHandler2(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"Файл створено: {event.src_path}")
            self.run_script()

    def run_script(self):
        try:
            subprocess.run(["python", "method_2.py"], check=True)
            print("Скрипт успішно запущений")
        except subprocess.CalledProcessError as e:
            print(f"Помилка при запуску скрипта: {e}")

if __name__ == "__main__":
    path_1 = "C:\\Users\ACER\Desktop\НН ФТІ\Com. graf\Project\media_users\document_in\method1"
    path_2 = "C:\\Users\ACER\Desktop\НН ФТІ\Com. graf\Project\media_users\document_in\method2"

    event_handler_1 = FileCreatedHandler1()
    event_handler_2 = FileCreatedHandler2()

    observer_1 = Observer()
    observer_2 = Observer()

    observer_1.schedule(event_handler_1, path_1, recursive=False)
    observer_2.schedule(event_handler_2, path_2, recursive=False)

    observer_1.start()
    observer_2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer_1.stop()
        observer_2.stop()

    observer_1.join()
    observer_2.join()
