import time
import asyncio
from typing import Any, Dict, List, Optional
from uuid import uuid4
from app.kernel.definitions import ProcessState

class PCB:
    """Process Control Block"""
    
    def __init__(self, pid: int, user_id: str, name: str, priority: int = 1):
        self.pid = pid
        self.user_id = user_id
        self.name = name
        self.priority = priority
        self.state = ProcessState.NEW
        self.created_at = time.time()
        self.started_at: Optional[float] = None
        self.completed_at: Optional[float] = None
        self.cpu_time_used = 0.0
        self.waiting_time = 0.0
        self.memory_pages: List[str] = []  # IDs of pages allocated
        self.files_open: List[str] = []    # IDs of files open
        self.logs: List[str] = []
        
        # Execution result
        self.result: Any = None
        self.error: Optional[Exception] = None
        
        # Async synchronization
        self.sync_event = asyncio.Event()
        
        # Task/Coroutine to execute (the actual work)
        self.task: Optional[Any] = None 
    
    def set_state(self, new_state: ProcessState):
        self.logs.append(f"State transition: {self.state.value} -> {new_state.value} at {time.time()}")
        self.state = new_state
        if new_state == ProcessState.RUNNING and self.started_at is None:
            self.started_at = time.time()
        if new_state == ProcessState.TERMINATED:
            self.completed_at = time.time()
            self.sync_event.set()
    
    def log(self, message: str):
        self.logs.append(f"[{time.time()}] {message}")

    def to_dict(self) -> Dict:
        return {
            "pid": self.pid,
            "user_id": self.user_id,
            "name": self.name,
            "state": self.state.value,
            "priority": self.priority,
            "cpu_time": self.cpu_time_used,
            "created_at": self.created_at,
            "memory_usage": len(self.memory_pages),
            "logs": self.logs[-5:] # Last 5 logs
        }
