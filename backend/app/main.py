from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routes import uploads  # ensure package import paths valid
from app.database import engine, Base

# Create the FastAPI app
app = FastAPI(title="Worship Session Integration")

# Create the database tables
Base.metadata.create_all(bind=engine)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Limiter
limiter = Limiter(key_func=get_remote_address)

# Add rate limiting middleware and exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include the uploads router
app.include_router(uploads.router, prefix="/uploads", tags=["uploads"])

# Root endpoint
@app.get("/")
def root():
    return {"ok": True}
