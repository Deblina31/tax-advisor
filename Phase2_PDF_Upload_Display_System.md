# Phase 2: PDF Upload & Display System (Local Development)

## Overview
Phase 2 focuses on implementing a robust PDF upload and display system for the Tax Advisor application. This phase handles user document uploads (Pay Slips, Salary Slips, or Form 16) and displays them alongside data input forms for manual entry.

## 🎯 Phase 2 Goals
- **Primary Goal:** PDF handling works locally
- **Key Deliverables:** 
  - PDF upload functionality with validation
  - In-browser PDF display using PDF.js
  - Local file system storage management
  - Side-by-side PDF display with input forms

## 📋 Technical Requirements

### Supported Document Types
- **Pay Slip / Salary Slip** (Image-based PDFs)
- **Form 16** (Image-based PDFs)
- **File Formats:** PDF only
- **File Size Limit:** 10MB maximum
- **Storage Duration:** Session-based (temporary storage)

### Technology Stack for Phase 2
| Component | Technology | Purpose |
|-----------|------------|---------|
| File Upload | HTML5 File API + FastAPI | Handle PDF uploads |
| PDF Display | PDF.js | In-browser PDF rendering |
| File Storage | Local file system | Temporary document storage |
| File Validation | Python libraries | PDF format validation |
| Session Management | FastAPI sessions | Associate files with user sessions |

## 🏗️ Implementation Architecture

### 1. Frontend Components

#### HTML Structure
```html
<!-- PDF Upload Section -->
<div class="upload-section">
    <div class="upload-area" id="uploadArea">
        <input type="file" id="pdfInput" accept=".pdf" hidden>
        <div class="upload-placeholder">
            <i class="fas fa-cloud-upload-alt"></i>
            <p>Click to upload or drag & drop your PDF</p>
            <small>Supported: Pay Slip, Salary Slip, or Form 16 (PDF only, max 10MB)</small>
        </div>
    </div>
</div>

<!-- PDF Display & Input Section -->
<div class="main-content" style="display: none;" id="mainContent">
    <div class="pdf-viewer-section">
        <canvas id="pdfCanvas"></canvas>
        <div class="pdf-controls">
            <button id="prevPage">Previous</button>
            <span id="pageInfo">Page 1 of 1</span>
            <button id="nextPage">Next</button>
        </div>
    </div>
    <div class="input-form-section">
        <!-- Data input forms will be loaded here -->
    </div>
</div>
```

#### CSS Styling
```css
.upload-section {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
}

.upload-area {
    border: 2px dashed #007bff;
    border-radius: 8px;
    padding: 3rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.upload-area:hover {
    border-color: #0056b3;
    background-color: #f8f9fa;
}

.main-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    padding: 2rem;
}

.pdf-viewer-section {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    background: #f8f9fa;
}

#pdfCanvas {
    width: 100%;
    height: auto;
    border: 1px solid #ccc;
}

.pdf-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
}
```

### 2. Backend API Endpoints

#### FastAPI Route Structure
```python
# api/pdf_handler.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
import os
import uuid
from pathlib import Path

router = APIRouter(prefix="/api/pdf", tags=["PDF Management"])

# Upload endpoint
@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    session_id: str = Depends(get_or_create_session)
):
    """Upload PDF file and store locally"""
    
# Download/serve endpoint  
@router.get("/serve/{file_id}")
async def serve_pdf(file_id: str, session_id: str = Depends(validate_session)):
    """Serve PDF file for display"""
    
# Delete endpoint
@router.delete("/delete/{file_id}")
async def delete_pdf(file_id: str, session_id: str = Depends(validate_session)):
    """Delete uploaded PDF file"""
```

### 3. File Management System

#### Local Storage Structure
```
project_root/
├── uploads/
│   ├── sessions/
│   │   ├── {session_id}/
│   │   │   ├── {file_id}_original.pdf
│   │   │   └── metadata.json
│   └── temp/
└── static/
    └── js/
        └── pdf-handler.js
```

#### File Metadata Storage
```json
{
  "file_id": "uuid-generated-id",
  "original_name": "salary_slip_jan_2024.pdf",
  "file_size": 2048576,
  "upload_timestamp": "2024-01-15T10:30:00Z",
  "document_type": "pay_slip",
  "session_id": "session-uuid",
  "file_path": "uploads/sessions/session-uuid/file-id_original.pdf"
}
```

