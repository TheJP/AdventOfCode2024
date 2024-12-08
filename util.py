from __future__ import annotations
from datetime import datetime
from datetime import time as dt_time
from enum import Enum
import os
import queue
import shutil
import subprocess
import sys
import threading
import time

from pytz import timezone
import requests
from bs4 import BeautifulSoup
from watchdog.events import DirModifiedEvent, FileModifiedEvent, FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

TIMEZONE = timezone("CET")
SESSION_FILE = ".session.private"
TEMPLATE_FILE = ".template.py.private"
EXAMPLE_FILE = "example.in"
EXAMPLE2_FILE = "example2.in"
TASK_FILE = "task.in"
LEVEL1_FILE = "one.py"
LEVEL2_FILE = "two.py"

auto_submit = True
done = False

# Day
if len(sys.argv) > 2:
    print(f"Usage: {sys.argv[0]} [[YEAR/]DAY]")
    exit(1)

now = datetime.now(TIMEZONE)
year, day = now.year, now.day
if len(sys.argv) == 2:
    input = sys.argv[1].strip()
    split_input = input.split("/")

    year_input = split_input[0]
    if len(split_input) == 2:
        if year_input.isdecimal() and 2015 <= int(year_input):
            year = int(year_input)
        else:
            print("< invalid year")
            exit(1)

    day_input = split_input[-1]
    if len(split_input) <= 2 and day_input.isdecimal() and 1 <= int(day_input) <= 25:
        day = int(day_input)
    elif input.strip() != "":
        print("< invalid day")
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
if not os.path.isfile(f"{day_dir}/{LEVEL1_FILE}") and os.path.isfile(TEMPLATE_FILE):
    shutil.copy2(TEMPLATE_FILE, f"{day_dir}/{LEVEL1_FILE}")
all_files = " ".join([f"{day_dir}/{file_name}" for file_name in [LEVEL1_FILE, EXAMPLE_FILE, TASK_FILE]])
os.system(f"touch {all_files} && code {all_files}")

url = f"https://adventofcode.com/{year}/day/{day}"
def fetch(url) -> requests.Response:
    global session

    while True:
        print(f"> fetching '{url}'")
        response = requests.get(url, cookies={ "session": session })

        if response.status_code == 404:
            now = datetime.now(TIMEZONE)
            start = datetime.combine(now, dt_time(hour=6), now.tzinfo)
            until_start = (start - now).total_seconds()
            if until_start <= 1:
                print("< 404 (retry right away)")
                time.sleep(0.1)
            else:
                print(f"< 404 (retry in {until_start:.1f}s)")
                time.sleep(until_start - 1)
            continue

        if 500 <= response.status_code < 600:
            print(f"< {response.status_code} (retry in 1s)")
            time.sleep(1)
            continue

        if not (200 <= response.status_code < 300):
            print(f"< failed: status code == {response.status_code}")
            print("< response:")
            print(response.text.strip())
            exit(2)

        return response

class SubmissionResult(Enum):
    CORRECT = 0
    INCORRECT = 1
    TOO_RECENT = 2
    WRONG_LEVEL = 3
    UNKNOWN = 4

    @staticmethod
    def from_response(response: str) -> SubmissionResult:
        if response.startswith("That's the right answer!"):
            return SubmissionResult.CORRECT
        elif response.startswith("That's not the right answer"):
            return SubmissionResult.INCORRECT
        elif response.startswith("You gave an answer too recently"):
            return SubmissionResult.TOO_RECENT
        elif response.startswith("You don't seem to be solving the right level"):
            return SubmissionResult.WRONG_LEVEL
        else:
            return SubmissionResult.UNKNOWN


def submit(solution: str, level: int) -> SubmissionResult:
    global url, session

    post_url = f"{url}/answer"
    while True:
        print(f"> posting '{post_url}'")
        data = {
            "level": str(level),
            "answer": solution,
            "submit": "[Submit]",
        }
        response = requests.post(post_url, data, cookies={ "session": session })

        if 500 <= response.status_code < 600:
            print(f"< {response.status_code} (retry in 1s)")
            time.sleep(1)
            continue

        if not (200 <= response.status_code < 300):
            print(f"< failed: status code == {response.status_code}")
            print("< response:")
            print(response.text.strip())
            exit(2)

        bs = BeautifulSoup(response.content, "lxml")
        response_text = bs.find("article").find("p").get_text().strip()
        response_type = SubmissionResult.from_response(response_text)
        print(f"< {response_type.name} '{response_text}'")

        return response_type

# Fetch Input
input_url = f"{url}/input"
response = fetch(input_url)
with open(f"{day_dir}/task.in", mode="w", encoding="utf-8") as f:
    f.write(response.text)

def find_example_result(part) -> str | None:
    # Result of Example
    example_result = None
    for code in reversed(part.find_all("code")):
        if len(code.contents) == 1 and code.contents[0].name == "em":
            example_result = code.get_text()
            break

    if example_result is None:
        print("example result? ", end="", flush=True)
        example_result = sys.stdin.readline().strip()

    print(f"< example result == '{example_result}'")
    return example_result

def find_example(part, filename: str) -> bool:
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
            with open(f"{day_dir}/{filename}", mode="w", encoding="utf-8") as f:
                f.write(example)
            break

    if example is None:
        print("< failed to find example")

    return example is not None

# Fetch Task
example_result_1 = None
example_result_2 = None
has_example_2 = False
level = 1

