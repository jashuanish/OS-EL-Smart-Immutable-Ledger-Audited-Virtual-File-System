import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import shutil

class LocalFilesystemService:
    """
    Service for interacting with the actual Windows filesystem.
    Provides safe file operations with proper error handling.
    """
    
    def __init__(self, allowed_roots: Optional[List[str]] = None):
        """
        Initialize with allowed root directories for security.
        
        Args:
            allowed_roots: List of allowed root paths. If None, defaults to user directories.
        """
        if allowed_roots is None:
            user_home = str(Path.home())
            onedrive = os.path.join(user_home, "OneDrive")
            
            # Start with basic user folders
            roots = [
                os.path.join(user_home, "Desktop"),
                os.path.join(user_home, "Documents"),
                os.path.join(user_home, "Downloads"),
                os.path.join(user_home, "Pictures"),
            ]
            
            # Add OneDrive versions if they exist
            if os.path.exists(onedrive):
                roots.extend([
                    os.path.join(onedrive, "Desktop"),
                    os.path.join(onedrive, "Documents"),
                    os.path.join(onedrive, "Pictures"),
                ])
            
            # Add current project folder as a safe root
            project_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
            roots.append(project_root)
            
            # Clean up and remove duplicates/non-existent
            self.allowed_roots = []
            seen = set()
            for r in roots:
                abs_r = os.path.abspath(r).lower()
                if os.path.exists(r) and abs_r not in seen:
                    self.allowed_roots.append(r)
                    seen.add(abs_r)
        else:
            self.allowed_roots = allowed_roots
    
    def _is_path_allowed(self, path: str) -> bool:
        """Check if path is within allowed roots (case-insensitive and resolved for Windows)."""
        try:
            # Resolve junctions/symlinks
            res_path = os.path.realpath(os.path.abspath(path)).lower()
            norm_path = os.path.normpath(res_path)
            
            for root in self.allowed_roots:
                # Resolve root as well
                res_root = os.path.realpath(os.path.abspath(root)).lower()
                norm_root = os.path.normpath(res_root)
                
                if norm_path.startswith(norm_root):
                    return True
            return False
        except Exception:
            return False
    
    def scan_directory(self, path: str) -> Dict:
        """
        Scan a directory and return its contents.
        """
        # Always normalize input path
        path = os.path.normpath(os.path.abspath(path))
        
        print(f"--- FOLDER SCAN START: {path} ---")
        if not self._is_path_allowed(path):
            print(f"Permission denied for path: {path}")
            # Try to resolve it once more for logging
            res = os.path.realpath(path).lower()
            print(f"Resolved path was: {res}")
            print(f"Allowed roots were: {[os.path.realpath(r).lower() for r in self.allowed_roots]}")
            raise PermissionError(f"Access denied: {path} is outside allowed directories")
        
        if not os.path.exists(path):
            print(f"Path does not exist: {path}")
            raise FileNotFoundError(f"Path not found: {path}")
        
        if not os.path.isdir(path):
            print(f"Not a directory: {path}")
            raise ValueError(f"Path is not a directory: {path}")
        
        files = []
        folders = []
        
        try:
            print(f"Reading directory contents...")
            with os.scandir(path) as it:
                for entry in it:
                    try:
                        name = entry.name
                        # Skip hidden files
                        if name.startswith('.') or name.startswith('$'):
                            continue
                            
                        stat = entry.stat()
                        
                        # Timestamp conversion can fail on some Windows files (e.g. system files or placeholders)
                        try:
                            modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
                            created = datetime.fromtimestamp(stat.st_ctime).isoformat()
                        except (ValueError, OSError, OverflowError):
                            modified = datetime.now().isoformat()
                            created = datetime.now().isoformat()

                        item = {
                            "name": name,
                            "path": entry.path,
                            "size": stat.st_size if entry.is_file() else 0,
                            "modified": modified,
                            "created": created,
                            "is_encrypted": name.endswith('.encrypted'),
                        }
                        
                        if entry.is_file():
                            item["extension"] = os.path.splitext(name)[1]
                            files.append(item)
                        elif entry.is_dir():
                            folders.append(item)
                            
                    except (PermissionError, OSError) as e:
                        print(f"Skipping entry {entry.name} due to error: {e}")
                        continue
            
            print(f"Scan complete. Found {len(folders)} folders and {len(files)} files.")
        except Exception as e:
            print(f"CRITICAL ERROR scanning directory {path}: {e}")
            import traceback
            traceback.print_exc()
            raise e
        
        return {
            "path": path,
            "files": files,
            "folders": folders,
            "parent": str(Path(path).parent) if Path(path).parent != Path(path) else None
        }
    
    def get_file_metadata(self, path: str) -> Dict:
        """Get detailed metadata for a single file."""
        if not self._is_path_allowed(path):
            raise PermissionError(f"Access denied: {path}")
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        stat = os.stat(path)
        
        return {
            "name": os.path.basename(path),
            "path": path,
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "is_file": os.path.isfile(path),
            "is_dir": os.path.isdir(path),
            "extension": os.path.splitext(path)[1] if os.path.isfile(path) else None,
            "is_encrypted": path.endswith('.encrypted'),
        }
    
    def create_folder(self, path: str) -> Dict:
        """Create a new folder."""
        if not self._is_path_allowed(path):
            raise PermissionError(f"Access denied: {path}")
        
        if os.path.exists(path):
            raise FileExistsError(f"Path already exists: {path}")
        
        os.makedirs(path, exist_ok=False)
        
        return {
            "success": True,
            "path": path,
            "message": f"Folder created: {os.path.basename(path)}"
        }
    
    def delete_path(self, path: str) -> Dict:
        """Delete a file or folder."""
        if not self._is_path_allowed(path):
            raise PermissionError(f"Access denied: {path}")
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")
        
        if os.path.isfile(path):
            os.remove(path)
            item_type = "file"
        else:
            shutil.rmtree(path)
            item_type = "folder"
        
        return {
            "success": True,
            "path": path,
            "message": f"Deleted {item_type}: {os.path.basename(path)}"
        }
    
    def move_path(self, src: str, dest: str) -> Dict:
        """Move or rename a file/folder."""
        if not self._is_path_allowed(src) or not self._is_path_allowed(dest):
            raise PermissionError("Access denied")
        
        if not os.path.exists(src):
            raise FileNotFoundError(f"Source not found: {src}")
        
        if os.path.exists(dest):
            raise FileExistsError(f"Destination already exists: {dest}")
        
        shutil.move(src, dest)
        
        return {
            "success": True,
            "old_path": src,
            "new_path": dest,
            "message": f"Moved: {os.path.basename(src)} → {os.path.basename(dest)}"
        }
    
    def read_file_content(self, path: str, max_size: int = 1024 * 1024) -> bytes:
        """
        Read file content (for encryption/decryption operations).
        
        Args:
            path: File path
            max_size: Maximum file size to read (default 1MB)
        """
        if not self._is_path_allowed(path):
            raise PermissionError(f"Access denied: {path}")
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        if not os.path.isfile(path):
            raise ValueError(f"Path is not a file: {path}")
        
        file_size = os.path.getsize(path)
        if file_size > max_size:
            raise ValueError(f"File too large: {file_size} bytes (max {max_size})")
        
        with open(path, 'rb') as f:
            return f.read()
    
    def write_file_content(self, path: str, content: bytes) -> Dict:
        """Write content to a file."""
        if not self._is_path_allowed(path):
            raise PermissionError(f"Access denied: {path}")
        
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'wb') as f:
            f.write(content)
        
        return {
            "success": True,
            "path": path,
            "size": len(content),
            "message": f"File written: {os.path.basename(path)}"
        }
    
    def get_allowed_roots(self) -> List[Dict]:
        """Get list of allowed root directories with metadata."""
        roots = []
        for root in self.allowed_roots:
            if os.path.exists(root):
                roots.append({
                    "path": root,
                    "name": os.path.basename(root),
                    "exists": True
                })
            else:
                roots.append({
                    "path": root,
                    "name": os.path.basename(root),
                    "exists": False
                })
        return roots
