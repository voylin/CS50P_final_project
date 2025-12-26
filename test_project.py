import pytest

from project import (
    Task,
    get_int,
    create_task,
    update_task_title,
    update_task_completion,
    delete_task,
)


def test_get_int() -> None:
    assert get_int("text") == -1
    assert get_int("3") == 3
    assert get_int("05") == 5


def test_create_task() -> None:
    tasks: dict[int, Task] = {}
    task_id: int = create_task(tasks, "Write test")

    assert task_id == 0
    assert tasks[0].title == "Write test"
    assert not tasks[0].completed


def test_update_task_title() -> None:
    tasks: dict[int, Task] = {}
    task_id: int = create_task(tasks, "Update test title")

    update_task_title(tasks, task_id, "Update test title working")
    assert tasks[0].title == "Update test title working"


def test_update_task_completion() -> None:
    tasks: dict[int, Task] = {}
    task_id: int = create_task(tasks, "Update test completion")

    update_task_completion(tasks, task_id)
    assert tasks[0].completed

    update_task_completion(tasks, task_id)
    assert not tasks[0].completed


def test_delete_task() -> None:
    tasks = {}
    task_id = create_task(tasks, "Delete test")

    delete_task(tasks, task_id)
    assert task_id not in tasks
    assert len(tasks.keys()) == 0