def scrape():
    global example_result_1, example_result_2, has_example_2, level

    response = fetch(url)
    bs = BeautifulSoup(response.content, "lxml")
    # bs = BeautifulSoup(response.content, "html.parser")  # <-- without lxml requirement

    parts = bs.find_all("article", class_="day-desc")
    level = len(parts)
    assert(1 <= level <= 2)

    if example_result_1 is None:
        print("< part 1")
        example_result_1 = find_example_result(parts[0])
        find_example(parts[0], EXAMPLE_FILE)
    if example_result_2 is None and level >= 2:
        print("< part 2")
        example_result_2 = find_example_result(parts[1])
        has_example_2 = find_example(parts[1], EXAMPLE2_FILE)

scrape()

class RunOnModification(FileSystemEventHandler):
    def __init__(self, path: str, expected_result: str | None, level: int = 1, example_file: str = EXAMPLE_FILE) -> None:
        self.path = path
        self.dir = os.path.dirname(path)
        self.expected_result = expected_result
        self.level = level
        self.last_run = time.time()
        self.output: str | None = None
        self.example_file = example_file


    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        if not os.path.isfile(self.path) or not os.path.samefile(self.path, event.src_path):
            return

        now = time.time()
        if now - self.last_run < 1:
            return
        self.last_run = now

        try:
            self.check()
        except KeyboardInterrupt:
            print("< abort run (ctrl+c)")


    def check(self):
        global auto_submit, done

        output = self.run(self.example_file)
        if output == self.expected_result:
            self.output = self.run(TASK_FILE)
            if auto_submit:
                print("> attempt auto-submit")
                response = submit(self.output, self.level)
                if self.level == 2 and response == SubmissionResult.WRONG_LEVEL:
                    done = True
                    return
                scrape()
                update_handlers()


    def run(self, input_file: str) -> str | None:
        try:
            print(f"> run '{self.path}' {input_file}")
            result = subprocess.run(["python", self.path, os.path.join(self.dir, input_file)], stdout=subprocess.PIPE)
            output = result.stdout.decode("utf-8").strip()
            print(output)
            return output
        except KeyboardInterrupt:
            print("< abort run (ctrl+c)")
            return None


observer = Observer()
event_handler_1 = RunOnModification(f"{day_dir}/{LEVEL1_FILE}", example_result_1, level=1)
watch_1 = observer.schedule(event_handler_1, day_dir, recursive=False)
event_handler_2 = RunOnModification(f"{day_dir}/{LEVEL2_FILE}", example_result_2, level=2)
watch_2 = observer.schedule(event_handler_2, day_dir, recursive=False)
observer.start()


def update_handlers():
    global example_result_1, example_result_2, has_example_2
    global event_handler_1, event_handler_2

    event_handler_1.expected_result = example_result_1
    event_handler_2.expected_result = example_result_2
    event_handler_2.example_file = EXAMPLE2_FILE if has_example_2 else EXAMPLE_FILE


lines = queue.Queue(32)


def read_lines():
    global lines, done
    while not sys.stdin.closed and not done:
        try:
            line = sys.stdin.readline().strip()
            lines.put(line)
        except KeyboardInterrupt:
            continue


reader_thread = threading.Thread(target=read_lines, daemon=True)
reader_thread.start()


while True:
    try:
        if sys.stdin.closed or done:
            break

        try:
            command = lines.get(block=True, timeout=0.01)
        except queue.Empty:
            continue

        handler = event_handler_1 if level == 1 else event_handler_2

        if command in ["q", "quit"]:
            break
        elif command in ["as", "auto-submit"]:
            auto_submit = not auto_submit
            print(f"< {auto_submit = }")
        elif command in ["f", "fetch"]:
            scrape()
            update_handlers()
        elif command in ["i", "info"]:
            print(f"< {level=} {example_result_1=} {example_result_2=} {has_example_2=}")
        elif command == "cp":
            if os.path.isfile(f"{day_dir}/{LEVEL2_FILE}"):
                shutil.copy2(f"{day_dir}/{LEVEL2_FILE}", f"{day_dir}/{os.urandom(16).hex()}.py")
            shutil.copy2(f"{day_dir}/{LEVEL1_FILE}", f"{day_dir}/{LEVEL2_FILE}")
        elif command in ["s", "submit"]:
            if handler.output is None:
                print("< failed to submit solution: solution not computed yet")
                continue

            print(f"> submit solution ({event_handler_1.output})")
            response = submit(handler.output, level)
            if level == 2 and response == SubmissionResult.CORRECT:
                done = True
                break
            scrape()
            update_handlers()
        elif command in ["c", "check"]:
            handler.check()
        elif command.startswith("ef") or command.startswith("example-file"):
            arguments = command.split(maxsplit=1)
            if len(arguments) == 2:
                handler.example_file = arguments[1]
            print(f"< example file == '{handler.example_file}'")
        elif command.startswith("e") or command.startswith("expect"):
            arguments = command.split(maxsplit=1)
            if len(arguments) == 2:
                handler.expected_result = arguments[1]
            print(f"< example result == '{handler.expected_result}'")
        elif command.startswith("r") or command.startswith("run"):
            arguments = command.split()[1:]
            if len(arguments) == 0:
                arguments = [handler.example_file]
            for argument in arguments:
                handler.run(argument)
        elif command == "":
            continue
        else:
            print("< unknown command")
    except KeyboardInterrupt:
        print("< use 'q' or 'quit' to exit")

observer.stop()
observer.join()
