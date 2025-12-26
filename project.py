from dataclasses import dataclass
from pathlib import Path
import json


SAVE_PATH: Path = Path("tasks.json")


@dataclass
class Task:
    completed: bool = False
    title: str = ""


def print_tasks(tasks: dict[int, Task]) -> None:
    print("\n--== Tasks ==--")

    if len(tasks.keys()) == 0:
        print(" No tasks yet")
    else:
        for task_id, task in tasks.items():
            completed: str = "[x]" if task.completed else "[ ]"
            print(f" {completed} - {task_id}: {task.title}")

    print("--==--=-=--==--")


def get_int(user_input: str) -> int:
    try:
        return int(input(user_input))
    except ValueError:
        return -1


def get_main_options() -> int:
    print(" 1) Create new task;")
    print(" 2) Update task;")
    print(" 3) Delete task;")
    print(" 0) Quit;")
    print("--==--=-=--==--")

    return get_int("> ")


def get_update_options() -> int:
    print(" 1) Toggle completion;")
    print(" 2) Change title;")
    print(" 0) Back;")
    print("--==--=-=--==--")

    return get_int("> ")


def create_task(tasks: dict[int, Task], task_title: str) -> int:
    if not task_title:
        return

    task_id = max(tasks.keys(), default=-1) + 1
    tasks[task_id] = Task(title=task_title)

    return task_id


def update_task(tasks: dict[int, Task], task_id: int) -> None:
    match get_update_options():
        case 1: update_task_completion(tasks, task_id)
        case 2: update_task_title(tasks, task_id, input("\nNew title: ").strip())


def update_task_completion(tasks: dict[int, Task], task_id: int) -> None:
    if task_id not in tasks:
        raise KeyError("Task not found")

    tasks[task_id].completed = not tasks[task_id].completed


def update_task_title(tasks: dict[int, Task], task_id: int, new_title: str) -> None:
    if task_id not in tasks:
        raise KeyError("Task not found")

    tasks[task_id].title = new_title


def delete_task(tasks: dict[int, Task], task_id: int) -> None:
    if task_id not in tasks:
        raise KeyError("Task not found")

    del tasks[task_id]


def save_tasks(tasks: dict[int, Task]) -> None:
    SAVE_PATH.write_text(json.dumps({
        task_id: {
            "completed": task.completed,
            "title": task.title
        } for task_id, task in tasks.items()}
    ))


def load_tasks() -> dict[int, Task]:
    if not SAVE_PATH.exists():
        return {}

    return {
        int(task_id): Task(
            completed=task["completed"],
            title=task["title"]
        ) for task_id, task in json.loads(SAVE_PATH.read_text()).items()}


def main():
    tasks: dict[int, Task] = load_tasks()

    while True:
        print_tasks(tasks)

        match get_main_options():
            case 1: create_task(tasks, input("\nTask title: ").strip())
            case 2: update_task(tasks, get_int("\nTask id: "))
            case 3: delete_task(tasks, get_int("\nTask id: "))
            case _:
                save_tasks(tasks)
                break


if __name__ == "__main__":
    main()
