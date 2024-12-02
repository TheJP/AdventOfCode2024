from datetime import datetime
import os
import shutil
import subprocess
import sys
import time
import requests
from bs4 import BeautifulSoup
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

YEAR = "2024"
SESSION_FILE = ".session.private"
TEMPLATE_FILE = ".template.py.private"

# Day
day = datetime.now().day
print(f"day? [{day}] ", end="", flush=True)

input = sys.stdin.readline().strip()
if input.isdecimal() and 1 <= int(input) and int(input) <= 25:
    day = int(input)
elif input.strip() != "":
    print("< invalid input")
    exit(1)

# Session
if not os.path.isfile(SESSION_FILE):
    print(f"session-key? (or set in '{SESSION_FILE}' and re-run)\n$ ", end="", flush=True)
    session = sys.stdin.readline().strip()
    if len(session) < 64:
        print("invalid session")
        exit(1)

    with open(SESSION_FILE, mode="w", encoding="utf-8") as f:
        f.write(session)

with open(SESSION_FILE, encoding="utf-8") as f:
    session = f.read().strip()

# Create Files (1)
print("> creating files")
day_dir = f"day{day:02}"
os.makedirs(day_dir, exist_ok=True)
if not os.path.isfile(f"{day_dir}/one.py"):
    shutil.copy2(TEMPLATE_FILE, f"{day_dir}/one.py")
# for file_name in ["example.in", "task.in", "one.py"]:
#     os.system(f"touch {day_dir}/{file_name} && code {day_dir}/{file_name}")

url = f"https://adventofcode.com/{YEAR}/day/{day}"
def fetch(url) -> requests.Response:
    global session
    print(f"> fetching '{url}'")
    response = requests.get(url, cookies={ "session": session })

    if response.status_code < 200 or 300 <= response.status_code:
        print(f"< failed: status code == {response.status_code}")
        print("< response:")
        print(response.text.strip())
        exit(2)

    return response

# Fetch Input
input_url = f"{url}/input"
response = fetch(input_url)
with open(f"{day_dir}/task.in", mode="w", encoding="utf-8") as f:
    f.write(response.text)

# Fetch Task
response = fetch(url)
bs = BeautifulSoup(response.content, "lxml")
# bs = BeautifulSoup(response.content, "html.parser")  # <-- without lxml requirement

def find_example(part):
    # Result of Example
    example_result = None
    for code in reversed(part.find_all("code")):
        if len(code.contents) == 1 and code.contents[0].name == "em":
            example_result = code.get_text()
            break

    print(f"example result? {'' if example_result is None else f'[{example_result}] '}", end="", flush=True)
    input = sys.stdin.readline().strip()
    if input != "":
        example_result = input

    # Example
    example = None
    for code in part.find_all("pre"):
        if len(code.contents) != 1 or code.contents[0].name != "code":
            continue
        if code.previous_sibling is None:
            continue

        if "for example" in code.find_previous_sibling("p").get_text().lower():
            example = code.get_text()
            print("< found example")
            print(example)
            with open(f"{day_dir}/example.in", mode="w", encoding="utf-8") as f:
                f.write(example)
            break

    if example is None:
        print("< failed to find example")

    return example_result

parts = bs.find_all("article", class_="day-desc")
example_result_1 = find_example(parts[0])

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, path: str) -> None:
        self.path = path
        self.last_run = time.time()

    def on_any_event(self, event: FileSystemEvent) -> None:
        global day_dir, example_result_1

        if event.event_type != "modified":
            return
        if not os.path.samefile(self.path, event.src_path):
            return

        now = time.time()
        if now - self.last_run < 1:
            return
        self.last_run = now

        print(f"> run '{self.path}' example.in")
        result = subprocess.run(["python", self.path, os.path.join(day_dir, "example.in")], stdout=subprocess.PIPE)
        output = result.stdout.decode("utf-8").strip()
        print(output)
        if output == example_result_1:
            print(f"> run '{self.path}' task.in")
            result = subprocess.run(["python", self.path, os.path.join(day_dir, "task.in")], stdout=subprocess.PIPE)
            output = result.stdout.decode("utf-8").strip()
            print(output)

event_handler = MyEventHandler(f"{day_dir}/one.py")
observer = Observer()
observer.schedule(event_handler, day_dir, recursive=True)
observer.start()
try:
    while True:
        if sys.stdin.readable():
            command = sys.stdin.readline().strip()
            if command in ["q", "quit"]:
                exit(0)
            if command in ["s", "submit"]:
                break
        time.sleep(0.01)
finally:
    observer.stop()
    observer.join()

if command in ["s", "submit"]:
    print("< submit solution")
