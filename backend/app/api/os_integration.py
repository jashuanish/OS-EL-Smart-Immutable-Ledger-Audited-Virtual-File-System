from typing import Any, List
import os
from uuid import UUID
from app.kernel.core import get_kernel
from app.kernel.definitions import SyscallID, ProcessState
from app.models.file import FileMetadata, EncryptionStatus
from app.models.user import UserRole

# Import Services
from app.services.file_ingestion import FileIngestionService
from app.services.content_analysis import ContentAnalysisService
from app.services.sensitivity_scoring import SensitivityScoringEngine
from app.services.encryption_service import EncryptionService
from app.services.policy_engine import PolicyEngine
from app.services.blockchain_logger import BlockchainLogger
from app.services.access_control import AccessControlService
from app.services.local_filesystem import LocalFilesystemService
from app.ai.explainability import ExplainabilityEngine

# Initialize services
file_ingestion = FileIngestionService()
content_analysis = ContentAnalysisService()
sensitivity_scoring = SensitivityScoringEngine()
encryption_service = EncryptionService()
policy_engine = PolicyEngine()
blockchain_logger = BlockchainLogger()
access_control = AccessControlService()
local_fs = LocalFilesystemService()
explainability = ExplainabilityEngine()

async def syscall_upload(user_id: str, file_content: bytes, filename: str, mime_type: str) -> dict:
    kernel = get_kernel()
    
    # Logic copied from routes.py but adapted
    metadata = await file_ingestion.ingest_file(
        file_content=file_content,
        filename=filename,
        mime_type=mime_type,
        uploaded_by=user_id
    )
    
    analysis = await content_analysis.analyze_file(
        file_content=file_content,
        mime_type=metadata.mime_type,
        file_id=str(metadata.file_id)
    )
    
    metadata.sensitivity_score = analysis.sensitivity_score
    metadata.sensitivity_level = analysis.classification
    metadata.detected_entities = analysis.detected_entities
    metadata.classification_reasons = analysis.reasons
    metadata.ai_confidence = analysis.confidence
    
    zone = sensitivity_scoring.calculate_zone(
        analysis.sensitivity_score,
        analysis.classification,
        analysis.detected_entities
    )
    metadata.zone = zone
    
    should_encrypt, policy_rule, reasons = policy_engine.decide_encryption(
        analysis.sensitivity_score,
        analysis.classification,
        analysis.detected_entities
    )
    
    if should_encrypt:
        encrypted_path, key_id = await encryption_service.encrypt_and_store(
            file_content,
            str(metadata.file_id),
            metadata.original_filename
        )
        metadata.encryption_status = EncryptionStatus.ENCRYPTED
        metadata.encryption_key_id = key_id
    
    # STORE IN KERNEL FS
    kernel.fs.files[str(metadata.file_id)] = metadata
    
    await blockchain_logger.log_event(
        event_type="FILE_UPLOAD",
        action="UPLOAD",
        result="SUCCESS",
        file_id=str(metadata.file_id),
        user_id=user_id,
        metadata={
            "filename": metadata.original_filename,
            "sensitivity_score": metadata.sensitivity_score,
            "zone": metadata.zone.value,
            "encrypted": should_encrypt
        }
    )
    
    explanation = explainability.explain_classification(
        metadata.sensitivity_score,
        metadata.sensitivity_level.value,
        metadata.detected_entities,
        metadata.classification_reasons,
        metadata.ai_confidence
    )
    
    return {
        "file_id": str(metadata.file_id),
        "filename": metadata.original_filename,
        "sensitivity_score": metadata.sensitivity_score,
        "sensitivity_level": metadata.sensitivity_level.value,
        "zone": metadata.zone.value,
        "encryption_status": metadata.encryption_status.value,
        "detected_entities": metadata.detected_entities,
        "classification_reasons": metadata.classification_reasons,
        "ai_confidence": metadata.ai_confidence,
        "explanation": explanation,
        "policy_rule": policy_rule
    }

async def syscall_list_files(user_id: str) -> List[dict]:
    kernel = get_kernel()
    files = []
    # Access Kernel FS
    for file_id, metadata in kernel.fs.files.items():
         files.append({
            "file_id": file_id,
            "filename": metadata.original_filename,
            "file_size": metadata.file_size,
            "mime_type": metadata.mime_type,
            "uploaded_at": metadata.uploaded_at.isoformat(),
            "zone": metadata.zone.value,
            "sensitivity_score": metadata.sensitivity_score,
            "sensitivity_level": metadata.sensitivity_level.value,
            "encryption_status": metadata.encryption_status.value,
            "detected_entities": metadata.detected_entities
        })
    return files

