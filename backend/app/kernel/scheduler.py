from abc import ABC, abstractmethod
from typing import List, Optional, Deque
from collections import deque
from app.kernel.process import PCB
from app.kernel.definitions import SchedulerAlgorithm

class Scheduler(ABC):
    def __init__(self):
        self.ready_queue: Deque[PCB] = deque()

    def add_process(self, process: PCB):
        """Add process to ready queue"""
        self.ready_queue.append(process)

    @abstractmethod
    def get_next_process(self) -> Optional[PCB]:
        """Select next process to run"""
        pass

    @property
    def queue_size(self) -> int:
        return len(self.ready_queue)

class FCFSScheduler(Scheduler):
    """First Come First Serve"""
    def get_next_process(self) -> Optional[PCB]:
        if not self.ready_queue:
            return None
        return self.ready_queue.popleft()

class SJFScheduler(Scheduler):
    """Shortest Job First - approximates by file size/expected duration"""
    # Note: true SJF requires knowing burst time. We'll use a heuristic.
    
    def add_process(self, process: PCB):
        self.ready_queue.append(process)
        # Sort queue by estimated burst time (stored in process metadata or heuristic)
        # For simplicity, we assume priority field might hold 'size' or we add a burst_time field
        # We will assume process.priority is holding the size for now or add a custom field later
        # Let's sort by a custom attribute 'job_size' if exists, else 0
        self.ready_queue = deque(sorted(self.ready_queue, key=lambda p: getattr(p, 'job_size', 0)))

    def get_next_process(self) -> Optional[PCB]:
        if not self.ready_queue:
            return None
        return self.ready_queue.popleft()

class PriorityScheduler(Scheduler):
    """Priority Scheduling (Non-preemptive for now)"""
    def add_process(self, process: PCB):
        self.ready_queue.append(process)
        # Sort by priority (Higher number = Higher priority, or vice versa? usually Lower # = Higher Priority in UNIX, but user said 'Priority')
        # Let's assume Higher Value = Higher Priority for clarity
        self.ready_queue = deque(sorted(self.ready_queue, key=lambda p: p.priority, reverse=True))

    def get_next_process(self) -> Optional[PCB]:
        if not self.ready_queue:
            return None
        return self.ready_queue.popleft()

class RoundRobinScheduler(Scheduler):
    """Round Robin"""
    def __init__(self, time_quantum: int = 2):
        super().__init__()
        self.time_quantum = time_quantum

    def get_next_process(self) -> Optional[PCB]:
        if not self.ready_queue:
            return None
        return self.ready_queue.popleft()

class SchedulerFactory:
    @staticmethod
    def get_scheduler(algo: SchedulerAlgorithm) -> Scheduler:
        if algo == SchedulerAlgorithm.FCFS:
            return FCFSScheduler()
        elif algo == SchedulerAlgorithm.SJF:
            return SJFScheduler()
        elif algo == SchedulerAlgorithm.PRIORITY:
            return PriorityScheduler()
        elif algo == SchedulerAlgorithm.ROUND_ROBIN:
            return RoundRobinScheduler()
        return FCFSScheduler()
