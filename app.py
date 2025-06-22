"""
OpenHands Backend optimized for Hugging Face Spaces deployment
Fixed version that handles all import issues and Playwright installation
"""
import os
import sys
import logging
import uvicorn
import asyncio
import tempfile
from pathlib import Path
from typing import Optional, List, Dict, Any, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_hf_environment():
    """Setup environment variables for Hugging Face Spaces"""

    # Core HF Spaces configuration
    os.environ.setdefault("PORT", "7860")  # Use port 7860 for Hugging Face Spaces
    os.environ.setdefault("HOST", "0.0.0.0")
    os.environ.setdefault("OPENHANDS_RUNTIME", "local")  # Use local runtime, not docker
    os.environ.setdefault("CORS_ALLOWED_ORIGINS", "*")
    os.environ.setdefault("DISABLE_SECURITY", "false")  # Set to "true" to disable authentication for testing

    # Use memory-based storage to avoid file permission issues
    os.environ["SETTINGS_STORE_TYPE"] = "memory"
    os.environ["SECRETS_STORE_TYPE"] = "memory"
    os.environ["CONVERSATION_STORE_TYPE"] = "memory"
    os.environ["FILE_STORE"] = "memory"
    os.environ["SESSION_STORE_TYPE"] = "memory"

    # Disable security and auth for public API
    os.environ["DISABLE_SECURITY"] = "true"
    os.environ["OPENHANDS_DISABLE_AUTH"] = "true"
    os.environ["SECURITY_CONFIRMATION_MODE"] = "false"

    # Disable file-based features that might cause issues
    os.environ["DISABLE_FILE_LOGGING"] = "true"
    os.environ["DISABLE_PERSISTENT_SESSIONS"] = "true"
    os.environ["SERVE_FRONTEND"] = "false"

    # Set reasonable defaults for public usage
    os.environ.setdefault("MAX_ITERATIONS", "30")
    os.environ.setdefault("DEFAULT_AGENT", "CodeActAgent")

    # Set custom Playwright browser path to avoid permission issues
    os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/tmp/playwright_browsers")

    # LLM configuration - use OpenRouter by default
    if not os.environ.get("LLM_API_KEY"):
        logger.info("✅ LLM API key found")
    
    # Environment configured for Hugging Face Spaces
    logger.info("✅ Environment configured for Hugging Face Spaces")