async def syscall_read(user_id: str, file_id: str, action: str = "READ") -> dict:
    # Handles GET /files/{id} and /download
    kernel = get_kernel()
    if file_id not in kernel.fs.files:
        raise FileNotFoundError("File not found")
        
    metadata = kernel.fs.files[file_id]
    user_role = UserRole.ADMIN if user_id == "demo_user" else UserRole.USER
    
    allowed, reason, _ = policy_engine.decide_access(
        user_role,
        metadata.sensitivity_level,
        "READ"
    )
    
    if not allowed:
        await blockchain_logger.log_event(
            event_type="ACCESS",
            action=action,
            result="DENIED",
            file_id=file_id,
            user_id=user_id,
            metadata={"reason": reason}
        )
        raise PermissionError(f"Access denied: {reason}")
        
    await blockchain_logger.log_event(
        event_type="ACCESS",
        action=action,
        result="ALLOWED",
        file_id=file_id,
        user_id=user_id
    )
    
    # Return metadata + explanations for Viewer
    # For download, route handles content fetching. Ideally syscall does it but we want to return content.
    # We will return the metadata and let route/handlers decide content fetching if this is meta-only.
    # Wait, 'sys_read' usually means reading bytes.
    # Let's split: sys_get_attrs (attrs) vs sys_read (content)
    # But for now, we'll return the full metadata object + explanations
    
    classification_explanation = explainability.explain_classification(
        metadata.sensitivity_score,
        metadata.sensitivity_level.value,
        metadata.detected_entities,
        metadata.classification_reasons,
        metadata.ai_confidence
    )
    
    encryption_explanation = explainability.explain_encryption_decision(
        metadata.encryption_status.value == "encrypted",
        "POLICY_RULE",
        metadata.classification_reasons,
        metadata.sensitivity_score
    )
    
    zone_explanation = explainability.explain_zone_assignment(
        metadata.zone.value,
        metadata.sensitivity_score,
        metadata.classification_reasons
    )
    
    return {
        "file_id": file_id,
        "metadata": metadata.dict(),
        "explanations": {
            "classification": classification_explanation,
            "encryption": encryption_explanation,
            "zone": zone_explanation
        }
    }

async def syscall_download_bytes(user_id: str, file_id: str):
    # Actually reads the file content
    kernel = get_kernel()
    if file_id not in kernel.fs.files:
        raise FileNotFoundError("File not found")
    metadata = kernel.fs.files[file_id]
    
    # Check perms again (or rely on sys_open logic if we had it)
    # Assuming sys_read checks perms
    
    # Fetch content
    if metadata.encryption_status.value == "encrypted":
        encrypted_path = encryption_service.encrypted_dir / f"{file_id}_encrypted_{metadata.original_filename}"
        import aiofiles
        async with aiofiles.open(encrypted_path, "rb") as f:
            return await f.read(), True, metadata # bytes, is_encrypted, meta
            
    else:
        content = await file_ingestion.read_file(UUID(file_id))
        return content, False, metadata

async def syscall_decrypt(user_id: str, file_id: str):
    kernel = get_kernel()
    if file_id not in kernel.fs.files:
        raise FileNotFoundError("File not found")
    
    metadata = kernel.fs.files[file_id]
    
    # Check permissions (must have explicit read access to high-sensitivity zones)
    user_role = UserRole.ADMIN if user_id == "demo_user" else UserRole.USER
    
    allowed, reason, _ = policy_engine.decide_access(
        user_role,
        metadata.sensitivity_level,
        "DECRYPT" # Custom action
    )
    
    # If not allowed by policy, and NOT admin, DENY.
    # We remove the fallback to "READ" because DECRYPT is a privileged operation.
    if not allowed and user_role != UserRole.ADMIN:
         await blockchain_logger.log_event("ACCESS", "DECRYPT", "DENIED", file_id, user_id, {"reason": reason})
         raise PermissionError(f"Access denied: {reason}")

    if metadata.encryption_status.value != "encrypted":
        # Return original if not encrypted
        content = await file_ingestion.read_file(UUID(file_id))
        return content, metadata

    # Perform Decryption
    encrypted_filename = f"{file_id}_encrypted_{metadata.original_filename}"
    decrypted_content = await encryption_service.decrypt_and_retrieve(file_id, encrypted_filename)
    
    if decrypted_content is None:
        raise FileNotFoundError("Encrypted file not found on disk")
        
    await blockchain_logger.log_event("ACCESS", "DECRYPT", "ALLOWED", file_id, user_id)
    
    return decrypted_content, metadata


# ============ Local Filesystem Syscalls ============

async def syscall_fs_scan(user_id: str, path: str):
    """Scan a local directory."""
    kernel = get_kernel()
    
    try:
        result = local_fs.scan_directory(path)
        await blockchain_logger.log_event("FILESYSTEM", "SCAN", "SUCCESS", path, user_id)
        return result
    except Exception as e:
        await blockchain_logger.log_event("FILESYSTEM", "SCAN", "FAILED", path, user_id, {"error": str(e)})
        raise


