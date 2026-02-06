"""
API routes for CryptoFS++ backend.
Defines REST endpoints for file operations, AI analysis, and blockchain audit.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from typing import Optional, List
from uuid import UUID

from app.models.file import FileMetadata, FileContentAnalysis, EncryptionStatus
from app.models.user import UserRole
from app.services.file_ingestion import FileIngestionService
from app.services.content_analysis import ContentAnalysisService
from app.services.sensitivity_scoring import SensitivityScoringEngine
from app.services.encryption_service import EncryptionService
from app.services.policy_engine import PolicyEngine
from app.services.blockchain_logger import BlockchainLogger
from app.services.access_control import AccessControlService
from app.ai.explainability import ExplainabilityEngine

router = APIRouter()

# Initialize services
file_ingestion = FileIngestionService()
content_analysis = ContentAnalysisService()
sensitivity_scoring = SensitivityScoringEngine()
encryption_service = EncryptionService()
policy_engine = PolicyEngine()
blockchain_logger = BlockchainLogger()
access_control = AccessControlService()
explainability = ExplainabilityEngine()

# In-memory storage for demo (replace with database in production)
file_registry: dict[str, FileMetadata] = {}

def get_current_user(user_id: Optional[str] = Header(None, alias="X-User-ID")) -> str:
    """Get current user ID from header (simplified auth)."""
    if not user_id:
        user_id = "demo_user"  # Default for demo
    return user_id

def get_user_role(user_id: str) -> UserRole:
    """Get user role (simplified, replace with proper auth)."""
    # Demo: admin for demo_user, user for others
    return UserRole.ADMIN if user_id == "demo_user" else UserRole.USER

@router.post("/files/upload", response_model=dict)
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):
    """
    Upload and process a file.
    Automatically analyzes content, assigns zone, and encrypts if needed.
    """
    try:
        # Read file content
        file_content = await file.read()
        
        # Execute via System Call
        from app.kernel.core import get_kernel
        from app.kernel.definitions import SyscallID
        kernel = get_kernel()
        
        result = await kernel.syscall(
            SyscallID.SYS_UPLOAD,
            user_id,
            file_content=file_content, 
            filename=file.filename,
            mime_type=file.content_type or "application/octet-stream"
        )
        return result

    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files", response_model=List[dict])
async def list_files(user_id: str = Depends(get_current_user)):
    """List all files with metadata."""
    from app.kernel.core import get_kernel
    from app.kernel.definitions import SyscallID
    kernel = get_kernel()
    return await kernel.syscall(SyscallID.SYS_LIST, user_id)


@router.get("/files/{file_id}", response_model=dict)
async def get_file(
    file_id: str,
    user_id: str = Depends(get_current_user)
):
    """Get file metadata and explanation."""
    # Logic moved to OS Kernel
    from app.kernel.core import get_kernel
    from app.kernel.definitions import SyscallID
    kernel = get_kernel()
    
    try:
        # Execute via System Call (Creates Process)
        result = await kernel.syscall(
            SyscallID.SYS_OPEN,
            user_id,
            file_id=file_id
        )
        return result
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    


@router.get("/files/{file_id}/download")
async def download_file(
    file_id: str,
    user_id: str = Depends(get_current_user)
):
    """
    Download file.

    For encrypted files, this endpoint returns the raw encrypted bytes
    (ciphertext), so you can inspect or store the encrypted version
    rather than the decrypted plaintext.
    """
    from app.kernel.core import get_kernel
    from app.kernel.definitions import SyscallID
    from fastapi.responses import Response
    kernel = get_kernel()

    try:
        content, is_encrypted, metadata = await kernel.syscall(SyscallID.SYS_READ, user_id, file_id=file_id)
        
        if is_encrypted:
            download_name = f"{metadata.original_filename}.enc"
            media_type = "application/octet-stream"
        else:
            download_name = metadata.original_filename
            media_type = metadata.mime_type
            
        return Response(
            content=content,
            media_type=media_type,
            headers={
                "Content-Disposition": f'attachment; filename="{download_name}"'
            }
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Access denied")

@router.get("/files/{file_id}/decrypt")
async def decrypt_file(
    file_id: str,
    user_id: str = Depends(get_current_user)
):
    """
    Decrypt and download file.
    Only allows if user has permission.
    """
    from app.kernel.core import get_kernel
    from app.kernel.definitions import SyscallID
    from fastapi.responses import Response
    kernel = get_kernel()

    try:
        content, metadata = await kernel.syscall(SyscallID.SYS_DECRYPT, user_id, file_id=file_id)
        
        return Response(
            content=content,
            media_type=metadata.mime_type,
            headers={
                "Content-Disposition": f'attachment; filename="decrypted_{metadata.original_filename}"'
            }
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.get("/files/{file_id}/explain")
async def explain_file_decisions(
    file_id: str,
    user_id: str = Depends(get_current_user)
):
    """Get AI explanations for file decisions."""
    from app.kernel.core import get_kernel
    from app.kernel.definitions import SyscallID
    kernel = get_kernel()
    
    try:
        # Use SYS_OPEN to get metadata with explanations (as implemented in syscall_read)
        result = await kernel.syscall(SyscallID.SYS_OPEN, user_id, file_id=file_id)
        return result
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Access denied")

@router.get("/blockchain/chain")
async def get_blockchain_chain():
    """Get entire blockchain."""
    return {
        "blocks": [
            {
                "index": block.index,
                "timestamp": block.timestamp.isoformat(),
                "events": [e.dict() for e in block.events],
                "hash": block.hash,
                "previous_hash": block.previous_hash
            }
            for block in blockchain_logger.get_chain()
        ]
    }

@router.get("/blockchain/file/{file_id}")
async def get_file_audit_trail(file_id: str):
    """Get audit trail for a specific file."""
    events = blockchain_logger.get_file_audit_trail(file_id)
    return {
        "file_id": file_id,
        "events": [e.dict() for e in events]
    }

@router.get("/blockchain/stats")
async def get_blockchain_stats():
    """Get blockchain statistics."""
    return blockchain_logger.get_chain_stats()

@router.get("/zones")
async def get_zones():
    """Get file zones information."""
    return {
        "zones": [
            {
                "id": "public",
                "name": "🟢 Public Zone",
                "description": "Low sensitivity, unencrypted files",
                "threshold": "0-30"
            },
            {
                "id": "monitored",
                "name": "🟡 Monitored Zone",
                "description": "Medium sensitivity, monitored access",
                "threshold": "31-60"
            },
            {
                "id": "crypto_vault",
                "name": "🔴 Crypto Vault",
                "description": "High sensitivity, encrypted storage",
                "threshold": "61-80"
            },
            {
                "id": "cold_storage",
                "name": "🧊 Cold Storage",
                "description": "Critical files, maximum security",
                "threshold": "81-100"
            }
        ]
    }

# OS VIZ ENDPOINTS
@router.get("/os/processes")
async def get_os_processes():
    from app.kernel.core import get_kernel
    return get_kernel().get_process_table()

@router.get("/os/stats")
async def get_os_stats():
    from app.kernel.core import get_kernel
    return get_kernel().get_stats()

@router.post("/os/scheduler/{algo}")
async def set_scheduler(algo: str):
    from app.kernel.core import get_kernel
    from app.kernel.scheduler import SchedulerFactory
    from app.kernel.definitions import SchedulerAlgorithm
    
    try:
        algo_enum = SchedulerAlgorithm(algo.upper())
        kernel = get_kernel()
        # Hot-swap scheduler (preserving queue would be ideal, but for now reset or copy)
        # kernel.scheduler = SchedulerFactory.get_scheduler(algo_enum) 
        # Better: keep queue
        old_queue = kernel.scheduler.ready_queue
        kernel.scheduler = SchedulerFactory.get_scheduler(algo_enum)
        kernel.scheduler.ready_queue = old_queue
        return {"status": "updated", "algo": algo}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid algorithm")


# ============ Local Filesystem Endpoints ============

@router.get("/local/roots")
async def get_allowed_roots(user_id: str = Depends(get_current_user)):
    """Get list of allowed root directories."""
    from app.services.local_filesystem import LocalFilesystemService
    local_fs = LocalFilesystemService()
    return {"roots": local_fs.get_allowed_roots()}


@router.get("/local/browse")
async def browse_directory(
    path: str,
    user_id: str = Depends(get_current_user)
):
    """Browse a local directory."""
    from app.kernel.core import get_kernel
    from app.kernel.definitions import SyscallID
    
    kernel = get_kernel()
    try:
        result = await kernel.syscall(SyscallID.SYS_FS_SCAN, user_id, path=path)
        return result
    except PermissionError as e:
        print(f"FORBIDDEN: {e}")
        raise HTTPException(status_code=403, detail=str(e))
    except FileNotFoundError as e:
        print(f"NOT FOUND: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"SERVER ERROR: {e}")
        # Provide more detail in the 500 response
        raise HTTPException(status_code=500, detail=f"Filesystem Error: {str(e)}")


@router.post("/local/folder")
async def create_folder(
    path: str,
    user_id: str = Depends(get_current_user)
):
    """Create a new folder."""
    from app.kernel.core import get_kernel
    from app.kernel.definitions import SyscallID
    
    kernel = get_kernel()
    try:
        result = await kernel.syscall(SyscallID.SYS_FS_CREATE, user_id, path=path)
        return result
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except FileExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/local/file")
async def delete_file(
    path: str,
    user_id: str = Depends(get_current_user)
):
    """Delete a file or folder."""
    from app.kernel.core import get_kernel
    from app.kernel.definitions import SyscallID
    
    kernel = get_kernel()
    try:
        result = await kernel.syscall(SyscallID.SYS_FS_DELETE, user_id, path=path)
        return result
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/local/move")
async def move_file(
    src: str,
    dest: str,
    user_id: str = Depends(get_current_user)
):
    """Move or rename a file/folder."""
    from app.kernel.core import get_kernel
    from app.kernel.definitions import SyscallID
    
    kernel = get_kernel()
    try:
        result = await kernel.syscall(SyscallID.SYS_FS_MOVE, user_id, src=src, dest=dest)
        return result
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except FileExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/local/encrypt")
async def encrypt_local_file(
    path: str,
    user_id: str = Depends(get_current_user)
):
    """Encrypt a local file in-place."""
    from app.kernel.core import get_kernel
    from app.kernel.definitions import SyscallID
    
    kernel = get_kernel()
    try:
        result = await kernel.syscall(SyscallID.SYS_LOCAL_ENCRYPT, user_id, path=path)
        return result
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/local/decrypt")
async def decrypt_local_file(
    path: str,
    user_id: str = Depends(get_current_user)
):
    """Decrypt a local file in-place."""
    from app.kernel.core import get_kernel
    from app.kernel.definitions import SyscallID
    
    kernel = get_kernel()
    try:
        result = await kernel.syscall(SyscallID.SYS_LOCAL_DECRYPT, user_id, path=path)
        return result
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