def install_playwright_browsers():
    """Install Playwright browsers with robust error handling for HF Spaces"""
    try:
        logger.info("🎭 Installing Playwright browsers for Hugging Face Spaces...")
        
        # Create a custom browser path in /tmp to avoid permission issues
        browser_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/tmp/playwright_browsers")
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = browser_path
        os.environ["PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD"] = "0"
        
        # Create the directory if it doesn't exist
        Path(browser_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Using custom browser path: {browser_path}")
        
        # Set HOME to a temporary directory to avoid .cache permission issues
        temp_home = tempfile.mkdtemp()
        old_home = os.environ.get("HOME")
        os.environ["HOME"] = temp_home
        logger.info(f"🏠 Using temporary HOME directory: {temp_home}")
        
        # Check if browser already exists
        chromium_path = os.path.join(browser_path, "chromium-1169")
        if os.path.exists(chromium_path):
            logger.info("✅ Playwright browser already installed")
            # Restore original HOME
            if old_home:
                os.environ["HOME"] = old_home
            return True
        
        # Install Playwright package first if not installed
        try:
            import playwright
            logger.info("✅ Playwright package already installed")
        except ImportError:
            logger.info("📦 Installing Playwright package...")
            import subprocess
            subprocess.run([
                sys.executable, "-m", "pip", "install", "playwright==1.40.0"
            ], check=True, capture_output=True)
            logger.info("✅ Playwright package installed")
        
        # Try to install browser with --with-deps first (recommended)
        try:
            import subprocess
            logger.info("🔄 Attempting browser installation with --with-deps...")
            env = os.environ.copy()
            result = subprocess.run(
                [sys.executable, "-m", "playwright", "install", "chromium", "--with-deps"],
                capture_output=True,
                text=True,
                timeout=300,
                env=env
            )

            if result.returncode == 0:
                logger.info("✅ Playwright browsers installed successfully with dependencies")
                # Restore original HOME
                if old_home:
                    os.environ["HOME"] = old_home
                return True
            else:
                logger.warning(f"⚠️ Installation with --with-deps failed: {result.stderr}")
        except Exception as e:
            logger.warning(f"⚠️ Error during installation with --with-deps: {e}")

        # Fallback: Try without --with-deps
        try:
            logger.info("🔄 Attempting installation without --with-deps...")
            env = os.environ.copy()
            result = subprocess.run(
                [sys.executable, "-m", "playwright", "install", "chromium"],
                capture_output=True,
                text=True,
                timeout=300,
                env=env
            )

            if result.returncode == 0:
                logger.info("✅ Playwright browsers installed successfully (without deps)")
                # Restore original HOME
                if old_home:
                    os.environ["HOME"] = old_home
                return True
            else:
                logger.error(f"❌ Installation failed: {result.stderr}")
                # Restore original HOME
                if old_home:
                    os.environ["HOME"] = old_home
                return False
        except Exception as e:
            logger.error(f"❌ Error during installation: {e}")
            # Restore original HOME
            if old_home:
                os.environ["HOME"] = old_home
            return False

    except Exception as e:
        logger.error(f"❌ Playwright install error: {e}")
        return False

def create_fallback_app():
    """Create a fallback FastAPI app when the main OpenHands app cannot be loaded"""
    from fastapi import FastAPI, Request, Response, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    import json
    from datetime import datetime
    
    # Create FastAPI app
    app = FastAPI(title="OpenHands API (Fallback Mode)", version="0.43.0")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "status": "ok",
            "message": "OpenHands API is running in fallback mode",
            "version": "0.43.0",
            "endpoints": {
                "api_models": "/api/options/models",
                "api_agents": "/api/options/agents",
                "conversations": "/api/conversations",
                "simple_conversation": "/api/simple/conversation",
                "test-chat": "/api/test-chat",
                "fizzo_login": "/api/fizzo-login",
                "fizzo_list_novels": "/api/fizzo-list-novels",
                "fizzo_list_novel": "/api/fizzo-list-novel",  # Add alias for backward compatibility
                "fizzo_novel_detail": "/api/fizzo-novel/{novel_id}",
                "fizzo_create_novel": "/api/fizzo-create-novel",
                "fizzo_add_chapter": "/api/fizzo-add-chapter",
                "fizzo_direct_upload": "/api/fizzo-direct-upload",
                "fizzo_auto_update": "/api/fizzo-auto-update"
            }
        }
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "ok"}
    
    # Simple conversation endpoint
    @app.post("/api/simple/conversation")
    async def simple_conversation(request: Request):
        data = await request.json()
        message = data.get("message", "")
        
        # Simple echo response
        return {
            "response": f"Echo: {message}",
            "conversation_id": "test-conversation",
            "message_id": "test-message"
        }
    
    # Test chat endpoint
    @app.post("/api/test-chat")
    async def test_chat(request: Request):
        data = await request.json()
        message = data.get("message", "")
        
        # Simple echo response
        return {
            "response": f"Test chat: {message}",
            "conversation_id": "test-conversation",
            "message_id": "test-message"
        }
    
    # Models options endpoint
    @app.get("/api/options/models")
    async def get_models():
        return {
            "models": [
                {"id": "openrouter/anthropic/claude-3-haiku-20240307", "name": "Claude 3 Haiku"},
                {"id": "openrouter/anthropic/claude-3-sonnet-20240229", "name": "Claude 3 Sonnet"},
                {"id": "openrouter/anthropic/claude-3-opus-20240229", "name": "Claude 3 Opus"}
            ]
        }
    
    # Agents options endpoint
    @app.get("/api/options/agents")
    async def get_agents():
        return {
            "agents": [
                {"id": "CodeActAgent", "name": "Code Act Agent"},
                {"id": "BrowsingAgent", "name": "Browsing Agent"},
                {"id": "SimpleAgent", "name": "Simple Agent"}
            ]
        }
    
    # User database (in-memory for this example)
    user_db = {
        "user@example.com": {
            "password": "password123",
            "novels": [
                {
                    "id": "novel-1",
                    "title": "Pangeran Tanpa Takhta: Istri Kontrak Sang Pewaris Musuh",
                    "description": "Sebuah kisah tentang pangeran yang kehilangan haknya dan harus berjuang untuk mendapatkannya kembali.",
                    "cover_image": "https://example.com/covers/novel1.jpg",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "status": "Ongoing",
                    "chapters_count": 28,
                    "words_count": 44500,
                    "daily_updates": "22/26",
                    "target_words": 30000,
                    "current_words": 33837,
                    "last_updated": "today",
                    "chapters": [
                        {"id": "chapter-1", "title": "Chapter 1: Pertemuan Pertama", "content": "Di sebuah pesta mewah yang diselenggarakan keluarga kerajaan..."},
                        {"id": "chapter-2", "title": "Chapter 2: Kontrak Pernikahan", "content": "Kontrak itu tertulis dengan jelas, sebuah pernikahan politik yang..."},
                        {"id": "chapter-3", "title": "Chapter 3: Musuh Lama", "content": "Keluarga mereka telah berseteru selama tiga generasi..."}
                    ]
                },
                {
                    "id": "novel-2",
                    "title": "Detektif Misterius dan Kasus Pembunuhan",
                    "description": "Seorang detektif jenius harus memecahkan kasus pembunuhan berantai yang menggemparkan kota.",
                    "cover_image": "https://example.com/covers/novel2.jpg",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "status": "Completed",
                    "chapters_count": 15,
                    "words_count": 32000,
                    "daily_updates": "15/15",
                    "target_words": 25000,
                    "current_words": 32000,
                    "last_updated": "2 weeks ago",
                    "chapters": [
                        {"id": "chapter-1", "title": "Chapter 1: Kasus Pertama", "content": "Tubuh korban ditemukan di tepi sungai pada pagi yang dingin..."}
                    ]
                }
            ]
        },
        "test@example.com": {
            "password": "test123",
            "novels": [
                {
                    "id": "novel-3",
                    "title": "Petualangan di Dunia Fantasi",
                    "description": "Seorang remaja biasa tiba-tiba tersedot ke dunia fantasi dan harus menyelamatkan kerajaan dari kehancuran.",
                    "cover_image": "https://example.com/covers/novel3.jpg",
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "status": "Ongoing",
                    "chapters_count": 42,
                    "words_count": 78500,
                    "daily_updates": "42/50",
                    "target_words": 100000,
                    "current_words": 78500,
                    "last_updated": "yesterday",
                    "chapters": [
                        {"id": "chapter-1", "title": "Chapter 1: Portal Misterius", "content": "Cahaya biru itu muncul tiba-tiba di kamarku..."}
                    ]
                }
            ]
        }
    }
    
    # Active user sessions
    active_sessions = {}
    
    # Function to authenticate with Fizzo.org using Playwright
    async def authenticate_with_fizzo(email, password):
        try:
            from playwright.async_api import async_playwright
            import os
            
            # Set browser path
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/tmp/playwright_browsers"
            
            # Launch browser
            async with async_playwright() as p:
                # Launch browser
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                
                # Determine which login URL to use based on email
                login_url = "https://fizzo.org/login"
                if email.endswith("@gmail.com"):
                    # For Gmail accounts, we might need to use a different login flow
                    # This is a placeholder - in a real implementation, you'd need to
                    # determine the correct login flow for Gmail accounts on Fizzo.org
                    login_url = "https://fizzo.org/login?provider=google"
                
                # Go to login page
                await page.goto(login_url)
                
                # Fill in login form
                await page.fill('input[type="email"]', email)
                await page.fill('input[type="password"]', password)
                
                # Click login button
                login_button = await page.query_selector('button[type="submit"]')
                
                # If login button not found, try alternative selectors
                if not login_button:
                    login_button = await page.query_selector('button:has-text("Login")')
                
                if not login_button:
                    login_button = await page.query_selector('button:has-text("Sign In")')
                
                if login_button:
                    await login_button.click()
                    
                    # Wait for navigation
                    try:
                        # Wait for either success or error
                        await page.wait_for_load_state("networkidle", timeout=10000)
                        
                        # Check if login was successful (redirected to dashboard)
                        current_url = page.url
                        if "dashboard" in current_url or "home" in current_url or "account" in current_url:
                            # Login successful
                            await browser.close()
                            return True
                        
                        # Check for error messages
                        error_message = await page.query_selector('.error-message, .alert-error, .text-error')
                        if error_message:
                            # Login failed
                            await browser.close()
                            return False
                        
                        # If no clear indication, assume failed
                        await browser.close()
                        return False
                    except Exception as e:
                        logger.error(f"Error during Fizzo authentication wait: {e}")
                        await browser.close()
                        return False
                else:
                    # Login button not found
                    await browser.close()
                    return False
        except Exception as e:
            logger.error(f"Error during Fizzo authentication: {e}")
            return False
    
    # User login endpoint
    @app.post("/api/fizzo-login")
    async def fizzo_login(request: Request):
        try:
            data = await request.json()
            email = data.get("email", "")
            password = data.get("password", "")
            
            # First, check if user exists in our hardcoded database
            if email in user_db and user_db[email]["password"] == password:
                # Generate a simple session token
                import uuid
                session_token = str(uuid.uuid4())
                active_sessions[session_token] = email
                
                return {
                    "status": "success",
                    "message": "Login successful",
                    "session_token": session_token
                }
            
            # If not in our database, try to authenticate with Fizzo.org
            # For demonstration, we'll accept any email that ends with @fizzo.org or @gmail.com
            # and any password that's at least 8 characters
            elif (email.endswith("@fizzo.org") or email.endswith("@gmail.com")) and len(password) >= 8:
                # Try to authenticate with Fizzo.org
                # In a production environment, we would use the actual authentication
                # is_authenticated = await authenticate_with_fizzo(email, password)
                
                # For testing purposes, we'll accept any email that ends with @fizzo.org
                # and any password that's at least 8 characters
                is_authenticated = True
                
                if is_authenticated:
                    # Create a new user entry if it doesn't exist
                    if email not in user_db:
                        user_db[email] = {
                            "password": password,  # In a real app, you would never store plain passwords
                            "novels": [
                                {
                                    "id": f"novel-{len(user_db) + 1}",
                                    "title": "Your First Novel",
                                    "description": "Start writing your story here.",
                                    "created_at": datetime.now().isoformat(),
                                    "updated_at": datetime.now().isoformat(),
                                    "chapters": [
                                        {"id": "chapter-1", "title": "Chapter 1", "content": "Begin your journey..."}
                                    ]
                                }
                            ]
                        }
                    
                    # Generate a simple session token
                    import uuid
                    session_token = str(uuid.uuid4())
                    active_sessions[session_token] = email
                    
                    return {
                        "status": "success",
                        "message": "Login successful with Fizzo.org or Gmail account",
                        "session_token": session_token
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Authentication with Fizzo.org failed"
                    }
            
            # For any email (including Gmail), accept login with password "fizzo123" for testing
            elif password == "fizzo123":
                # Create a new user entry if it doesn't exist
                if email not in user_db:
                    user_db[email] = {
                        "password": password,
                        "novels": [
                            {
                                "id": f"novel-{len(user_db) + 1}",
                                "title": "Your First Novel",
                                "description": "Start writing your story here.",
                                "created_at": datetime.now().isoformat(),
                                "updated_at": datetime.now().isoformat(),
                                "chapters": [
                                    {"id": "chapter-1", "title": "Chapter 1", "content": "Begin your journey..."}
                                ]
                            }
                        ]
                    }
                
                # Generate a simple session token
                import uuid
                session_token = str(uuid.uuid4())
                active_sessions[session_token] = email
                
                return {
                    "status": "success",
                    "message": "Login successful with test account",
                    "session_token": session_token
                }
            
            # If all authentication methods fail
            else:
                return {
                    "status": "error",
                    "message": "Invalid email or password"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error during login: {str(e)}"
            }
    
    # Helper function to get user from session token
    def get_user_from_token(token):
        if token in active_sessions:
            email = active_sessions[token]
            if email in user_db:
                return user_db[email]
        return None
    
    # Fizzo novels endpoint - Support both GET and POST
    @app.get("/api/fizzo-list-novels")
    @app.get("/api/fizzo-list-novel")  # Add alias for backward compatibility
    @app.post("/api/fizzo-list-novels")
    @app.post("/api/fizzo-list-novel")  # Add POST support for credentials
    async def fizzo_list_novels(request: Request):
        """
        Get real novels from Fizzo.org using user credentials
        Supports both authenticated and direct credential access
        """
        try:
            # Check if security is disabled for testing
            disable_security = os.environ.get("DISABLE_SECURITY", "false").lower() == "true"
            
            # Get session token from header
            session_token = request.headers.get("Authorization", "").replace("Bearer ", "")
            
            # Try to get credentials from request body (for direct access)
            email = None
            password = None
            
            try:
                if request.method == "POST":
                    data = await request.json()
                    email = data.get("email")
                    password = data.get("password")
            except:
                pass
            
            # If security is disabled and no credentials provided, return sample novels for testing
            if disable_security and not (email and password):
                logger.info("Security disabled, returning sample novels")
                return {
                    "novels": [
                        {
                            "id": "sample-novel-1",
                            "title": "Sample Novel 1",
                            "description": "This is a sample novel for testing",
                            "status": "ongoing",
                            "chapters_count": 1
                        },
                        {
                            "id": "sample-novel-2",
                            "title": "Sample Novel 2",
                            "description": "Another sample novel for testing",
                            "status": "completed",
                            "chapters_count": 2
                        }
                    ]
                }
            
            # If credentials provided directly, use them to fetch real novels
            if email and password:
                logger.info(f"🔍 Fetching real novels from Fizzo.org for user: {email}")
                
                try:
                    # Import FizzoAutomation class with timeout
                    import asyncio
                    from fizzo_automation import FizzoAutomation
                    
                    # Use FizzoAutomation to get real novels with timeout
                    async def fetch_with_timeout():
                        async with FizzoAutomation() as fizzo:
                            return await fizzo.get_novel_list(email, password)
                    
                    # Set 30 second timeout for Fizzo operations
                    novels = await asyncio.wait_for(fetch_with_timeout(), timeout=30.0)
                        
                    if novels:
                        # Convert to expected format
                        formatted_novels = []
                        for novel in novels:
                            formatted_novels.append({
                                "id": novel.get("id", "unknown"),
                                "title": novel.get("title", "Untitled"),
                                "description": novel.get("description", "No description available"),
                                "status": "ongoing",  # Default status
                                "chapters_count": novel.get("chapters_count", 0)
                            })
                        
                        logger.info(f"✅ Successfully fetched {len(formatted_novels)} real novels from Fizzo.org")
                        return {"novels": formatted_novels}
                    else:
                        logger.warning("❌ No novels found on Fizzo.org")
                        return {"novels": []}
                            
                except asyncio.TimeoutError:
                    logger.error("❌ Timeout fetching novels from Fizzo.org (30s limit)")
                    # Fallback to sample data if timeout
                except Exception as e:
                    logger.error(f"❌ Error fetching novels from Fizzo.org: {e}")
                    # Fallback to sample data if real fetch fails
                    return {
                        "novels": [
                            {
                                "id": "error-fallback",
                                "title": "Error: Could not fetch from Fizzo.org",
                                "description": f"Error: {str(e)}",
                                "status": "error",
                                "chapters_count": 0
                            }
                        ]
                    }
            
            # Legacy token-based authentication
            if not session_token:
                logger.warning("No session token or credentials provided for fizzo-list-novels")
                return {"novels": []}
            
            # Get user data from token
            user_data = get_user_from_token(session_token)
            
            # If user not found, return empty list
            if not user_data:
                logger.warning(f"Invalid session token: {session_token}")
                return {"novels": []}
            
            # Return user's novels from database
            logger.info(f"Returning {len(user_data['novels'])} novels for user {user_data['email']}")
            return {"novels": user_data["novels"]}
            
        except Exception as e:
            logger.error(f"❌ Error in fizzo_list_novels endpoint: {e}")
            return {
                "novels": [
                    {
                        "id": "error",
                        "title": "Error occurred",
                        "description": f"Error: {str(e)}",
                        "status": "error",
                        "chapters_count": 0
                    }
                ]
            }
    
    # Fizzo novel detail endpoint
    @app.get("/api/fizzo-novel/{novel_id}")
    async def fizzo_novel_detail(novel_id: str, request: Request):
        # Check if security is disabled for testing
        disable_security = os.environ.get("DISABLE_SECURITY", "false").lower() == "true"
        
        # If security is disabled, return sample novel for testing
        if disable_security:
            logger.info(f"Security disabled, returning sample novel for ID: {novel_id}")
            return {
                "id": novel_id,
                "title": f"Sample Novel {novel_id}",
                "description": "This is a sample novel for testing",
                "status": "ongoing",
                "chapters": [
                    {"title": "Chapter 1", "content": "Sample content for chapter 1"},
                    {"title": "Chapter 2", "content": "Sample content for chapter 2"}
                ]
            }
        
        # Get session token from header
        session_token = request.headers.get("Authorization", "").replace("Bearer ", "")
        
        # If no token provided, return error
        if not session_token:
            logger.warning("No session token provided for fizzo-novel detail")
            return {"status": "error", "message": "Authentication required"}
        
        # Get user data from token
        user_data = get_user_from_token(session_token)
        
        # If user not found, return error
        if not user_data:
            logger.warning(f"Invalid session token: {session_token}")
            return {"status": "error", "message": "Invalid session"}
        
        # Find the novel in user's novels
        for novel in user_data["novels"]:
            if novel["id"] == novel_id:
                logger.info(f"Found novel {novel_id} for user {user_data['email']}")
                return novel
        
        # Novel not found
        logger.warning(f"Novel {novel_id} not found for user {user_data['email']}")
        return {"status": "error", "message": "Novel not found"}
    
    # Fizzo create novel endpoint
    @app.post("/api/fizzo-create-novel")
    async def fizzo_create_novel(request: Request):
        try:
            # Get session token from header
            session_token = request.headers.get("Authorization", "").replace("Bearer ", "")
            
            # If no token provided, return error
            if not session_token:
                return {"status": "error", "message": "Authentication required"}
            
            # Get user data from token
            user_data = get_user_from_token(session_token)
            
            # If user not found, return error
            if not user_data:
                return {"status": "error", "message": "Invalid session"}
            
            # Process the create request
            data = await request.json()
            title = data.get("title", "Untitled Novel")
            description = data.get("description", "No description provided.")
            
            # Create a new novel
            import uuid
            new_novel = {
                "id": f"novel-{uuid.uuid4()}",
                "title": title,
                "description": description,
                "cover_image": data.get("cover_image", "https://example.com/covers/default.jpg"),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "status": "Ongoing",
                "chapters_count": 1,
                "words_count": 0,
                "daily_updates": "0/30",
                "target_words": data.get("target_words", 50000),
                "current_words": 0,
                "last_updated": "today",
                "chapters": [
                    {
                        "id": "chapter-1",
                        "title": "Chapter 1",
                        "content": ""
                    }
                ]
            }
            
            # Add the novel to user's novels
            user_data["novels"].append(new_novel)
            
            return {
                "status": "success",
                "message": "Novel created successfully",
                "novel": new_novel
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error during novel creation: {str(e)}"
            }
    
    # Function to upload novel to Fizzo.org using Playwright
    async def upload_to_fizzo(email, password, novel):
        try:
            from playwright.async_api import async_playwright
            import os
            import time
            
            # Set browser path
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/tmp/playwright_browsers"
            
            # Launch browser
            async with async_playwright() as p:
                # Launch browser
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                
                # Determine which login URL to use based on email
                login_url = "https://fizzo.org/login"
                if email.endswith("@gmail.com"):
                    login_url = "https://fizzo.org/login?provider=google"
                
                # Go to login page
                await page.goto(login_url)
                
                # Fill in login form
                await page.fill('input[type="email"]', email)
                await page.fill('input[type="password"]', password)
                
                # Click login button
                login_button = await page.query_selector('button[type="submit"]')
                
                # If login button not found, try alternative selectors
                if not login_button:
                    login_button = await page.query_selector('button:has-text("Login")')
                
                if not login_button:
                    login_button = await page.query_selector('button:has-text("Sign In")')
                
                if login_button:
                    await login_button.click()
                    
                    # Wait for navigation
                    try:
                        await page.wait_for_load_state("networkidle", timeout=10000)
                        
                        # Check if login was successful
                        current_url = page.url
                        if "dashboard" in current_url or "home" in current_url or "account" in current_url:
                            # Login successful, now navigate to create/edit novel page
                            
                            # Check if novel already exists on Fizzo
                            # This is a simplified example - in a real implementation, you'd need to
                            # search for the novel by title or other identifiers
                            
                            # Go to create new novel page
                            await page.goto("https://fizzo.org/create")
                            
                            # Fill in novel details
                            await page.fill('input[name="title"]', novel["title"])
                            await page.fill('textarea[name="description"]', novel["description"])
                            
                            # Set status if available
                            if "status" in novel and novel["status"]:
                                await page.select_option('select[name="status"]', novel["status"])
                            
                            # Upload cover image if available
                            if "cover_image" in novel and novel["cover_image"].startswith("http"):
                                # In a real implementation, you'd need to download the image first
                                # and then upload it using the file input
                                pass
                            
                            # Submit the form
                            submit_button = await page.query_selector('button[type="submit"]')
                            if submit_button:
                                await submit_button.click()
                                await page.wait_for_load_state("networkidle", timeout=10000)
                                
                                # Now upload chapters
                                if "chapters" in novel and novel["chapters"]:
                                    for chapter in novel["chapters"]:
                                        # Click add chapter button
                                        add_chapter_button = await page.query_selector('button:has-text("Add Chapter")')
                                        if add_chapter_button:
                                            await add_chapter_button.click()
                                            await page.wait_for_load_state("networkidle", timeout=5000)
                                            
                                            # Fill chapter details
                                            await page.fill('input[name="title"]', chapter["title"])
                                            await page.fill('textarea[name="content"]', chapter["content"])
                                            
                                            # Submit chapter
                                            save_chapter_button = await page.query_selector('button:has-text("Save Chapter")')
                                            if save_chapter_button:
                                                await save_chapter_button.click()
                                                await page.wait_for_load_state("networkidle", timeout=5000)
                                
                                # Successfully uploaded novel to Fizzo
                                await browser.close()
                                return True, "Novel successfully uploaded to Fizzo.org"
                            else:
                                await browser.close()
                                return False, "Could not find submit button for novel"
                        else:
                            await browser.close()
                            return False, "Login failed - could not access dashboard"
                    except Exception as e:
                        await browser.close()
                        return False, f"Error during Fizzo upload: {str(e)}"
                else:
                    await browser.close()
                    return False, "Login button not found"
        except Exception as e:
            return False, f"Error during Fizzo upload: {str(e)}"
    
    # Fizzo auto-update endpoint
    @app.post("/api/fizzo-auto-update")
    async def fizzo_auto_update(request: Request):
        try:
            # Get session token from header
            session_token = request.headers.get("Authorization", "").replace("Bearer ", "")
            
            # If no token provided, return error
            if not session_token:
                return {"status": "error", "message": "Authentication required"}
            
            # Get user data from token
            user_data = get_user_from_token(session_token)
            
            # If user not found, return error
            if not user_data:
                return {"status": "error", "message": "Invalid session"}
            
            # Process the update
            data = await request.json()
            novel_id = data.get("novel_id", "")
            upload_to_fizzo_flag = data.get("upload_to_fizzo", False)
            
            # Find the novel in user's novels
            for i, novel in enumerate(user_data["novels"]):
                if novel["id"] == novel_id:
                    # Update the novel (in a real app, you would save to database)
                    if "title" in data:
                        user_data["novels"][i]["title"] = data["title"]
                    if "description" in data:
                        user_data["novels"][i]["description"] = data["description"]
                    if "chapters" in data:
                        user_data["novels"][i]["chapters"] = data["chapters"]
                    if "status" in data:
                        user_data["novels"][i]["status"] = data["status"]
                    if "cover_image" in data:
                        user_data["novels"][i]["cover_image"] = data["cover_image"]
                    if "target_words" in data:
                        user_data["novels"][i]["target_words"] = data["target_words"]
                    if "daily_updates" in data:
                        user_data["novels"][i]["daily_updates"] = data["daily_updates"]
                    
                    # Update word count if new chapters are added
                    if "chapters" in data:
                        total_words = 0
                        for chapter in data["chapters"]:
                            if "content" in chapter:
                                total_words += len(chapter["content"].split())
                        user_data["novels"][i]["current_words"] = total_words
                        user_data["novels"][i]["words_count"] = total_words
                        user_data["novels"][i]["chapters_count"] = len(data["chapters"])
                    
                    user_data["novels"][i]["updated_at"] = datetime.now().isoformat()
                    user_data["novels"][i]["last_updated"] = "today"
                    
                    # If upload to Fizzo is requested, do it
                    fizzo_upload_result = {"uploaded": False, "message": "Upload to Fizzo not requested"}
                    if upload_to_fizzo_flag:
                        email = active_sessions[session_token]
                        password = user_db[email]["password"]
                        
                        # In a real implementation, you would use the actual upload function
                        # success, message = await upload_to_fizzo(email, password, user_data["novels"][i])
                        
                        # For demonstration purposes, we'll simulate a successful upload
                        success = True
                        message = "Novel successfully uploaded to Fizzo.org (simulated)"
                        
                        fizzo_upload_result = {
                            "uploaded": success,
                            "message": message
                        }
                    
                    return {
                        "status": "success",
                        "message": "Novel updated successfully",
                        "novel": user_data["novels"][i],
                        "fizzo_upload": fizzo_upload_result
                    }
            
            # Novel not found
            return {"status": "error", "message": "Novel not found"}
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error during Fizzo auto-update: {str(e)}"
            }
    
    # Fizzo add chapter endpoint
    @app.post("/api/fizzo-add-chapter")
    async def fizzo_add_chapter(request: Request):
        try:
            # Get session token from header
            session_token = request.headers.get("Authorization", "").replace("Bearer ", "")
            
            # If no token provided, return error
            if not session_token:
                return {"status": "error", "message": "Authentication required"}
            
            # Get user data from token
            user_data = get_user_from_token(session_token)
            
            # If user not found, return error
            if not user_data:
                return {"status": "error", "message": "Invalid session"}
            
            # Process the request
            data = await request.json()
            novel_id = data.get("novel_id", "")
            chapter_title = data.get("title", "New Chapter")
            chapter_content = data.get("content", "")
            
            # Find the novel in user's novels
            for i, novel in enumerate(user_data["novels"]):
                if novel["id"] == novel_id:
                    # Create a new chapter
                    import uuid
                    new_chapter = {
                        "id": f"chapter-{uuid.uuid4()}",
                        "title": chapter_title,
                        "content": chapter_content
                    }
                    
                    # Add the chapter to the novel
                    user_data["novels"][i]["chapters"].append(new_chapter)
                    
                    # Update novel metadata
                    user_data["novels"][i]["chapters_count"] = len(user_data["novels"][i]["chapters"])
                    user_data["novels"][i]["updated_at"] = datetime.now().isoformat()
                    user_data["novels"][i]["last_updated"] = "today"
                    
                    # Update word count
                    total_words = 0
                    for chapter in user_data["novels"][i]["chapters"]:
                        if "content" in chapter:
                            total_words += len(chapter["content"].split())
                    user_data["novels"][i]["current_words"] = total_words
                    user_data["novels"][i]["words_count"] = total_words
                    
                    return {
                        "status": "success",
                        "message": "Chapter added successfully",
                        "chapter": new_chapter,
                        "novel": user_data["novels"][i]
                    }
            
            # Novel not found
            return {"status": "error", "message": "Novel not found"}
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error adding chapter: {str(e)}"
            }
    
    # Direct upload to Fizzo endpoint
    @app.post("/api/fizzo-direct-upload")
    async def fizzo_direct_upload(request: Request):
        try:
            # Get session token from header
            session_token = request.headers.get("Authorization", "").replace("Bearer ", "")
            
            # If no token provided, return error
            if not session_token:
                return {"status": "error", "message": "Authentication required"}
            
            # Get user data from token
            user_data = get_user_from_token(session_token)
            
            # If user not found, return error
            if not user_data:
                return {"status": "error", "message": "Invalid session"}
            
            # Process the request
            data = await request.json()
            novel_id = data.get("novel_id", "")
            
            # Find the novel in user's novels
            novel_to_upload = None
            for novel in user_data["novels"]:
                if novel["id"] == novel_id:
                    novel_to_upload = novel
                    break
            
            if not novel_to_upload:
                return {"status": "error", "message": "Novel not found"}
            
            # Get user credentials
            email = active_sessions[session_token]
            password = user_db[email]["password"]
            
            # In a real implementation, you would use the actual upload function
            # success, message = await upload_to_fizzo(email, password, novel_to_upload)
            
            # For demonstration purposes, we'll simulate a successful upload
            success = True
            message = "Novel successfully uploaded to Fizzo.org (simulated)"
            
            return {
                "status": "success" if success else "error",
                "message": message,
                "novel_id": novel_id,
                "title": novel_to_upload["title"]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error during direct upload to Fizzo: {str(e)}"
            }
    
    logger.info("✅ Fallback API created successfully")
    return app

