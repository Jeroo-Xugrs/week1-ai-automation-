"""
Week 1: AI Automation Starter Project
Features:
1. A small Python automation menu.
2. Makes three API requests to the Official Joke API and parses JSON.
3. Includes a reusable prompt template for an AI productivity assistant.
4. Organizes files into folders based on file extension.

Uses Python standard library only.
"""

from __future__ import annotations

import json
import shutil
import time
import urllib.error
import urllib.request
from pathlib import Path

JOKE_API = "https://official-joke-api.appspot.com/random_joke"
DEFAULT_ORGANIZE_FOLDER = "organized_files"

# Simple extension categories. Add extensions as needed.
FILE_CATEGORIES = {
    "Images": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt"},
    "Spreadsheets": {".csv", ".xls", ".xlsx", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg"},
    "Video": {".mp4", ".mov", ".avi", ".mkv", ".webm"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".json"},
}


def fetch_joke(timeout: int = 10) -> dict:
    """Fetch one joke and return parsed JSON as a dictionary."""
    request = urllib.request.Request(
        JOKE_API,
        headers={"User-Agent": "Week1-AI-Automation-Student-Project/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        if response.status != 200:
            raise RuntimeError(f"Joke API returned HTTP {response.status}")
        payload = json.loads(response.read().decode("utf-8"))

    if not isinstance(payload, dict) or not {"setup", "punchline"}.issubset(payload):
        raise ValueError("Unexpected API response format.")
    return payload


def get_three_jokes() -> list[dict]:
    """Make three separate API calls, handling common network/API errors."""
    jokes = []
    for index in range(3):
        try:
            joke = fetch_joke()
            jokes.append(joke)
            print(f"\nAPI call {index + 1}/3")
            print(f"Setup: {joke['setup']}")
            print(f"Punchline: {joke['punchline']}")
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError,
                RuntimeError, ValueError) as exc:
            print(f"API call {index + 1} failed: {exc}")
        if index < 2:
            time.sleep(0.4)  # brief pause between requests
    return jokes


def save_jokes(jokes: list[dict], output_file: Path | None = None) -> Path:
    """Save fetched joke data to a JSON file."""
    target = output_file or Path("jokes.json")
    target.write_text(json.dumps(jokes, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved {len(jokes)} joke(s) to: {target.resolve()}")
    return target


def build_prompt(task: str, audience: str = "a beginner", tone: str = "clear and friendly") -> str:
    """Create a structured prompt that can be pasted into an AI assistant."""
    return f"""Role: You are a careful productivity assistant.
Task: {task}
Audience: {audience}
Tone: {tone}

Instructions:
- Give an actionable, numbered solution.
- State assumptions instead of inventing missing facts.
- Include a short example where useful.
- Keep the explanation beginner-friendly.
- End with a brief checklist the user can follow.

Output format:
1. Goal
2. Steps
3. Example
4. Checklist
"""


def category_for(path: Path) -> str:
    """Return the matching folder name for a file."""
    suffix = path.suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Other"


def organize_files(source_dir: Path, destination_dir: Path | None = None) -> int:
    """
    Move files from source_dir into categorized subfolders.
    Does not recursively process subfolders and never overwrites a file.
    """
    source_dir = source_dir.expanduser().resolve()
    destination_dir = (destination_dir or source_dir / DEFAULT_ORGANIZE_FOLDER).expanduser().resolve()

    if not source_dir.exists() or not source_dir.is_dir():
        raise NotADirectoryError(f"Source folder does not exist: {source_dir}")
    if source_dir == destination_dir or source_dir in destination_dir.parents:
        # A destination inside the source folder is supported, but excluded from scanning.
        pass

    moved = 0
    for item in list(source_dir.iterdir()):
        if not item.is_file():
            continue
        if destination_dir == item or destination_dir in item.parents:
            continue

        category_dir = destination_dir / category_for(item)
        category_dir.mkdir(parents=True, exist_ok=True)
        target = category_dir / item.name

        # Avoid accidental overwrite by adding a numeric suffix.
        counter = 1
        while target.exists():
            target = category_dir / f"{item.stem}_{counter}{item.suffix}"
            counter += 1

        shutil.move(str(item), str(target))
        print(f"Moved: {item.name} -> {category_dir.name}/{target.name}")
        moved += 1

    print(f"\nFinished. Organized {moved} file(s) into: {destination_dir}")
    return moved


def main() -> None:
    while True:
        print("\n=== Week 1: AI Automation Starter ===")
        print("1. Fetch 3 jokes from an API and save JSON")
        print("2. Generate an AI prompt template")
        print("3. Organize files in a folder")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            jokes = get_three_jokes()
            if jokes:
                save_jokes(jokes)
            else:
                print("No jokes were received. Check your internet connection and retry.")
        elif choice == "2":
            task = input("What task should the AI help with? ").strip()
            if not task:
                print("Please enter a task.")
                continue
            audience = input("Audience [a beginner]: ").strip() or "a beginner"
            tone = input("Tone [clear and friendly]: ").strip() or "clear and friendly"
            prompt = build_prompt(task, audience, tone)
            print("\n--- Generated Prompt ---\n")
            print(prompt)
            Path("generated_prompt.txt").write_text(prompt, encoding="utf-8")
            print("\nSaved to generated_prompt.txt")
        elif choice == "3":
            raw = input("Folder path to organize (e.g. sample_files): ").strip()
            if not raw:
                print("Please enter a folder path.")
                continue
            try:
                organize_files(Path(raw))
            except (OSError, ValueError) as exc:
                print(f"Could not organize files: {exc}")
        elif choice == "4":
            print("Good luck with your assignment!")
            break
        else:
            print("Invalid option. Enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