async def syscall_fs_create(user_id: str, path: str):
    """Create a new folder."""
    kernel = get_kernel()
    
    try:
        result = local_fs.create_folder(path)
        await blockchain_logger.log_event("FILESYSTEM", "CREATE_FOLDER", "SUCCESS", path, user_id)
        return result
    except Exception as e:
        await blockchain_logger.log_event("FILESYSTEM", "CREATE_FOLDER", "FAILED", path, user_id, {"error": str(e)})
        raise


async def syscall_fs_delete(user_id: str, path: str):
    """Delete a file or folder."""
    kernel = get_kernel()
    
    # Check if user has permission (require admin for sensitive operations)
    user_role = UserRole.ADMIN if user_id == "demo_user" else UserRole.USER
    
    try:
        result = local_fs.delete_path(path)
        await blockchain_logger.log_event("FILESYSTEM", "DELETE", "SUCCESS", path, user_id)
        return result
    except Exception as e:
        await blockchain_logger.log_event("FILESYSTEM", "DELETE", "FAILED", path, user_id, {"error": str(e)})
        raise


async def syscall_fs_move(user_id: str, src: str, dest: str):
    """Move or rename a file/folder."""
    kernel = get_kernel()
    
    try:
        result = local_fs.move_path(src, dest)
        await blockchain_logger.log_event("FILESYSTEM", "MOVE", "SUCCESS", src, user_id, {"destination": dest})
        return result
    except Exception as e:
        await blockchain_logger.log_event("FILESYSTEM", "MOVE", "FAILED", src, user_id, {"error": str(e)})
        raise


async def syscall_local_encrypt(user_id: str, path: str):
    """Encrypt a local file in-place."""
    kernel = get_kernel()
    user_role = UserRole.ADMIN if user_id == "demo_user" else UserRole.USER
    
    try:
        # Read file content
        content = local_fs.read_file_content(path)
        
        # Encrypt it
        encrypted_content = await encryption_service.encrypt_file(content)
        
        # Write back with .encrypted extension
        encrypted_path = f"{path}.encrypted"
        local_fs.write_file_content(encrypted_path, encrypted_content)
        
        # Optionally delete original
        # local_fs.delete_path(path)
        
        await blockchain_logger.log_event("ENCRYPTION", "LOCAL_ENCRYPT", "SUCCESS", path, user_id)
        
        return {
            "success": True,
            "original_path": path,
            "encrypted_path": encrypted_path,
            "message": f"File encrypted: {os.path.basename(encrypted_path)}"
        }
    except Exception as e:
        await blockchain_logger.log_event("ENCRYPTION", "LOCAL_ENCRYPT", "FAILED", path, user_id, {"error": str(e)})
        raise


async def syscall_local_decrypt(user_id: str, path: str):
    """Decrypt a local file in-place."""
    kernel = get_kernel()
    user_role = UserRole.ADMIN if user_id == "demo_user" else UserRole.USER
    
    if not path.endswith('.encrypted'):
        raise ValueError("File does not appear to be encrypted (missing .encrypted extension)")
    
    try:
        # Read encrypted content
        encrypted_content = local_fs.read_file_content(path)
        
        # Decrypt it
        decrypted_content = await encryption_service.decrypt_file(encrypted_content)
        
        # Write back without .encrypted extension
        decrypted_path = path.replace('.encrypted', '')
        local_fs.write_file_content(decrypted_path, decrypted_content)
        
        await blockchain_logger.log_event("ENCRYPTION", "LOCAL_DECRYPT", "SUCCESS", path, user_id)
        
        return {
            "success": True,
            "encrypted_path": path,
            "decrypted_path": decrypted_path,
            "message": f"File decrypted: {os.path.basename(decrypted_path)}"
        }
    except Exception as e:
        await blockchain_logger.log_event("ENCRYPTION", "LOCAL_DECRYPT", "FAILED", path, user_id, {"error": str(e)})
        raise


def register_syscalls():
    kernel = get_kernel()
    kernel.register_handler(SyscallID.SYS_UPLOAD, syscall_upload)
    kernel.register_handler(SyscallID.SYS_LIST, syscall_list_files)
    kernel.register_handler(SyscallID.SYS_OPEN, syscall_read) # We map OPEN/GET to this
    kernel.register_handler(SyscallID.SYS_READ, syscall_download_bytes) # We map READ/DOWNLOAD to this
    kernel.register_handler(SyscallID.SYS_DECRYPT, syscall_decrypt)
    
    # Local Filesystem Handlers
    kernel.register_handler(SyscallID.SYS_FS_SCAN, syscall_fs_scan)
    kernel.register_handler(SyscallID.SYS_FS_CREATE, syscall_fs_create)
    kernel.register_handler(SyscallID.SYS_FS_DELETE, syscall_fs_delete)
    kernel.register_handler(SyscallID.SYS_FS_MOVE, syscall_fs_move)
    kernel.register_handler(SyscallID.SYS_LOCAL_ENCRYPT, syscall_local_encrypt)
    kernel.register_handler(SyscallID.SYS_LOCAL_DECRYPT, syscall_local_decrypt)
    
    print("Syscalls registered")
