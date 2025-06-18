import contextlib
import warnings
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi.routing import Mount

with warnings.catch_warnings():
    warnings.simplefilter('ignore')

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)

import openhands.agenthub  # noqa F401 (we import this to get the agents registered)
from openhands import __version__
from openhands.server.routes.conversation import app as conversation_api_router
from openhands.server.routes.feedback import app as feedback_api_router
from openhands.server.routes.files import app as files_api_router
from openhands.server.routes.git import app as git_api_router
from openhands.server.routes.health import add_health_endpoints
from openhands.server.routes.manage_conversations import (
    app as manage_conversation_api_router,
    public_app as public_conversation_api_router,
)
from openhands.server.routes.mcp import mcp_server
from openhands.server.routes.public import app as public_api_router
from openhands.server.routes.secrets import app as secrets_router
from openhands.server.routes.security import app as security_api_router
from openhands.server.routes.settings import app as settings_router
from openhands.server.routes.trajectory import app as trajectory_router
from openhands.server.shared import conversation_manager

# Import HF Spaces routes if available
try:
    from openhands.server.routes.hf_spaces import router as hf_spaces_router
    HF_SPACES_AVAILABLE = True
except ImportError:
    HF_SPACES_AVAILABLE = False

# Import simple conversation routes
try:
    from openhands.server.routes.simple_conversation import router as simple_conversation_router
    SIMPLE_CONVERSATION_AVAILABLE = True
except ImportError:
    SIMPLE_CONVERSATION_AVAILABLE = False

mcp_app = mcp_server.http_app(path='/mcp')


def combine_lifespans(*lifespans):
    # Create a combined lifespan to manage multiple session managers
    @contextlib.asynccontextmanager
    async def combined_lifespan(app):
        async with contextlib.AsyncExitStack() as stack:
            for lifespan in lifespans:
                await stack.enter_async_context(lifespan(app))
            yield

    return combined_lifespan


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with conversation_manager:
        yield


app = FastAPI(
    title='OpenHands',
    description='OpenHands: Code Less, Make More',
    version=__version__,
    lifespan=combine_lifespans(_lifespan, mcp_app.lifespan),
    routes=[Mount(path='/mcp', app=mcp_app)],
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add root endpoint
@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return JSONResponse({
        "name": "OpenHands Backend API",
        "version": __version__,
        "description": "OpenHands: Code Less, Make More",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "api_config": "/api/options/config",
            "api_models": "/api/options/models",
            "api_agents": "/api/options/agents",
            "conversations": "/api/conversations",
            "simple_conversations": "/api/conversations/simple",
            "test_chat": "/test-chat",
            "hf_status": "/api/hf/status",
            "hf_ready": "/api/hf/ready",
            "hf_environment": "/api/hf/environment"
        },
        "documentation": "/docs",
        "openapi": "/openapi.json"
    })

@app.post("/test-chat")
async def test_chat():
    """Ultra simple test endpoint for chat functionality."""
    try:
        import uuid
        from datetime import datetime
        
        chat_id = uuid.uuid4().hex
        
        return JSONResponse({
            "status": "success",
            "chat_id": chat_id,
            "message": "Test chat created successfully",
            "timestamp": datetime.now().isoformat(),
            "ready": True
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Test chat failed: {str(e)}"
            }
        )

# Add global exception handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Handle 404 errors with helpful information."""
    return JSONResponse(
        status_code=404,
        content={
            "detail": f"Endpoint not found: {request.url.path}",
            "message": "The requested endpoint does not exist",
            "available_endpoints": {
                "root": "/",
                "health": "/health",
                "docs": "/docs",
                "api_config": "/api/options/config",
                "hf_status": "/api/hf/status"
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "body": exc.body
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred",
            "type": type(exc).__name__
        }
    )

app.include_router(public_api_router)
app.include_router(public_conversation_api_router)  # Public conversations endpoint
app.include_router(files_api_router)
app.include_router(security_api_router)
app.include_router(feedback_api_router)
app.include_router(conversation_api_router)
app.include_router(manage_conversation_api_router)
app.include_router(settings_router)
app.include_router(secrets_router)
app.include_router(git_api_router)
app.include_router(trajectory_router)

# Add HF Spaces routes if available
if HF_SPACES_AVAILABLE:
    app.include_router(hf_spaces_router)
    logger.info("✅ HF Spaces routes included")
else:
    logger.warning("⚠️ HF Spaces routes not available")

# Add simple conversation routes if available
if SIMPLE_CONVERSATION_AVAILABLE:
    app.include_router(simple_conversation_router)
    logger.info("✅ Simple conversation routes included")
else:
    logger.warning("⚠️ Simple conversation routes not available")

add_health_endpoints(app)
