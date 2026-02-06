from typing import List, Deque
from collections import deque
from enum import Enum

class DiskAlgo(Enum):
    FCFS = "FCFS"
    SSTF = "SSTF"
    SCAN = "SCAN"
    CSCAN = "CSCAN"

class DiskRequest:
    def __init__(self, block: int, pid: int, is_write: bool):
        self.block = block
        self.pid = pid
        self.is_write = is_write

class DiskDrive:
    def __init__(self, total_blocks: int = 1000):
        self.total_blocks = total_blocks
        self.head_position = 0
        self.direction = 1 # 1 for up, -1 for down
        self.request_queue: List[DiskRequest] = []
        self.algo = DiskAlgo.SCAN
        
        self.total_head_movement = 0
    
    def add_request(self, pid: int, block: int, is_write: bool = False):
        self.request_queue.append(DiskRequest(block, pid, is_write))
    
    def get_next_request(self) -> DiskRequest:
        if not self.request_queue:
            return None
            
        req = None
        
        if self.algo == DiskAlgo.FCFS:
            req = self.request_queue.pop(0)
            
        elif self.algo == DiskAlgo.SSTF:
            # Shortest Seek Time First
            msg_req = min(self.request_queue, key=lambda r: abs(r.block - self.head_position))
            self.request_queue.remove(msg_req)
            req = msg_req
            
        elif self.algo == DiskAlgo.SCAN:
            # Elevator
            # Sort requests
            sorted_reqs = sorted(self.request_queue, key=lambda r: r.block)
            
            # Find requests in current direction
            candidates = []
            if self.direction == 1:
                candidates = [r for r in sorted_reqs if r.block >= self.head_position]
            else:
                candidates = [r for r in sorted_reqs if r.block <= self.head_position]
                candidates.reverse() # Process descending
            
            if not candidates:
                # Reverse direction
                self.direction *= -1
                return self.get_next_request() # Recurse
            
            req = candidates[0]
            self.request_queue.remove(req)
            
        elif self.algo == DiskAlgo.CSCAN:
             # Circular SCAN - only goes up
            sorted_reqs = sorted(self.request_queue, key=lambda r: r.block)
            candidates = [r for r in sorted_reqs if r.block >= self.head_position]
            
            if not candidates:
                # Jump to 0 (wrap around)
                self.head_position = 0
                self.total_head_movement += abs(self.total_blocks - 0) # Simulated wrap cost? Or free?
                # Usually scan treats it as reset
                return self.get_next_request()
                
            req = candidates[0]
            self.request_queue.remove(req)

        if req:
            dist = abs(req.block - self.head_position)
            self.total_head_movement += dist
            self.head_position = req.block
            
        return req
