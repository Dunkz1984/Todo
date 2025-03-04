import json
from datetime import datetime
import shlex
import os

filepath = 'Todo.json'
opening = "Welcome to the To-Do List App! What would you like to do?"

def add(x):
    creation_date = datetime.now().date().isoformat()

    # Ensure file exists and contains valid JSON
    todo = []  # Default to an empty list if file is missing or invalid
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as file:
                todo = json.load(file)  # Attempt to load JSON
                if not isinstance(todo, list):  # Ensure it's a list
                    raise ValueError("Invalid JSON format: Expected a list.")
        except (json.JSONDecodeError, ValueError):  # Handle empty/corrupt files
            print("Warning: Todo.json was empty or invalid. Resetting it.")
            todo = []  # Reset to empty list

    # Generate new task ID safely
    uid = max([task['id'] for task in todo], default=0) + 1

    # Append new task
    todo.append({
        'id': uid,
        'description': x.strip(),  # Strip unnecessary whitespace
        'status': 'todo',
        'created_at': creation_date,
        'modified_at': None
    })

    # Save updated tasks to file
    with open(filepath, 'w') as file:
        json.dump(todo, file, indent=4)  # Pretty-print JSON

    print(f'Added task with ID {uid}')

def delete(x):
    try:
        with open(filepath, 'r') as file:
            todo = json.load(file)
        updated_todo = [task for task in todo if task['id'] != int(x)]
        if len(todo) == len(updated_todo):
            print(f'Task with ID {x} does not exist')
        else:
            with open(filepath, 'w') as file:
                json.dump(updated_todo, file)
            print(f'Task with ID {x} has been deleted')
    except FileNotFoundError:
        print("No tasks found.")

def update(x):
    modification_date = datetime.now().date().isoformat()
    try:
        with open(filepath, 'r') as file:
            todo = json.load(file)
        parts = shlex.split(x)
        task_id, description, status = parts[0], parts[1], parts[2]
        updated_todo = []
        found = False
        for task in todo:
            if task['id'] == int(task_id):
                updated_todo.append({'id': int(task_id), 'description': description, 'status': status, 'created_at': task['created_at'], 'modified_at': modification_date})
                found = True
            else:
                updated_todo.append(task)
        if not found:
            print(f'Task with ID {task_id} not found')
        else:
            with open(filepath, 'w') as file:
                json.dump(updated_todo, file)
            print(f'Task with ID {task_id} updated')
    except FileNotFoundError:
        print("No tasks found.")
    except (IndexError, ValueError):
        print("Invalid update format. Use: update <id> <description> <status>")

def markProgress(x):
    try:
        with open(filepath, 'r') as file:
            todo = json.load(file)
        updated_todo = []
        for task in todo:
            if task['id'] == int(x):
                task['status'] = 'in progress'
                task['modified_at'] = datetime.now().date().isoformat()
            updated_todo.append(task)
        with open(filepath, 'w') as file:
            json.dump(updated_todo, file)
        print(f'Task with ID {x} is now in progress')
    except FileNotFoundError:
        print("No tasks found.")

def markDone(x):
    try:
        with open(filepath, 'r') as file:
            todo = json.load(file)
        updated_todo = []
        for task in todo:
            if task['id'] == int(x):
                task['status'] = 'done'
                task['modified_at'] = datetime.now().date().isoformat()
            updated_todo.append(task)
        with open(filepath, 'w') as file:
            json.dump(updated_todo, file)
        print(f'Task with ID {x} is now done')
    except FileNotFoundError:
        print("No tasks found.")

def list():
    try:
        with open(filepath, 'r') as file:
            todo = json.load(file)
        for task in todo:
            mod_date = task.get('modified_at', 'N/A')
            print(f'{task["id"]} - {task["description"]} - {task["status"]} - Created: {task["created_at"]} - Modified: {mod_date}')
    except FileNotFoundError:
        print("No tasks found. Start by adding a task with 'add'!")

def main():
    print(opening)
    command = input()
    if command.startswith('add'):
        add(command.split(' ', 1)[1])
    elif command.startswith('delete'):
        delete(command.split(' ', 1)[1])
    elif command.startswith('update'):
        update(command.split(' ', 1)[1])
    elif command.startswith('mark-in-progress'):
        markProgress(command.split(' ', 1)[1])
    elif command.startswith('mark-done'):
        markDone(command.split(' ', 1)[1])
    elif command.startswith('list'):
        list()
    else:
        print('Invalid command. Please try again.')

if __name__ == '__main__':
    while True:
        main()