# Week 1 — AI Automation Starter Project

A beginner-friendly Python project covering Python automation, API requests, JSON parsing, prompt engineering, and file organization.

## Features

1. **Python automation menu** — run the project from one place.
2. **API practice** — makes three separate requests to the Official Joke API, parses the JSON response, and saves successful results to `jokes.json`.
3. **Prompt engineering** — creates a reusable, structured prompt and saves it to `generated_prompt.txt`.
4. **File organizer** — sorts files by extension into folders such as `Images`, `Documents`, `Spreadsheets`, `Code`, and `Other`. It avoids overwriting existing files.

## Requirements

- Python 3.10 or later recommended
- Internet connection only for the joke API feature
- No third-party Python packages required

## Run the project

1. Install Python from https://www.python.org/downloads/ if it is not installed.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

   ```bash
   python main.py
   ```

   On some Windows setups, use `py main.py`.

5. Select an option from the menu.

## Test the file organizer safely

The repository includes a `sample_files/` folder. In the program, choose option `3` and enter:

```text
sample_files
```

The files will be moved into `sample_files/organized_files/` by category. If you want to keep the sample folder unchanged, copy it before testing.

## API and JSON notes

- Endpoint: `https://official-joke-api.appspot.com/random_joke`
- The program makes three separate requests.
- It reads the response body and parses it with `json.loads`.
- Network errors, timeouts, and unexpected response data are handled without crashing the whole program.
- The API is a public learning endpoint; availability may vary.

## Prompt engineering example

Try option `2` and enter a task such as `Create a 30-minute study plan for Python basics`. The program creates a prompt with a role, task, audience, tone, instructions, and a defined output format.

## Safety note

Test file organization on a copy of important folders first. The organizer moves files; it does not delete them, but moving still changes their locations.

## Suggested GitHub repository description

`Beginner Python automation project with API calls, JSON parsing, prompt engineering, and an extension-based file organizer.`
