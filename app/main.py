from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import traceback
from app.routes.predict import router as predict_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Focus API",
    description="AI-powered focus detection API with multiple models",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to FastAPI with more specific configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Validation error",
            "details": exc.errors(),
            "status_code": 422
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500
        }
    )

# Include routers
app.include_router(predict_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Welcome to the AI Focus Detection API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "AI Focus API is running"
    }

# For Vercel deployment
@app.get("/api/health")
async def api_health_check():
    return {
        "status": "healthy",
        "message": "AI Focus API is running"
    }