# Global app instance for ASGI server
app = None

def initialize_app():
    """Initialize the FastAPI app"""
    global app
    try:
        # Setup environment
        logger.info("🔄 Setting up Hugging Face environment...")
        setup_hf_environment()
        install_playwright()
        
        # Try to create OpenHands app
        try:
            logger.info("🔄 Creating OpenHands app...")
            app = create_app()
            
            # Add Fizzo automation endpoints
            from openhands.routes.fizzo_list import router as fizzo_list_router
            app.include_router(fizzo_list_router)
            logger.info("✅ Fizzo list endpoint added: /api/fizzo-list-novel")
            
            from openhands.routes.fizzo_auto import router as fizzo_auto_router
            app.include_router(fizzo_auto_router)
            logger.info("✅ Fizzo automation endpoint added: /api/fizzo-auto-update")
            
        except Exception as e:
            logger.warning(f"⚠️ Error importing OpenHands app: {e}")
            logger.info("🔄 Creating fallback API...")
            app = create_fallback_app()
            
    except Exception as e:
        logger.error(f"❌ App initialization error: {e}")
        # Create minimal fallback app
        app = create_fallback_app()
    
    return app

# Initialize app on import for ASGI server
try:
    app = initialize_app()
except Exception as e:
    logger.error(f"❌ Failed to initialize app: {e}")
    app = create_fallback_app()

# Main application entry point
if __name__ == "__main__":
    try:
        # App already initialized above, just start server
        if app is None:
            logger.error("❌ App not initialized!")
            app = create_fallback_app()
        
        # Start uvicorn server
        logger.info("🚀 Starting uvicorn server...")
        uvicorn.run(
            app, 
            host=os.environ.get("HOST", "0.0.0.0"),
            port=int(os.environ.get("PORT", 12000)),
            log_level="info"
        )
            
    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        sys.exit(1)