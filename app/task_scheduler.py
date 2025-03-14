# app/task_scheduler.py

from collections import defaultdict
from heapq import heappush, heappop
from flask import session
from datetime import datetime

class Task:
    def __init__(self, name, scheduled_date, importance=1, duration=1):
        self.name = name
        self.scheduled_date = scheduled_date if scheduled_date else "Not Scheduled"
        self.importance = int(importance)
        self.duration = int(duration)
    
    def __lt__(self, other):
        return self.scheduled_date < other.scheduled_date or (
            self.scheduled_date == other.scheduled_date and self.importance > other.importance
        )

class Scheduler:
    def __init__(self):
        self.graph = defaultdict(list)
        self.tasks = {}

    def add_task(self, name, scheduled_date, importance=1, duration=1, dependency=None):
        task = Task(name, scheduled_date, importance, duration)
        self.tasks[name] = task
        if dependency:
            self.graph[dependency].append(name)

    def remove_task(self, name):
        if name in self.tasks:
            del self.tasks[name]
        for task in self.graph:
            if name in self.graph[task]:
                self.graph[task].remove(name)

    def get_schedule(self):
        in_degree = {task: 0 for task in self.tasks}
        for dependencies in self.graph.values():
            for dep in dependencies:
                in_degree[dep] += 1

        task_queue = []
        for task_name, task_obj in self.tasks.items():  # Ensure correct mapping
            if in_degree[task_name] == 0:
                heappush(task_queue, task_obj)

        schedule = []
        while task_queue:
            task = heappop(task_queue)
            schedule.append({
                'name': task.name,
                'scheduled_date': task.scheduled_date,
                'importance': task.importance,
                'duration': task.duration
            })

            for dependent_task in self.graph.get(task.name, []):  # Fix reference
                in_degree[dependent_task] -= 1
                if in_degree[dependent_task] == 0:
                    heappush(task_queue, self.tasks[dependent_task])

        return sorted(schedule, key=lambda x: (x['scheduled_date'], -x['importance']))

    def save_to_session(self):
        session["tasks"] = {
            name: {
                "name": task.name,
                "scheduled_date": task.scheduled_date,
                "importance": task.importance,
                "duration": task.duration
            }
            for name, task in self.tasks.items()
        }
        session["graph"] = dict(self.graph)

    def load_from_session(self):
        if "tasks" in session and "graph" in session:
            self.tasks = {
                name: Task(
                    task_data["name"],
                    task_data.get("scheduled_date", "Not Scheduled"),
                    task_data["importance"],
                    task_data["duration"]
                )
                for name, task_data in session["tasks"].items()
            }
            self.graph = defaultdict(list, session["graph"])
