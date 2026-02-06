from typing import List, Dict, Optional, Deque
from collections import deque
import time
from app.kernel.definitions import PageReplacementAlgo

class Page:
    def __init__(self, page_id: str, pid: int, content_ref: str = None):
        self.page_id = page_id
        self.pid = pid
        self.last_accessed = time.time()
        self.content_ref = content_ref # Pointer to actual data or swap ID

class MemoryManager:
    def __init__(self, total_memory_kb: int = 1024, page_size_kb: int = 4):
        self.total_memory_kb = total_memory_kb
        self.page_size_kb = page_size_kb
        self.num_frames = total_memory_kb // page_size_kb
        self.frames: List[Optional[Page]] = [None] * self.num_frames
        
        self.page_replacement_algo = PageReplacementAlgo.FIFO
        self.fifo_queue: Deque[int] = deque() # Stores frame indices
        
        # Statistics
        self.page_faults = 0
        self.page_hits = 0
    
    def allocate(self, pid: int, size_kb: int) -> List[str]:
        """Allocate memory for a process. Returns list of page IDs."""
        num_pages = (size_kb + self.page_size_kb - 1) // self.page_size_kb
        allocated_pages = []
        
        for i in range(num_pages):
            page_id = f"{pid}_{time.time()}_{i}"
            page = Page(page_id, pid)
            
            frame_idx = self._find_free_frame()
            if frame_idx == -1:
                frame_idx = self._evict_page()
                self.page_faults += 1
            
            self.frames[frame_idx] = page
            self.fifo_queue.append(frame_idx)
            allocated_pages.append(page_id)
            
        return allocated_pages

    def access_page(self, page_id: str):
        """Simulate memory access for LRU"""
        for page in self.frames:
            if page and page.page_id == page_id:
                page.last_accessed = time.time()
                self.page_hits += 1
                return
    
    def free(self, pid: int):
        """Free all memory for a process"""
        for i in range(len(self.frames)):
            if self.frames[i] and self.frames[i].pid == pid:
                self.frames[i] = None
                # Note: We don't remove from fifo_queue immediately for O(1) performance in sim, 
                # but real OS would handle free frames list.
                # Simplified: Just nullify frame. 

    def _find_free_frame(self) -> int:
        for i, frame in enumerate(self.frames):
            if frame is None:
                return i
        return -1

    def _evict_page(self) -> int:
        """Evict a page based on current algorithm"""
        if self.page_replacement_algo == PageReplacementAlgo.FIFO:
            # Simple FIFO
            if not self.fifo_queue:
                return 0 # Should not happen if frames full
            
            # Pop valid frame index
            victim_idx = self.fifo_queue.popleft()
            while self.frames[victim_idx] is None and self.fifo_queue:
                 victim_idx = self.fifo_queue.popleft()
            
            # Swap out logic would go here (write to Disk)
            # print(f"Evicting frame {victim_idx}")
            self.frames[victim_idx] = None
            return victim_idx
            
        elif self.page_replacement_algo == PageReplacementAlgo.LRU:
            # Find Least Recently Used
            lru_idx = -1
            oldest_time = float('inf')
            
            for i, page in enumerate(self.frames):
                if page and page.last_accessed < oldest_time:
                    oldest_time = page.last_accessed
                    lru_idx = i
            
            if lru_idx != -1:
                self.frames[lru_idx] = None
                return lru_idx
                
        return 0 # Fallback
