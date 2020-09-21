from .models import InTask, OutTask
from typing import List

class DBSession:
    tasks: List[OutTask] = []
    def __init__(self):
        self.tasks = DBSession.tasks
def get_db():
    return DBSession()