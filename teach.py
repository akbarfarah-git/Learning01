#!/usr/bin/env python3
"""Fun, funny, rich-text terminal app that teaches Python (minimal demo).

Run: python3 teach.py
      python3 teach.py --demo   # autoplay first lesson
"""
from __future__ import annotations
import sys
import subprocess
from time import sleep
from typing import List, Dict

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

console = Console()

LESSONS: List[Dict] = [
    {
        "title": "Hello, Python!",
        "content": "Use the `print()` function to say hello. Python loves greetings (and snacks).",
        "code": 'print("Hello, Python! 🐍")',
        "quiz": {
            "q": "Which function prints text to the console?",
            "choices": ["input", "print", "len", "open"],
            "a": "print",
        },
    },
    {
        "title": "Variables: Name Your Things",
        "content": "Variables hold values. They are like labeled jars for your data (peanut butter optional).",
        "code": 'name = "Ada"\nprint(f"Hello, {name}!")',
        "quiz": {
            "q": "What operator is used to assign a value to a variable?",
            "choices": ["=", ":", "==", "->"],
            "a": "=",
        },
    },
    {
        "title": "Loops: Do It Again (But Intentionally)",
        "content": "Loops let you repeat things. Great for songs, recipes, and boring tasks.",
        "code": 'for i in range(3):\n    print("I will not forget semicolons")',
        "quiz": {
            "q": "Which keyword starts a for-loop?",
            "choices": ["if", "for", "loop", "repeat"],
            "a": "for",
        },
    },
]


def panel(text: str, title: str | None = None):
    console.print(Panel(text, title=title, expand=False))


def show_welcome() -> None:
    panel("Welcome to Python Party — where code wears a party hat!\n\nPick a lesson and let's have some fun.", "Python Party 🎉")


def list_lessons() -> None:
    tbl = Table(title="Lessons")
    tbl.add_column("#", style="cyan", no_wrap=True)
    tbl.add_column("Title", style="magenta")
    for i, l in enumerate(LESSONS, start=1):
        tbl.add_row(str(i), l["title"])
    console.print(tbl)


def show_lesson(idx: int) -> None:
    lesson = LESSONS[idx]
    panel(lesson["content"], title=lesson["title"])
    console.print(Syntax(lesson["code"], "python", theme="monokai", line_numbers=True))


def run_code(code: str) -> None:
    console.print(Panel("Running the snippet... (safely-ish)", title="Executor"))
    try:
        completed = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=5)
        out = completed.stdout.strip()
        err = completed.stderr.strip()
        if out:
            console.print(Panel(out, title="Output", style="green"))
        if err:
            console.print(Panel(err, title="Errors", style="red"))
        if not out and not err:
            console.print(Panel("(no output)", style="yellow"))
    except subprocess.TimeoutExpired:
        console.print(Panel("Execution timed out — Python took a coffee break.", style="red"))


def ask_quiz(lesson) -> None:
    q = lesson["quiz"]
    console.print(f"[bold]{q['q']}[/bold]")
    for i, choice in enumerate(q["choices"], start=1):
        console.print(f"  {i}. {choice}")
    ans = console.input("Your answer (number): ")
    try:
        picked = int(ans) - 1
        choice = q["choices"][picked]
    except Exception:
        panel("That's not a valid choice. Try again later.", "Uh-oh")
        return
    if choice == q["a"]:
        panel("Correct! You're learning like a champ.", "Nice ✅")
    else:
        panel(f"Not quite — the answer is [bold]{q['a']}[/bold]. Keep trying!", "Almost")


def main_loop() -> None:
    show_welcome()
    while True:
        list_lessons()
        console.print("Commands: [b]view <n>[/b], [b]run <n>[/b], [b]quiz <n>[/b], [b]demo[/b], [b]quit[/b]")
        cmd = console.input("> ").strip()
        if not cmd:
            continue
        parts = cmd.split()
        cmd_name = parts[0].lower()
        if cmd_name in ("q", "quit", "exit"):
            panel("Bye-bye! May your exceptions be few.", "Goodbye 👋")
            break
        if cmd_name == "demo":
            panel("Autoplaying lesson 1 in 1 second...", "Demo")
            sleep(1)
            show_lesson(0)
            run_code(LESSONS[0]["code"])
            ask_quiz(LESSONS[0])
            continue
        if len(parts) < 2:
            panel("Specify a lesson number, e.g. `view 1`.", "Help")
            continue
        try:
            n = int(parts[1]) - 1
            if not (0 <= n < len(LESSONS)):
                raise ValueError
        except Exception:
            panel("Invalid lesson number.", "Error")
            continue
        if cmd_name == "view":
            show_lesson(n)
        elif cmd_name == "run":
            run_code(LESSONS[n]["code"])
        elif cmd_name == "quiz":
            ask_quiz(LESSONS[n])
        else:
            panel("Unknown command — try `view`, `run`, `quiz`, or `demo`.", "Hmm")


def demo_once() -> None:
    show_welcome()
    show_lesson(0)
    run_code(LESSONS[0]["code"])
    ask_quiz(LESSONS[0])


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo_once()
        sys.exit(0)
    try:
        main_loop()
    except KeyboardInterrupt:
        console.print("\nInterrupted. Bye!")
