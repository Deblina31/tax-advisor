"""
Tax Advisor Application - Phase 2: PDF Upload & Display System
FastAPI main application file
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os

# Import database initialization
try:
    from database.connection import init_db, test_db_connection
    from database.models import Base
    database_available = True
except ImportError:
    print("Warning: Database components not found")
    database_available = False

# Import API routes
try:
    from api.pdf_routes import router as pdf_router
except ImportError:
    print("Warning: PDF routes not found")
    pdf_router = None

# AI routes removed - LLM integration no longer available

# Create FastAPI app
app = FastAPI(
    title="Tax Advisor - PDF Upload System",
    description="PDF Upload and Display System for Tax Document Analysis",
    version="1.0.0"
)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Include API routes
if pdf_router:
    app.include_router(pdf_router)

# AI router removed - LLM integration no longer available

@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    if database_available:
        try:
            print("Initializing database...")
            init_db()
            
            # Test database connection
            if test_db_connection():
                print("✅ Database initialized and connected successfully!")
            else:
                print("❌ Database connection test failed!")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
    else:
        print("⚠️  Database not available - running without database storage")

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon to avoid 404 errors"""
    return {"message": "No favicon available"}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main application page"""
    return templates.TemplateResponse("index.html", {"request": request})

# AI demo route removed - LLM integration no longer available

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Tax Advisor API is running"}

@app.get("/database/health")
async def database_health_check():
    """Database health check endpoint"""
    if not database_available:
        return {"status": "unavailable", "message": "Database components not loaded"}
    
    try:
        if test_db_connection():
            return {"status": "healthy", "message": "Database connection successful"}
        else:
            return {"status": "unhealthy", "message": "Database connection failed"}
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}

# Create uploads directory if it doesn't exist
uploads_dir = "uploads/sessions"
os.makedirs(uploads_dir, exist_ok=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 