import asyncio
import time
from typing import Dict, Any, Optional, Callable
from app.kernel.definitions import SyscallID, ProcessState, SchedulerAlgorithm, PageReplacementAlgo
from app.kernel.process import PCB
from app.kernel.scheduler import SchedulerFactory
from app.kernel.memory import MemoryManager
from app.kernel.disk import DiskDrive
from app.kernel.filesystem import FileSystem, LockType

# Singleton instance
_kernel_instance = None

class Kernel:
    def __init__(self):
        self.scheduler = SchedulerFactory.get_scheduler(SchedulerAlgorithm.FCFS)
        self.memory_manager = MemoryManager()
        self.disk = DiskDrive()
        self.fs = FileSystem()
        
        self.processes: Dict[int, PCB] = {}
        self.next_pid = 100
        self.running = False
        
        # Callbacks for actual logic (injected to avoid circular imports if possible, or direct import)
        self.syscall_handlers: Dict[SyscallID, Callable] = {}

    def start(self):
        """Start the Kernel simulation loop"""
        if not self.running:
            self.running = True
            asyncio.create_task(self._tick_loop())
            print("OS Kernel Started")

    async def _tick_loop(self):
        """Simulates CPU cycles"""
        while self.running:
            # 1. Disk I/O Simulation
            disk_req = self.disk.get_next_request()
            if disk_req:
                # Simulate I/O completion for that PID
                # In a real OS, we'd wake up the process waiting for I/O
                # Here, we usually assume processes doing I/O are WAITING
                pass 

            # 2. CPU Scheduling
            proc = self.scheduler.get_next_process()
            if proc:
                proc.set_state(ProcessState.RUNNING)
                try:
                    # Execute the task
                    # For simulation, we await the wrapped coroutine
                    # This implies non-preemptive execution for the duration of the coroutine
                    if proc.task:
                        proc.result = await proc.task()
                except Exception as e:
                    proc.error = e
                    proc.log(f"Error: {str(e)}")
                
                # Cleanup
                self.memory_manager.free(proc.pid)
                # Release locks
                for fid in list(proc.files_open):
                     self.fs.release_lock(fid, proc.pid)
                
                proc.set_state(ProcessState.TERMINATED)
                del self.processes[proc.pid]
            else:
                # Idle cyle
                await asyncio.sleep(0.1)
                
            await asyncio.sleep(0.01) # Tick interval

    async def syscall(self, call_id: SyscallID, user_id: str, *args, **kwargs) -> Any:
        """
        Main System Call Interface.
        Creates a process for the requested operation and waits for it.
        """
        # 1. Create Process
        pid = self.next_pid
        self.next_pid += 1
        
        # Name heuristic
        proc_name = f"{call_id.value}_{pid}"
        
        proc = PCB(pid, user_id, proc_name)
        self.processes[pid] = proc
        
        # 2. Assign Task based on syscall
        # We wrap the handler in a closure
        handler = self.syscall_handlers.get(call_id)
        if not handler:
            raise NotImplementedError(f"Syscall {call_id} not implemented")
            
        async def wrapped_task():
            # Simulate Overhead
            proc.log("Allocating Memory...")
            pages = self.memory_manager.allocate(pid, 64) # Arbitrary 64KB overhead
            
            proc.log("Requesting Disk I/O...")
            # Simulate disk write for "request"
            self.disk.add_request(pid, pid, True)
            await asyncio.sleep(3.0) # Simulate seek/boot (Increased for Visualization)
            
            proc.log("Executing System Service...")
            return await handler(user_id, *args, **kwargs)

        proc.task = wrapped_task
        
        # 3. Submit to Scheduler
        proc.set_state(ProcessState.READY)
        self.scheduler.add_process(proc)
        
        # 4. Wait for completion (Synchronous from caller perspective)
        await proc.sync_event.wait()
        
        if proc.error:
            raise proc.error
        return proc.result

    def register_handler(self, call_id: SyscallID, handler: Callable):
        self.syscall_handlers[call_id] = handler

    # Admin/Debug methods for visualization
    def get_process_table(self):
        return [p.to_dict() for p in self.processes.values()]
    
    def get_stats(self):
        return {
            "memory": {
                "total": self.memory_manager.total_memory_kb,
                "used_frames": sum(1 for f in self.memory_manager.frames if f is not None),
                "page_faults": self.memory_manager.page_faults
            },
            "disk": {
                "head_pos": self.disk.head_position,
                "total_movement": self.disk.total_head_movement
            },
            "scheduler": {
                "algo": type(self.scheduler).__name__,
                "queue_size": self.scheduler.queue_size
            }
        }

def get_kernel() -> Kernel:
    global _kernel_instance
    if _kernel_instance is None:
        _kernel_instance = Kernel()
    return _kernel_instance
