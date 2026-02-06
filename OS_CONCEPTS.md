# OS Concepts Implementation Mapping

This document maps the OS theory to the actual code implementation in this project.

## 1. System Calls (`app/kernel/syscalls.py`, `core.py`)
- **Theory**: Users cannot access kernel data directly. They must use a trap/interrupt mechanism to switch mode.
- **Implementation**: The API routes (User Space) call `kernel.syscall(ID, ...)`. This is the logical trap that enters the `Kernel` class (Kernel Space) to execute privileged operations like file I/O or memory allocation.

## 2. Process Lifecycle (`app/kernel/process.py`)
- **Theory**: Processes go through states: NEW -> READY -> RUNNING -> WAITING -> TERMINATED.
- **Implementation**: The `PCB` class tracks this state.
  - **NEW**: Created in `kernel.syscall()`.
  - **READY**: Added to `scheduler.ready_queue`.
  - **RUNNING**: Picked by `scheduler.get_next_process()`.
  - **TERMINATED**: Finished execution in `_tick_loop`.

## 3. CPU Scheduling (`app/kernel/scheduler.py`)
- **Theory**: The OS must decide which process gets the CPU.
- **Implementation**:
  - **FCFS**: `deque.popleft()`.
  - **SJF**: Heuristic based on file size.
  - **Round Robin**: Time quantum logic (simulated).
  - **Priority**: Sorted by priority field.

## 4. Memory Management (`app/kernel/memory.py`)
- **Theory**: RAM is divided into Frames. Processes use Pages. Page Tables map Page->Frame.
- **Implementation**:
  - `MemoryManager` maintains `frames[]`.
  - `allocate()` finds free frames or triggers `evict_page()`.
  - **Page Replacement**: Implements standard FIFO and LRU algorithms to select victim frames when memory is full.

## 5. File System Locking (`app/kernel/filesystem.py`)
- **Theory**: Concurrency control prevents race conditions. Deadlocks occur when circular wait exists.
- **Implementation**:
  - **Reader-Writer Locks**: Shared vs Exclusive.
  - **Deadlock Detection**: Maintains a `waits_for` graph and performs Cycle Detection (DFS) before blocking a process.

## 6. Disk Scheduling (`app/kernel/disk.py`)
- **Theory**: Seek time is the dominant cost in HDD I/O. Algorithms minimize arm movement.
- **Implementation**:
  - `DiskDrive` simulates a linear block device.
  - **SCAN/Elevator**: Sorts I/O requests to move in one direction before reversing, mimicking physical disk physics.
