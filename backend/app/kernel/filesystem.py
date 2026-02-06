from enum import Enum
from typing import Dict, List, Set, Optional
import time

class LockType(Enum):
    SHARED = "SHARED"       # Read
    EXCLUSIVE = "EXCLUSIVE" # Write

class FileLock:
    def __init__(self, file_id: str):
        self.file_id = file_id
        self.holders: Set[int] = set() # PIDs holding the lock
        self.type: Optional[LockType] = None
        self.waiting_queue: List[int] = [] # PIDs waiting

class FileSystem:
    def __init__(self):
        self.locks: Dict[str, FileLock] = {}
        # Resource allocation graph: PID -> Set of PIDs it is waiting for
        self.waits_for: Dict[int, Set[int]] = {}
        # Simulated Disk Storage (Metadata)
        self.files: Dict[str, Any] = {}

    def acquire_lock(self, file_id: str, pid: int, lock_type: LockType) -> bool:
        """
        Attempt to acquire a lock. 
        Returns True if acquired immediately.
        Returns False if blocked (must wait).
        Raises Exception if deadlock detected.
        """
        if file_id not in self.locks:
            self.locks[file_id] = FileLock(file_id)
        
        lock = self.locks[file_id]
        
        # If nobody holds execution, take it
        if not lock.holders:
            lock.holders.add(pid)
            lock.type = lock_type
            return True
            
        # Check compatibility
        if lock.type == LockType.SHARED and lock_type == LockType.SHARED:
            # Shared/Shared is compatible
            # BUT if there are exclusive waiters, we might want to wait to prevent starvation
            # For simplicity: Allow
            lock.holders.add(pid)
            return True
            
        if pid in lock.holders:
            # Re-entrant (simplified) or upgrading
            if lock.type == LockType.SHARED and lock_type == LockType.EXCLUSIVE:
                 if len(lock.holders) == 1:
                     lock.type = LockType.EXCLUSIVE
                     return True
                 else:
                     return False # Cannot upgrade if others hold read lock
            return True # Already holds it
            
        # Conflict
        # Add dependency to waits_for graph
        if pid not in self.waits_for:
            self.waits_for[pid] = set()
            
        for holder in lock.holders:
            self.waits_for[pid].add(holder)
            
        # Check Deadlock
        if self._detect_deadlock(pid):
            # Rollback/Fail
            self.waits_for[pid].clear() # Cleanup
            raise Exception(f"Deadlock detected for PID {pid} waiting on {file_id}")
            
        lock.waiting_queue.append(pid)
        return False

    def release_lock(self, file_id: str, pid: int):
        if file_id not in self.locks:
            return
            
        lock = self.locks[file_id]
        if pid in lock.holders:
            lock.holders.remove(pid)
            
            # Remove dependencies
            if pid in self.waits_for:
                del self.waits_for[pid]
            # Also remove PID from others' wait lists? No, only outgoing edges stored in waits_for[pid]
            # Actually we need to remove pid from others who were waiting on IT? 
            # No, correct way: if A waits for B, waits_for[A] has B.
            # If B releases, A is no longer waiting for B.
            # We must inspect all waiters
            pass # Simplification: The waiting process will retry acquiring and update its edges
            
            if not lock.holders:
                # Grant to next waiter
                if lock.waiting_queue:
                    # Logic here typically handled by Kernel waking up process
                    # We just reset type
                    lock.type = None # Reset
                else:
                    del self.locks[file_id]

    def _detect_deadlock(self, start_pid: int) -> bool:
        """DFS to find cycle"""
        visited = set()
        stack = set()
        
        def visit(node):
            if node in stack:
                return True
            if node in visited:
                return False
            
            visited.add(node)
            stack.add(node)
            
            neighbors = self.waits_for.get(node, set())
            for neighbor in neighbors:
                if visit(neighbor):
                    return True
            
            stack.remove(node)
            return False
            
        return visit(start_pid)
