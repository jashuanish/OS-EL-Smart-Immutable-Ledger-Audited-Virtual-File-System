# OS Experiential Learning Labs

Run these experiments to verify the OS behavior.

## Lab 1: CPU Scheduling Analysis
**Goal**: Observe how different algorithms handle short vs long jobs.

1. **Setup**:
   - Open specific tabs: 1x small image (1MB), 1x large video (100MB).
   - Set Scheduler to **FCFS**.
2. **Action**:
   - Upload the VIDEO first, then immediately the IMAGE.
3. **Observation**:
   - The IMAGE waits until the VIDEO finishes processing.
   - **Metric**: High Wait Time for "Short Job".
4. **Experiment**:
   - Switch to **SJF** (Shortest Job First).
   - Repeat upload (VIDEO then IMAGE).
5. **Result**:
   - The IMAGE (if queued before VIDEO starts running) or subsequent small files will jump ahead of the large video.

## Lab 2: Memory Thrashing
**Goal**: Trigger page replacement.

1. **Setup**:
   - The Simulated RAM is capped at 1MB (approx 256 pages).
2. **Action**:
   - Upload a 5MB file.
   - Watch the **Memory Map** on the Dashboard.
3. **Observation**:
   - RAM fills to 100%.
   - **Page Fault** counter spikes rapidly.
   - The log shows "Evicting frame..." / "Swap out".

## Lab 3: Deadlock Detection
**Goal**: Create a circular wait.

1. **Setup**:
   - This requires a custom script or concurrent modification modification mock.
2. **Concept**:
   - Process A locks File X.
   - Process B locks File Y.
   - A tries to lock Y (Wait).
   - B tries to lock X (Wait -> **DEADLOCK**).
3. **Result**:
   - The Kernel detects the cycle in the Resource Allocation Graph.
   - One process is terminated with a `DeadlockException`.