## 🔧 Implementation Details

### 1. PDF Upload Implementation

#### Frontend JavaScript
```javascript
// static/js/pdf-handler.js
class PDFUploadHandler {
    constructor() {
        this.initializeUpload();
        this.initializePDFJS();
    }
    
    initializeUpload() {
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('pdfInput');
        
        // Drag and drop functionality
        uploadArea.addEventListener('dragover', this.handleDragOver);
        uploadArea.addEventListener('drop', this.handleDrop);
        uploadArea.addEventListener('click', () => fileInput.click());
        
        // File input change
        fileInput.addEventListener('change', this.handleFileSelect);
    }
    
    async handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            await this.uploadFile(file);
        }
    }
    
    async uploadFile(file) {
        // Validate file
        if (!this.validateFile(file)) return;
        
        // Show loading
        this.showUploadProgress();
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await fetch('/api/pdf/upload', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                await this.displayPDF(result.file_url);
                this.showMainContent();
            } else {
                throw new Error('Upload failed');
            }
        } catch (error) {
            this.showError('Upload failed. Please try again.');
        }
    }
    
    validateFile(file) {
        // Check file type
        if (file.type !== 'application/pdf') {
            this.showError('Please upload a PDF file only.');
            return false;
        }
        
        // Check file size (10MB limit)
        if (file.size > 10 * 1024 * 1024) {
            this.showError('File size must be less than 10MB.');
            return false;
        }
        
        return true;
    }
}
```

#### Backend Implementation
```python
# api/pdf_handler.py
import os
import uuid
import json
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from database.crud import create_document_record

router = APIRouter()

UPLOAD_DIR = Path("uploads/sessions")
ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), session_id: str = Depends(get_session)):
    # Validate file
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    
    # Create session directory
    session_dir = UPLOAD_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    
    # Save file
    file_path = session_dir / f"{file_id}_original.pdf"
    
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Save metadata
        metadata = {
            "file_id": file_id,
            "original_name": file.filename,
            "file_size": len(content),
            "upload_timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id,
            "file_path": str(file_path)
        }
        
        metadata_path = session_dir / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Store in database
        await create_document_record(session_id, file_id, file.filename, str(file_path))
        
        return {
            "success": True,
            "file_id": file_id,
            "file_url": f"/api/pdf/serve/{file_id}",
            "original_name": file.filename
        }
        
    except Exception as e:
        # Clean up on error
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail="Upload failed")

@router.get("/serve/{file_id}")
async def serve_pdf(file_id: str, session_id: str = Depends(get_session)):
    session_dir = UPLOAD_DIR / session_id
    file_path = session_dir / f"{file_id}_original.pdf"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"document_{file_id}.pdf"
    )
```

### 2. PDF Display Implementation

#### PDF.js Integration
```javascript
// static/js/pdf-viewer.js
class PDFViewer {
    constructor() {
        this.pdfDoc = null;
        this.pageNum = 1;
        this.pageCount = 0;
        this.scale = 1.5;
        this.canvas = document.getElementById('pdfCanvas');
        this.ctx = this.canvas.getContext('2d');
    }
    
    async loadPDF(url) {
        try {
            // Load PDF using PDF.js
            const loadingTask = pdfjsLib.getDocument(url);
            this.pdfDoc = await loadingTask.promise;
            this.pageCount = this.pdfDoc.numPages;
            
            // Render first page
            await this.renderPage(1);
            this.updatePageInfo();
            this.setupNavigation();
            
        } catch (error) {
            console.error('Error loading PDF:', error);
            this.showError('Failed to load PDF. Please try uploading again.');
        }
    }
    
    async renderPage(pageNumber) {
        const page = await this.pdfDoc.getPage(pageNumber);
        const viewport = page.getViewport({ scale: this.scale });
        
        // Set canvas dimensions
        this.canvas.height = viewport.height;
        this.canvas.width = viewport.width;
        
        // Render page
        const renderContext = {
            canvasContext: this.ctx,
            viewport: viewport
        };
        
        await page.render(renderContext).promise;
        this.pageNum = pageNumber;
    }
    
    setupNavigation() {
        document.getElementById('prevPage').onclick = () => {
            if (this.pageNum > 1) {
                this.renderPage(this.pageNum - 1);
            }
        };
        
        document.getElementById('nextPage').onclick = () => {
            if (this.pageNum < this.pageCount) {
                this.renderPage(this.pageNum + 1);
            }
        };
    }
    
    updatePageInfo() {
        document.getElementById('pageInfo').textContent = 
            `Page ${this.pageNum} of ${this.pageCount}`;
    }
}
```

