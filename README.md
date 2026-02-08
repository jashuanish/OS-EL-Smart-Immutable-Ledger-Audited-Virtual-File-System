# 🛡️ CryptoFS++: AI-Governed, Blockchain-Audited Virtual File System

[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2014-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Language-Python%203.9+-3776AB?style=flat-square&logo=python)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178C6?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

## 📖 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Core Features](#core-features)
4. [Technology Stack](#technology-stack)
5. [Installation Guide](#installation-guide)
6. [Quick Start](#quick-start)
7. [Project Structure](#project-structure)
8. [Operating System Concepts](#operating-system-concepts)
9. [AI Classification System](#ai-classification-system)
10. [Security Model](#security-model)
11. [Blockchain Audit System](#blockchain-audit-system)
12. [File Zones and Policies](#file-zones-and-policies)
13. [API Documentation](#api-documentation)
14. [Frontend Components](#frontend-components)
15. [Experiential Learning Labs](#experiential-learning-labs)
16. [Testing and Validation](#testing-and-validation)
17. [Troubleshooting](#troubleshooting)
18. [Future Enhancements](#future-enhancements)
19. [Contributing](#contributing)
20. [License](#license)

---

## 🎯 Project Overview

CryptoFS++ is an advanced **AI-governed, blockchain-audited virtual file system** that demonstrates sophisticated operating system concepts through practical implementation. This project combines cutting-edge technologies including artificial intelligence, blockchain, cryptography, and OS kernel simulation to create a secure, intelligent file management system.

### Key Innovation Points

- **AI-Powered Classification**: Automatic detection of sensitive data using machine learning
- **Blockchain Auditing**: Immutable audit trail for all file operations
- **Zero-Trust Security**: Multi-layered security with behavioral analysis
- **OS Kernel Simulation**: Complete implementation of OS concepts including scheduling, memory management, and process control
- **Explainable AI**: Transparent decision-making with detailed explanations
- **Autonomous Encryption**: Policy-based automatic encryption of sensitive files

---

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER SPACE                                │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Next.js       │  │   React UI      │  │   TensorFlow    │ │
│  │   Frontend      │  │   Components    │  │   Face Detection│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   API Gateway     │
                    │   (FastAPI)       │
                    └─────────┬─────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    KERNEL SPACE                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Process       │  │   Memory        │  │   File System   │ │
│  │   Scheduler     │  │   Manager       │  │   & Locking     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Disk I/O      │  │   System Calls  │  │   AI Services   │ │
│  │   Scheduler     │  │   Interface     │  │   & Analysis    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                 HARDWARE SIMULATION                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Virtual RAM   │  │   Virtual Disk  │  │   Blockchain    │ │
│  │   (1MB)         │  │   Storage       │  │   Ledger        │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Three-Tier Architecture

1. **User Space Layer** (Next.js Frontend)
   - React-based user interface
   - TensorFlow.js for client-side AI processing
   - Real-time file monitoring and visualization
   - Interactive blockchain explorer

2. **Kernel Services Layer** (FastAPI Backend)
   - OS kernel simulation with scheduling algorithms
   - Memory management with paging
   - Process lifecycle management
   - File system with locking mechanisms
   - AI classification services
   - Blockchain audit logging

3. **Hardware Simulation Layer**
   - Virtual RAM (1MB capacity)
   - Virtual disk storage
   - Blockchain ledger for immutable auditing

---

## ✨ Core Features

### 🔍 AI-Powered Content Analysis
- **Text Analysis**: Advanced regex and ML-based detection of PII, credentials, and sensitive data
- **Image Analysis**: Face detection, ID card recognition, and content classification
- **Multi-format Support**: Text files, images, and documents
- **Explainable AI**: Detailed explanations for classification decisions

### 🔐 Security & Encryption
- **Autonomous Encryption**: AES-256 encryption for sensitive files
- **Zero-Trust Architecture**: Behavioral analysis and access control
- **Multi-factor Authentication**: Face recognition and credential verification
- **Policy Engine**: Configurable security policies and rules

### ⛓️ Blockchain Auditing
- **Immutable Ledger**: All operations logged to blockchain
- **Event Traceability**: Complete audit trail with timestamps
- **Chain Integrity**: Cryptographic verification of blockchain integrity
- **Transparent Governance**: Visible and verifiable system actions

### 🖥️ OS Kernel Simulation
- **CPU Scheduling**: FCFS, SJF, Round Robin, and Priority algorithms
- **Memory Management**: Paging with FIFO and LRU replacement
- **Process Management**: Complete process lifecycle simulation
- **File System**: Reader-writer locks and deadlock detection
- **Disk Scheduling**: SCAN/Elevator algorithm implementation

### 📊 Zone-Based File Management
- **Public Zone**: Low sensitivity, unrestricted access
- **Monitored Zone**: Medium sensitivity, access logging
- **Crypto Vault**: High sensitivity, encrypted storage
- **Cold Storage**: Critical sensitivity, maximum security

---

## 🛠️ Technology Stack

### Backend Technologies
- **FastAPI**: Modern, fast web framework for building APIs
- **Python 3.9+**: Core programming language
- **Cryptography**: AES-256 encryption and security operations
- **OpenCV**: Computer vision and image processing
- **NumPy**: Numerical computing and data analysis
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for FastAPI

### Frontend Technologies
- **Next.js 14**: React framework with server-side rendering
- **TypeScript**: Type-safe JavaScript development
- **TailwindCSS**: Utility-first CSS framework
- **Lucide React**: Modern icon library
- **TensorFlow.js**: Machine learning in the browser
- **React Dropzone**: File upload component
- **Axios**: HTTP client for API communication

### Development Tools
- **Git**: Version control system
- **Node.js**: JavaScript runtime environment
- **Python Virtual Environment**: Dependency isolation
- **ESLint**: Code linting and formatting

---

## 🚀 Installation Guide

### Prerequisites

Ensure you have the following installed:
- Python 3.9 or higher
- Node.js 18 or higher
- npm 8 or higher
- Git

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd "OS EL"
```

### Step 2: Backend Setup

```bash
cd FileExplorer/backend
python3 -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Step 3: Frontend Setup

```bash
cd ../frontend
npm install
```

### Step 4: Environment Configuration

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
ENCRYPTION_ALGORITHM=AES-256
KEY_DERIVATION_ITERATIONS=100000
```

---

## ⚡ Quick Start

### Launch the Application

**Terminal 1 - Backend:**
```bash
cd FileExplorer/backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd FileExplorer/frontend
npm run dev
```

### Access Points

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Test the System

1. **Upload Test Files**: Use files from `sample_files/` directory
2. **Observe Classification**: Watch AI classify files into security zones
3. **Check Encryption**: Verify sensitive files are automatically encrypted
4. **Explore Blockchain**: View immutable audit trail
5. **Monitor OS Metrics**: See kernel simulation in action

---

## 📁 Project Structure

```
OS EL/
├── FileExplorer/
│   ├── backend/                    # FastAPI Backend
│   │   ├── app/
│   │   │   ├── ai/               # AI Analysis Services
│   │   │   │   ├── text_analyzer.py      # Text content analysis
│   │   │   │   ├── image_analyzer.py     # Image processing
│   │   │   │   └── explainability.py     # AI explanation engine
│   │   │   ├── api/               # API Routes
│   │   │   ├── kernel/            # OS Kernel Simulation
│   │   │   │   ├── core.py               # Main kernel class
│   │   │   │   ├── scheduler.py          # CPU scheduling algorithms
│   │   │   │   ├── memory.py             # Memory management
│   │   │   │   ├── process.py            # Process control blocks
│   │   │   │   ├── filesystem.py         # File system & locking
│   │   │   │   └── disk.py               # Disk I/O scheduling
│   │   │   ├── services/         # Business Logic Services
│   │   │   │   ├── blockchain_logger.py  # Blockchain audit logging
│   │   │   │   ├── encryption_service.py  # File encryption
│   │   │   │   ├── access_control.py     # Security & access control
│   │   │   │   ├── policy_engine.py      # Security policy management
│   │   │   │   └── sensitivity_scoring.py # Content sensitivity scoring
│   │   │   ├── models/           # Data Models
│   │   │   ├── config.py         # Configuration management
│   │   │   └── main.py           # FastAPI application entry
│   │   ├── requirements.txt       # Python dependencies
│   │   ├── uploads/              # File upload directory
│   │   ├── encrypted/            # Encrypted file storage
│   │   └── blockchain_ledger.json # Blockchain ledger
│   ├── frontend/                  # Next.js Frontend
│   │   ├── src/
│   │   │   ├── app/              # Next.js app router
│   │   │   ├── components/       # React components
│   │   │   │   ├── FileExplorer.tsx      # Main file explorer
│   │   │   │   ├── OSDashboard.tsx       # OS metrics dashboard
│   │   │   │   ├── BlockchainViewer.tsx  # Blockchain explorer
│   │   │   │   ├── ZoneVisualization.tsx # Security zones view
│   │   │   │   ├── FileDetails.tsx       # File detail view
│   │   │   │   ├── FaceAuthModal.tsx     # Face authentication
│   │   │   │   └── LocalFileBrowser.tsx  # Local file browser
│   │   │   └── types/            # TypeScript type definitions
│   │   ├── package.json          # Node.js dependencies
│   │   └── tailwind.config.js    # TailwindCSS configuration
│   ├── sample_files/             # Test files for validation
│   │   ├── test_pii.txt          # PII test data
│   │   ├── test_credentials.txt   # Credential test data
│   │   ├── test_medical.txt      # Medical data test
│   │   └── test_normal.txt       # Normal file test
│   ├── README.md                 # This comprehensive documentation
│   ├── QUICKSTART.md            # Quick start guide
│   ├── INSTALL.md               # Installation instructions
│   ├── OS_CONCEPTS.md           # OS concepts mapping
│   ├── EXPERIMENTS.md           # Learning experiments
│   ├── setup.sh                 # Automated setup script
│   └── .gitignore               # Git ignore rules
```

---

## 🖥️ Operating System Concepts

### 1. System Calls Implementation

**Location**: `backend/app/kernel/syscalls.py`, `core.py`

**Theory**: Users cannot access kernel data directly. They must use a trap/interrupt mechanism to switch from user mode to kernel mode.

**Implementation**: 
- API routes (User Space) call `kernel.syscall(ID, ...)`
- This acts as the logical trap entering the `Kernel` class (Kernel Space)
- Privileged operations like file I/O and memory allocation execute in kernel mode

### 2. Process Lifecycle Management

**Location**: `backend/app/kernel/process.py`

**Theory**: Processes transition through states: NEW → READY → RUNNING → WAITING → TERMINATED

**Implementation**:
- **NEW**: Process created in `kernel.syscall()`
- **READY**: Added to `scheduler.ready_queue`
- **RUNNING**: Selected by `scheduler.get_next_process()`
- **TERMINATED**: Completes execution in `_tick_loop`

### 3. CPU Scheduling Algorithms

**Location**: `backend/app/kernel/scheduler.py`

**Theory**: The OS must decide which process gets CPU time to optimize system performance.

**Implemented Algorithms**:
- **FCFS (First Come First Served)**: `deque.popleft()`
- **SJF (Shortest Job First)**: Heuristic based on file size
- **Round Robin**: Time quantum simulation
- **Priority Scheduling**: Processes sorted by priority field

### 4. Memory Management

**Location**: `backend/app/kernel/memory.py`

**Theory**: RAM is divided into frames, processes use pages, and page tables map pages to frames.

**Implementation**:
- `MemoryManager` maintains frame allocation
- `allocate()` finds free frames or triggers `evict_page()`
- **Page Replacement**: FIFO and LRU algorithms for frame selection

### 5. File System Locking

**Location**: `backend/app/kernel/filesystem.py`

**Theory**: Concurrency control prevents race conditions. Deadlocks occur with circular wait conditions.

**Implementation**:
- **Reader-Writer Locks**: Shared vs Exclusive access patterns
- **Deadlock Detection**: Maintains `waits_for` graph with cycle detection using DFS

### 6. Disk Scheduling

**Location**: `backend/app/kernel/disk.py`

**Theory**: Seek time dominates HDD I/O costs. Algorithms minimize arm movement.

**Implementation**:
- `DiskDrive` simulates linear block device
- **SCAN/Elevator**: Sorts I/O requests for directional movement

---

## 🤖 AI Classification System

### Text Analysis Engine

**Location**: `backend/app/ai/text_analyzer.py`

**Detection Patterns**:
- **PII Detection**: Aadhaar, PAN, SSN, credit card numbers
- **Credential Detection**: API keys, passwords, tokens
- **Medical Information**: Diagnosis, prescriptions, patient data
- **High-Entropy Strings**: Encrypted data, random keys

**Classification Pipeline**:
1. **Pattern Matching**: Regex-based initial detection
2. **Context Analysis**: ML-based context understanding
3. **Confidence Scoring**: Weighted confidence calculation
4. **Risk Assessment**: Overall sensitivity scoring

### Image Analysis Engine

**Location**: `backend/app/ai/image_analyzer.py`

**Capabilities**:
- **Face Detection**: Using OpenCV and TensorFlow
- **ID Card Recognition**: Structural pattern detection
- **Text Extraction**: OCR for sensitive text in images
- **Content Classification**: Image categorization

**Processing Pipeline**:
1. **Preprocessing**: Image normalization and enhancement
2. **Feature Extraction**: Face and structure detection
3. **Classification**: Content-based categorization
4. **Risk Scoring**: Sensitivity level determination

### Explainability Engine

**Location**: `backend/app/ai/explainability.py`

**Features**:
- **Decision Explanation**: Why a file was classified as sensitive
- **Pattern Highlighting**: Specific patterns that triggered alerts
- **Confidence Breakdown**: Detailed confidence scoring
- **Recommendation Engine**: Security recommendations

---

## 🔒 Security Model

### Zero-Trust Architecture

**Location**: `backend/app/services/access_control.py`

**Principles**:
- **Never Trust, Always Verify**: Every access request is authenticated
- **Least Privilege**: Minimum necessary access permissions
- **Micro-Segmentation**: Fine-grained access control
- **Continuous Monitoring**: Behavioral analysis and anomaly detection

### Encryption Service

**Location**: `backend/app/services/encryption_service.py`

**Features**:
- **AES-256 Encryption**: Industry-standard symmetric encryption
- **Key Derivation**: PBKDF2 with 100,000 iterations
- **Secure Key Storage**: Environment-based key management
- **File Integrity**: Cryptographic hash verification

### Policy Engine

**Location**: `backend/app/services/policy_engine.py`

**Policy Types**:
- **Classification Policies**: Rules for content classification
- **Access Policies**: User and role-based access control
- **Encryption Policies**: Automatic encryption rules
- **Audit Policies**: Event logging and monitoring requirements

---

## ⛓️ Blockchain Audit System

### Blockchain Logger

**Location**: `backend/app/services/blockchain_logger.py`

**Features**:
- **Immutable Ledger**: Cryptographically chained blocks
- **Event Logging**: All system operations recorded
- **Chain Integrity**: Hash-based verification
- **Genesis Block**: Initial blockchain creation

**Block Structure**:
```json
{
  "index": 0,
  "timestamp": "2024-01-01T00:00:00Z",
  "events": [...],
  "previous_hash": "0" * 64,
  "hash": "calculated_block_hash"
}
```

**Event Types**:
- **FILE_UPLOAD**: File uploaded to system
- **CLASSIFICATION**: AI classification completed
- **ENCRYPTION**: File encrypted/decrypted
- **ACCESS_GRANTED**: Access permission granted
- **POLICY_VIOLATION**: Security policy violation

---

## 🗂️ File Zones and Policies

### Zone Classification

1. **Public Zone** 🟢
   - **Sensitivity**: 0-30
   - **Access**: Unrestricted
   - **Encryption**: None
   - **Monitoring**: Basic

2. **Monitored Zone** 🟡
   - **Sensitivity**: 31-60
   - **Access**: Logged access
   - **Encryption**: Optional
   - **Monitoring**: Enhanced

3. **Crypto Vault** 🔴
   - **Sensitivity**: 61-80
   - **Access**: Restricted
   - **Encryption**: Mandatory
   - **Monitoring**: Real-time

4. **Cold Storage** 🧊
   - **Sensitivity**: 81-100
   - **Access**: Highly restricted
   - **Encryption**: Maximum security
   - **Monitoring**: Continuous

### Policy Enforcement

**Automatic Actions**:
- **Classification**: AI-based zone assignment
- **Encryption**: Policy-based encryption
- **Access Control**: Role-based permissions
- **Audit Logging**: Comprehensive event tracking

---

## 📚 API Documentation

### Core Endpoints

#### File Management
- `POST /api/v1/files/upload` - Upload file for classification
- `GET /api/v1/files/` - List all files with metadata
- `GET /api/v1/files/{file_id}` - Get file details
- `DELETE /api/v1/files/{file_id}` - Delete file

#### Blockchain
- `GET /api/v1/blockchain/` - Get blockchain ledger
- `GET /api/v1/blockchain/blocks/{block_id}` - Get specific block
- `GET /api/v1/blockchain/verify` - Verify chain integrity

#### Zones
- `GET /api/v1/zones/` - Get zone statistics
- `GET /api/v1/zones/{zone_name}` - Get zone details

#### OS Metrics
- `GET /api/v1/os/stats` - Get OS simulation statistics
- `GET /api/v1/os/processes` - Get running processes
- `GET /api/v1/os/memory` - Get memory usage

### Response Format

```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

---

## 🎨 Frontend Components

### FileExplorer Component
**Location**: `frontend/src/components/FileExplorer.tsx`

**Features**:
- File upload with drag-and-drop
- Zone-based file organization
- Real-time classification display
- Interactive file details

### OSDashboard Component
**Location**: `frontend/src/components/OSDashboard.tsx`

**Features**:
- Real-time OS metrics
- CPU scheduling visualization
- Memory usage charts
- Process monitoring

### BlockchainViewer Component
**Location**: `frontend/src/components/BlockchainViewer.tsx`

**Features**:
- Interactive blockchain explorer
- Block detail view
- Event traceability
- Chain integrity verification

### ZoneVisualization Component
**Location**: `frontend/src/components/ZoneVisualization.tsx`

**Features**:
- Visual zone representation
- File distribution charts
- Zone statistics
- Interactive navigation

---

## 🧪 Experiential Learning Labs

### Lab 1: CPU Scheduling Analysis

**Goal**: Observe different scheduling algorithms with various job sizes.

**Procedure**:
1. Set scheduler to **FCFS**
2. Upload large file first, then small file
3. Observe wait time for short job
4. Switch to **SJF** and repeat
5. Compare scheduling efficiency

**Expected Learning**: Understanding scheduling algorithm impact on system performance.

### Lab 2: Memory Thrashing

**Goal**: Trigger and observe page replacement behavior.

**Procedure**:
1. Upload file larger than available RAM (1MB)
2. Monitor memory usage dashboard
3. Observe page fault counter increase
4. Watch frame eviction messages

**Expected Learning**: Understanding virtual memory and page replacement algorithms.

### Lab 3: Deadlock Detection

**Goal**: Create and observe deadlock resolution.

**Procedure**:
1. Simulate concurrent file access
2. Create circular wait condition
3. Observe deadlock detection
4. Watch system recovery process

**Expected Learning**: Understanding deadlock conditions and resolution strategies.

---

## 🧪 Testing and Validation

### Test Files

**Location**: `sample_files/`

1. **test_pii.txt**: Contains Aadhaar, PAN, credit card numbers
   - **Expected**: HIGH sensitivity, Crypto Vault, encrypted

2. **test_credentials.txt**: Contains API keys, passwords
   - **Expected**: HIGH sensitivity, Crypto Vault, encrypted

3. **test_medical.txt**: Contains medical information
   - **Expected**: MEDIUM-HIGH sensitivity, monitored zone

4. **test_normal.txt**: Regular document
   - **Expected**: LOW sensitivity, public zone

### Validation Checklist

- [ ] Backend starts successfully on port 8000
- [ ] Frontend starts successfully on port 3000
- [ ] File upload works correctly
- [ ] AI classification produces expected results
- [ ] Encryption is applied to sensitive files
- [ ] Blockchain ledger records all events
- [ ] OS metrics display correctly
- [ ] Zone assignment follows policies

---

## 🔧 Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check Python version
python3 --version

# Verify dependencies
pip list

# Check port availability
netstat -an | grep 8000
```

#### Frontend Won't Start
```bash
# Check Node version
node --version

# Clear cache and reinstall
rm -rf node_modules .next
npm install
```

#### API Connection Errors
- Verify backend is running on port 8000
- Check CORS configuration in `backend/app/config.py`
- Verify `NEXT_PUBLIC_API_URL` in frontend environment

#### File Upload Issues
- Check file size limit (100MB)
- Verify upload directory permissions
- Check backend logs for errors

#### Classification Issues
- Verify AI models are loaded correctly
- Check pattern definitions in text analyzer
- Review confidence thresholds in config

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export DEBUG=true
```

---

## 🚀 Future Enhancements

### Planned Features

1. **Advanced AI Models**
   - GPT integration for content analysis
   - Advanced image recognition
   - Behavioral pattern analysis

2. **Enhanced Security**
   - Multi-factor authentication
   - Hardware security module integration
   - Advanced threat detection

3. **Performance Optimization**
   - Distributed processing
   - Caching mechanisms
   - Load balancing

4. **User Experience**
   - Mobile application
   - Desktop client
   - Advanced reporting dashboard

5. **Integration**
   - Cloud storage integration
   - Enterprise directory services
   - Third-party security tools

### Research Opportunities

- **Machine Learning**: Improve classification accuracy
- **Cryptography**: Advanced encryption schemes
- **Distributed Systems**: Scalability improvements
- **Human-Computer Interaction**: UX optimization

---

## 🤝 Contributing

### Development Guidelines

1. **Code Style**: Follow PEP 8 for Python, ESLint for TypeScript
2. **Testing**: Write unit tests for new features
3. **Documentation**: Update documentation for API changes
4. **Commits**: Use conventional commit messages

### Pull Request Process

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request with description
5. Code review and merge

### Issue Reporting

Use GitHub issues to report:
- Bug reports with reproduction steps
- Feature requests with use cases
- Documentation improvements
- Performance issues

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

### Attribution

- Built with modern web technologies
- Inspired by operating system principles
- Enhanced with AI and blockchain innovations

---

## 📞 Support

For support and questions:

- **Documentation**: Check this README and markdown files
- **Issues**: Create GitHub issue for bugs
- **Features**: Request features via GitHub discussions
- **Community**: Join our developer community

---

## 🎓 Educational Value

This project demonstrates:

- **Operating Systems**: Complete OS kernel simulation
- **Artificial Intelligence**: Practical ML implementation
- **Blockchain**: Distributed ledger technology
- **Web Development**: Full-stack application
- **Security**: Modern security practices
- **Software Engineering**: Best practices and patterns

Perfect for:
- Computer Science students
- Security researchers
- Full-stack developers
- System administrators
- Technology enthusiasts

---

**CryptoFS++ - Where Security Meets Intelligence** 🛡️✨

---

# AI-ML Model & Security Architecture Documentation

## 1. Executive Summary

This document provides a comprehensive technical breakdown of the Artificial Intelligence (AI), Machine Learning (ML), and Cryptographic security mechanisms implemented in the **OS-EL Smart Immutable Ledger Audited Virtual File System** (CryptoFS++).

The system employs a multi-layered approach to data security and privacy:
1.  **Intelligent Content Analysis**: Automated scanning of files for Personally Identifiable Information (PII) and sensitive content using NLP and Computer Vision.
2.  **Military-Grade Encryption**: AES-256 encryption with unique per-file key derivation.
3.  **Biometric & Object Detection**: specialized models for face detection and document verification.

---

## 2. File Content Analysis Engine

The file analysis engine is orchestrated by the `ContentAnalysisService`, which delegates tasks to specialized analyzers based on the file MIME type.

### 2.1 Text Analysis Architecture

**Component**: `TextAnalyzer` (`backend/app/ai/text_analyzer.py`)

The text analysis module utilizes a hybrid approach combining **Regular Expression (Regex) Pattern Matching** and **Heuristic Entropy Analysis** to identify sensitive information with high precision.

#### 2.1.1 Pattern-Based Detection
The system scans for specific PII entities using optimized regex patterns. Each pattern is assigned a confidence score:

| Entity Type | Methodology | Confidence Score |
| :--- | :--- | :--- |
| **Aadhaar Card** | 12-digit pattern (`\d{4}\s?\d{4}\s?\d{4}`) | 0.85 |
| **PAN Card** | Alphanumeric (5 letters, 4 digits, 1 letter) | 0.90 |
| **SSN** | US Social Security Number format | 0.90 |
| **Credit Card** | 16-digit sequences with Luhn algorithm validation check | 0.80 |
| **API Keys** | Keyword-prefixed high-entropy strings | 0.85 |
| **Medical Data** | Semantic keyword matching (e.g., "diagnosis", "prescription") | 0.70 |

#### 2.1.2 High-Entropy Credential Detection
To detect undefined secrets (like random access tokens or passwords), the system employs **Shannon Entropy** analysis.
- **Algorithm**: `_is_high_entropy(text)`
- **Logic**: It calculates the ratio of unique characters to string length. If a string (length > 32) has a high variation of characters (> 50% unique), it is flagged as a potential cryptographic secret or token.

#### 2.1.3 Sensitivity Scoring
A cumulative `sensitivity_score` (0-100) is calculated based on weighted detections.
- **Critical Weights**: API Keys, Passwords (30 points)
- **High Weights**: Aadhaar, SSN (25 points)
- **Medium Weights**: Medical terms (20 points)
- **Classification**:
    - **CRITICAL**: Score ≥ 81
    - **HIGH**: Score ≥ 61
    - **MEDIUM**: Score ≥ 31
    - **LOW**: Score < 31

---

### 2.2 Image Analysis & Computer Vision

**Component**: `ImageAnalyzer` (`backend/app/ai/image_analyzer.py`)

The image analysis pipeline leverages **OpenCV** and **MediaPipe** to perform distinct computer vision tasks. The process involves decoding raw byte streams into NumPy arrays for processing.

#### 2.2.1 Face Detection (Biometric Screening)
The system determines the presence of human faces to flag potentially private photos or biometric data.

*   **Primary Engine**: **MediaPipe Face Detection**
    *   **Technology**: Google's BlazeFace model (lightweight, sub-millisecond inference).
    *   **Implementation**: `mp.solutions.face_detection`
    *   **Accuracy**: High resistance to rotation, scale, and lighting variations.
    *   **Output**: Bounding box coordinates and confidence scores for each face.

*   **Fallback Engine**: **OpenCV Haar Cascades**
    *   **Technology**: Traditional Viola-Jones object detection framework.
    *   **Model**: `haarcascade_frontalface_default.xml`
    *   **Usage**: Automatically triggered if MediaPipe fails or is unavailable.

#### 2.2.2 ID Card & Document Detection
Uses geometric shape analysis to detect ID cards (drivers licenses, national IDs).
1.  **Preprocessing**: Grayscale conversion + Canny Edge Detection (`cv2.Canny`).
2.  **Contour Analysis**: `cv2.findContours` identifies structural outlines.
3.  **Polygon Approximation**: `cv2.approxPolyDP` simplifies contours to checks for 4-sided shapes (rectangles) that occupy a significant portion (>10%) of the image area.

#### 2.2.3 Sensitive Screenshot Detection
Detects screenshots containing OTPs or QR codes.
- **QR Code Heuristic**: Analyzes contour hierarchy to find nested square patterns typical of QR position markers.
- **OTP/Text Heuristic**: Calculates "Edge Density". High-frequency edge patterns (>15% density) indicate text-heavy images like chat screenshots or OTP notifications.

---

## 3. Encryption & Security Architecture

The `EncryptionService` implements a **Zero-Knowledge-Proof-inspired** architecture where every file is encrypted with a unique, mathematically derived key.

### 3.1 Cryptographic Primitives
*   **Algorithm**: **AES-256-CBC** (Advanced Encryption Standard, 256-bit key, Cipher Block Chaining mode).
*   **Library**: `cryptography` (Python package backed by OpenSSL).
*   **Padding**: **PKCS7** (Public Key Cryptography Standards #7) to align data to 128-bit block boundaries.

### 3.2 Key Management Lifecycle

#### 3.2.1 Key Derivation (KDF)
Keys are **never stored directly**. They are derived on-the-fly using **PBKDF2-HMAC-SHA256**. This ensures that even if the database is compromised, the encryption keys cannot be recovered without the Master Secret.

**Derivation Formula**:
```python
Salt = SHA256(FileID + MasterSecret)[:16]
Key  = PBKDF2(
    Secret: MasterSecret,
    Salt: Salt,
    Algorithm: SHA256,
    Iterations: 100,000,
    Length: 32 bytes
)
```
*   **Uniqueness**: The `FileID` in the salt ensures every file has a completely different encryption key, even if the content is identical.
*   **Security**: 100,000 iterations make brute-force attacks computationally infeasible.

### 3.3 The Encryption Process
1.  **Input**: Raw file bytes.
2.  **Key Gen**: Unique key derived for the file.
3.  **IV Gen**: A cryptographically strong random 16-byte **Initialization Vector (IV)** is generated (`os.urandom(16)`).
4.  **Encryption**:
    *   Data is padded (PKCS7).
    *   Data is encrypted using AES-256-CBC with the Key and IV.
5.  **Packaging**: The IV is **prepended** to the encrypted ciphertext.
    *   `Final_Output = IV + Ciphertext`
6.  **Storage**: The blob is written to disk.

### 3.4 The Decryption Process
1.  **Extraction**: The system reads the first 16 bytes to retrieve the IV.
2.  **Key Gen**: The unique key is re-derived using the `FileID` and Master Secret.
3.  **Decryption**: AES-256-CBC decrypts the remaining bytes using the extracted IV and derived Key.
4.  **Unpadding**: PKCS7 padding is removed to restore the original file content.

---

## 4. Technical Stack Summary

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend Framework** | FastAPI | High-performance async API |
| **Computer Vision** | OpenCV (`cv2`) | Image processing, edge detection |
| **Face AI** | MediaPipe | ML-based face detection |
| **NLP/Text** | Regex + Custom Heuristics | PII and credential extraction |
| **Encryption** | `cryptography` (OpenSSL) | AES-256 primitives |
| **Key Derivation** | PBKDF2-HMAC-SHA256 | Secure key generation |


*Last updated: January 2024*
