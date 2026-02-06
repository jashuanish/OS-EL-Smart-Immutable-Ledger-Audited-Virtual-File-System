from enum import Enum, auto

class ProcessState(Enum):
    NEW = "NEW"
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    TERMINATED = "TERMINATED"

class SchedulerAlgorithm(Enum):
    FCFS = "FCFS"
    SJF = "SJF"
    PRIORITY = "PRIORITY"
    ROUND_ROBIN = "ROUND_ROBIN"

class SyscallID(Enum):
    SYS_OPEN = "SYS_OPEN"
    SYS_READ = "SYS_READ"
    SYS_WRITE = "SYS_WRITE"
    SYS_CLOSE = "SYS_CLOSE"
    SYS_UPLOAD = "SYS_UPLOAD"       # High-level convenience
    SYS_DOWNLOAD = "SYS_DOWNLOAD"   # High-level convenience
    SYS_ENCRYPT = "SYS_ENCRYPT"
    SYS_DECRYPT = "SYS_DECRYPT"     # NEW: Decryption
    SYS_DELETE = "SYS_DELETE"
    SYS_LIST = "SYS_LIST"
    SYS_ACCESS = "SYS_ACCESS"       # Policy check
    
    # Local Filesystem Operations
    SYS_FS_SCAN = "SYS_FS_SCAN"         # Scan local directory
    SYS_FS_CREATE = "SYS_FS_CREATE"     # Create folder
    SYS_FS_DELETE = "SYS_FS_DELETE"     # Delete file/folder
    SYS_FS_MOVE = "SYS_FS_MOVE"         # Move/rename
    SYS_LOCAL_ENCRYPT = "SYS_LOCAL_ENCRYPT"  # Encrypt local file
    SYS_LOCAL_DECRYPT = "SYS_LOCAL_DECRYPT"  # Decrypt local file
    SYS_GET_PROCESSES = "SYS_GET_PROCESSES" # Visualization
    SYS_GET_STATS = "SYS_GET_STATS" # Visualization

class PageReplacementAlgo(Enum):
    FIFO = "FIFO"
    LRU = "LRU"
