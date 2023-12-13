from abc import ABC

from fastapi import BackgroundTasks


class Repository(ABC):
    def __init__(self, background_tasks: BackgroundTasks):
        self.background_tasks = background_tasks