### 3. Session Management

#### Session Handler
```python
# utils/session_manager.py
import uuid
from datetime import datetime, timedelta
from typing import Optional

class SessionManager:
    def __init__(self):
        self.sessions = {}  # In production, use database
    
    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'created_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(hours=24),
            'files': []
        }
        return session_id
    
    def validate_session(self, session_id: str) -> bool:
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        if datetime.utcnow() > session['expires_at']:
            self.cleanup_session(session_id)
            return False
        
        return True
    
    def cleanup_session(self, session_id: str):
        # Remove files and session data
        if session_id in self.sessions:
            session_dir = Path(f"uploads/sessions/{session_id}")
            if session_dir.exists():
                import shutil
                shutil.rmtree(session_dir)
            del self.sessions[session_id]
```

## 🧪 Testing Strategy

### 1. File Upload Testing
- [ ] Test PDF file upload with valid files
- [ ] Test file size validation (10MB limit)
- [ ] Test file type validation (PDF only)
- [ ] Test drag and drop functionality
- [ ] Test error handling for invalid files
- [ ] Test session-based file association

### 2. PDF Display Testing
- [ ] Test PDF rendering with different PDF types
- [ ] Test multi-page navigation
- [ ] Test zoom functionality
- [ ] Test responsive display on different screen sizes
- [ ] Test PDF loading performance
- [ ] Test error handling for corrupted PDFs

### 3. File Management Testing
- [ ] Test file storage and retrieval
- [ ] Test session cleanup
- [ ] Test concurrent uploads
- [ ] Test file deletion
- [ ] Test metadata storage and retrieval

## 📝 Database Integration

### Document Storage Schema
```sql
-- documents table
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    file_id TEXT UNIQUE NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    file_type TEXT DEFAULT 'pdf',
    document_type TEXT, -- 'pay_slip' or 'form_16'
    upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES user_sessions (session_id)
);
```

### Database Operations
```python
# database/crud.py
async def create_document_record(session_id: str, file_id: str, file_name: str, file_path: str):
    query = """
    INSERT INTO documents (session_id, file_id, file_name, file_path, file_size)
    VALUES (?, ?, ?, ?, ?)
    """
    # Implementation depends on database connection

async def get_document_by_file_id(file_id: str) -> Optional[dict]:
    query = "SELECT * FROM documents WHERE file_id = ?"
    # Implementation depends on database connection
```

## 🚀 Deployment Checklist for Phase 2

### Prerequisites
- [ ] FastAPI application structure set up
- [ ] SQLite database initialized
- [ ] Static file serving configured
- [ ] Session management implemented

### Phase 2 Completion Criteria
- [ ] PDF upload functionality working
- [ ] PDF display with PDF.js working
- [ ] File validation implemented
- [ ] Session-based file management
- [ ] Error handling and user feedback
- [ ] Responsive UI for PDF viewing
- [ ] Local file cleanup mechanism

### Next Phase Integration
- [ ] Document type detection (Pay Slip vs Form 16)
- [ ] Data extraction preparation
- [ ] Form loading based on document type
- [ ] Integration with Phase 3 data input forms

## 🔍 Error Handling & User Experience

### Error Scenarios
1. **Invalid File Type:** Clear message with supported formats
2. **File Too Large:** Size limit information and suggestions
3. **Upload Failed:** Retry mechanism with error details
4. **PDF Corrupted:** Alternative upload suggestion
5. **Session Expired:** Graceful session renewal

### User Feedback
- Progress indicators during upload
- Success confirmation with preview
- Clear error messages with actionable solutions
- Loading states for PDF rendering
- Intuitive navigation controls

## 📊 Performance Considerations

### Optimization Strategies
- Lazy loading for large PDFs
- Canvas rendering optimization
- File compression for storage
- Efficient session cleanup
- Memory management for PDF processing

### Monitoring Points
- Upload success rate
- PDF rendering time
- File size distribution
- Session duration
- Error frequency

---

**Phase 2 Status:** Ready for Implementation
**Next Phase:** Phase 3 - Manual Data Input Forms with Validation 