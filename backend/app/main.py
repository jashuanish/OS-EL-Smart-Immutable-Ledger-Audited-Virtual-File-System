"""
Main FastAPI application for CryptoFS++.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import routes

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Governed, Blockchain-Audited Virtual File System"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router, prefix=settings.API_V1_STR, tags=["api"])

@app.on_event("startup")
async def startup_event():
    from app.kernel.core import get_kernel
    from app.api.os_integration import register_syscalls
    
    kernel = get_kernel()
    kernel.start()
    register_syscalls()

@app.get("/")
async def root():
    """Root endpoint."""
    from app.kernel.core import get_kernel
    kernel = get_kernel()
    stats = kernel.get_stats()
    
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "os_simulation": {
            "status": "running",
            "scheduler": stats["scheduler"]["algo"],
            "memory_usage": f'{stats["memory"]["used_frames"]*4}KB'
        },
        "endpoints": {
            "files": f"{settings.API_V1_STR}/files",
            "blockchain": f"{settings.API_V1_STR}/blockchain",
            "zones": f"{settings.API_V1_STR}/zones"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

