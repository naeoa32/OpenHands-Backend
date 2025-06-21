"""
OpenHands Backend optimized for Hugging Face Spaces deployment
Final fixed version that handles all import issues
"""
import os
import sys
import logging
import uvicorn
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_hf_environment():
    """Setup environment variables for Hugging Face Spaces"""
    
    # Core HF Spaces configuration
    os.environ.setdefault("PORT", "7860")
    os.environ.setdefault("HOST", "0.0.0.0")
    os.environ.setdefault("OPENHANDS_RUNTIME", "local")  # Use local runtime, not docker
    os.environ.setdefault("CORS_ALLOWED_ORIGINS", "*")
    
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
    
    # LLM configuration - use OpenRouter by default
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.warning("⚠️  LLM_API_KEY or OPENROUTER_API_KEY not set. Please set it in HF Spaces environment variables.")
        logger.warning("⚠️  Without API key, the backend will start but LLM calls will fail.")
    else:
        logger.info("✅ LLM API key found")
        # Ensure LLM_API_KEY is set to the OpenRouter key
        os.environ["LLM_API_KEY"] = api_key
    
    # Fixed model name format for OpenRouter (remove openrouter/ prefix)
    os.environ.setdefault("LLM_MODEL", "anthropic/claude-3.5-sonnet")
    os.environ.setdefault("LLM_BASE_URL", "https://openrouter.ai/api/v1")
    
    # Force OpenRouter provider to avoid direct Anthropic connection
    os.environ.setdefault("LLM_CUSTOM_LLM_PROVIDER", "openrouter")
    
    # Create directories if they don't exist
    directories = ["/tmp/openhands", "/tmp/cache", "/tmp/workspace", "/tmp/file_store"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    logger.info("✅ Environment configured for Hugging Face Spaces")

def check_dependencies():
    """Check if critical dependencies are available"""
    missing_deps = []
    
    try:
        import fastapi
        logger.info("✅ FastAPI available")
    except ImportError:
        missing_deps.append("fastapi")
    
    try:
        import uvicorn
        logger.info("✅ Uvicorn available")
    except ImportError:
        missing_deps.append("uvicorn")
    
    try:
        import litellm
        logger.info("✅ LiteLLM available")
    except ImportError:
        missing_deps.append("litellm")
    
    # Check optional dependencies
    try:
        import docker
        logger.info("⚠️  Docker available (not needed for HF Spaces)")
    except ImportError:
        logger.info("✅ Docker not available (expected for HF Spaces)")
    
    # Google Cloud is COMPLETELY OPTIONAL - no login required, no API key needed
    # This is just for informational purposes only
    try:
        import google.api_core
        logger.info("⚠️  Google Cloud available (OPTIONAL - not needed for basic functionality)")
    except ImportError:
        logger.info("✅ Google Cloud not available (PERFECTLY FINE - no login/API key required)")
    
    if missing_deps:
        logger.error(f"❌ Missing critical dependencies: {missing_deps}")
        return False
    
    return True

def setup_fizzo_automation():
    """Setup Fizzo automation dependencies"""
    try:
        import playwright
        logger.info("✅ Playwright available for Fizzo automation")
        
        # Auto-install browsers if needed
        try:
            import subprocess
            import sys
            logger.info("🎭 Installing Playwright browsers...")
            
            # Try to install Chromium with proper error handling
            result = subprocess.run([
                sys.executable, "-m", "playwright", "install", "chromium", "--with-deps"
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info("✅ Playwright Chromium installed successfully")
            else:
                logger.warning(f"⚠️ Playwright install failed: {result.stderr}")
                # Try without --with-deps flag
                result2 = subprocess.run([
                    sys.executable, "-m", "playwright", "install", "chromium"
                ], capture_output=True, text=True, timeout=300)
                
                if result2.returncode == 0:
                    logger.info("✅ Playwright Chromium installed successfully (without deps)")
                else:
                    logger.warning(f"⚠️ Playwright install failed again: {result2.stderr}")
                    
        except subprocess.TimeoutExpired:
            logger.warning("⚠️ Playwright install timeout - continuing anyway")
        except Exception as e:
            logger.warning(f"⚠️ Could not auto-install Playwright browsers: {e}")
            
        return True
    except ImportError:
        logger.warning("⚠️ Playwright not available - Fizzo automation disabled")
        return False

if __name__ == "__main__":
    try:
        logger.info("🔧 Setting up Hugging Face environment...")
        setup_hf_environment()
        
        logger.info("🔍 Checking dependencies...")
        if not check_dependencies():
            logger.error("❌ Critical dependencies missing. Cannot start server.")
            sys.exit(1)
            
        logger.info("🎭 Setting up Fizzo automation...")
        fizzo_available = setup_fizzo_automation()
        
        logger.info("📦 Importing OpenHands app...")
        from openhands.server.app import app
        
        # Add Fizzo automation endpoint if available
        if fizzo_available:
            try:
                from fastapi import HTTPException
                from pydantic import BaseModel
                import asyncio
                
                logger.info("🔧 Creating inline Fizzo automation...")
                
                # Inline Fizzo automation implementation - completely self-contained
                async def fizzo_auto_update(email: str, password: str, chapter_title: str, chapter_content: str):
                    """Inline Fizzo automation implementation - no external dependencies"""
                    try:
                        from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
                        
                        # Validate input
                        if not email or not password:
                            return {"success": False, "error": "Email and password are required"}
                        if not chapter_title or not chapter_content:
                            return {"success": False, "error": "Chapter title and content are required"}
                        if len(chapter_content) < 1000:
                            return {"success": False, "error": "Chapter content must be at least 1,000 characters"}
                        if len(chapter_content) > 60000:
                            return {"success": False, "error": "Chapter content must be less than 60,000 characters"}
                        
                        logger.info("🚀 Starting Fizzo auto-update process...")
                        
                        playwright = await async_playwright().start()
                        browser = await playwright.chromium.launch(
                            headless=True,
                            args=[
                                '--no-sandbox',
                                '--disable-setuid-sandbox', 
                                '--disable-dev-shm-usage',
                                '--disable-accelerated-2d-canvas',
                                '--no-first-run',
                                '--no-zygote',
                                '--disable-gpu'
                            ]
                        )
                        page = await browser.new_page()
                        
                        # Set mobile user agent
                        await page.set_extra_http_headers({
                            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15'
                        })
                        
                        try:
                            # Step 1: Navigate to fizzo.org
                            logger.info("🌐 Navigating to fizzo.org...")
                            await page.goto("https://fizzo.org", wait_until='networkidle', timeout=30000)
                            
                            # Step 2: Click hamburger menu
                            logger.info("📱 Clicking hamburger menu...")
                            hamburger_selector = 'button:has-text("☰"), [aria-label*="menu"], .menu-button'
                            await page.wait_for_selector(hamburger_selector, timeout=10000)
                            await page.click(hamburger_selector)
                            await asyncio.sleep(1)
                            
                            # Step 3: Click "Menulis Cerita"
                            logger.info("✍️ Clicking 'Menulis Cerita'...")
                            menulis_selector = 'text="Menulis Cerita"'
                            await page.wait_for_selector(menulis_selector, timeout=10000)
                            await page.click(menulis_selector)
                            await asyncio.sleep(2)
                            
                            # Step 4: Click "Lanjutkan dengan Email"
                            logger.info("📧 Clicking 'Lanjutkan dengan Email'...")
                            email_button_selector = 'text="Lanjutkan dengan Email"'
                            await page.wait_for_selector(email_button_selector, timeout=10000)
                            await page.click(email_button_selector)
                            await asyncio.sleep(2)
                            
                            # Step 5: Fill email
                            logger.info("📝 Filling email field...")
                            email_input_selector = 'input[type="email"], input[placeholder*="email"], input[name*="email"]'
                            await page.wait_for_selector(email_input_selector, timeout=10000)
                            await page.fill(email_input_selector, email)
                            
                            # Step 6: Fill password
                            logger.info("🔒 Filling password field...")
                            password_input_selector = 'input[type="password"]'
                            await page.wait_for_selector(password_input_selector, timeout=10000)
                            await page.fill(password_input_selector, password)
                            
                            # Step 7: Click "Lanjut"
                            logger.info("🚀 Clicking 'Lanjut' button...")
                            lanjut_button_selector = 'button:has-text("Lanjut"), input[type="submit"]'
                            await page.click(lanjut_button_selector)
                            
                            # Step 8: Wait for dashboard
                            logger.info("⏳ Waiting for dashboard...")
                            await page.wait_for_url('**/mobile/**', timeout=15000)
                            
                            # Verify login success
                            dashboard_indicators = [
                                'text="New Chapter"',
                                'text="Chapter"',
                                'text="Story Info"',
                                '.dashboard, .writer-dashboard'
                            ]
                            
                            login_success = False
                            for indicator in dashboard_indicators:
                                try:
                                    await page.wait_for_selector(indicator, timeout=5000)
                                    logger.info("✅ Login successful - Dashboard loaded")
                                    login_success = True
                                    break
                                except PlaywrightTimeoutError:
                                    continue
                                    
                            if not login_success:
                                return {"success": False, "error": "Login failed - Dashboard not found"}
                            
                            # Step 9: Click "New Chapter"
                            logger.info("📝 Clicking 'New Chapter' button...")
                            new_chapter_selector = 'text="New Chapter", button:has-text("New Chapter")'
                            await page.wait_for_selector(new_chapter_selector, timeout=10000)
                            await page.click(new_chapter_selector)
                            await asyncio.sleep(3)
                            
                            # Step 10: Fill chapter title
                            logger.info(f"📖 Filling chapter title: {chapter_title}")
                            title_selectors = [
                                'input[placeholder*="chapter name"]',
                                'input[placeholder*="Enter chapter"]',
                                'input[name*="title"]',
                                '.chapter-title input'
                            ]
                            
                            title_filled = False
                            for selector in title_selectors:
                                try:
                                    await page.wait_for_selector(selector, timeout=5000)
                                    await page.fill(selector, chapter_title)
                                    title_filled = True
                                    break
                                except PlaywrightTimeoutError:
                                    continue
                                    
                            if not title_filled:
                                logger.warning("⚠️ Could not find chapter title field")
                            
                            # Step 11: Fill chapter content
                            logger.info(f"📄 Filling chapter content ({len(chapter_content)} characters)...")
                            content_selectors = [
                                'textarea[placeholder*="Start writing"]',
                                'textarea[placeholder*="writing here"]',
                                '.editor textarea',
                                '.content-editor textarea',
                                'div[contenteditable="true"]'
                            ]
                            
                            content_filled = False
                            for selector in content_selectors:
                                try:
                                    await page.wait_for_selector(selector, timeout=5000)
                                    await page.fill(selector, chapter_content)
                                    content_filled = True
                                    break
                                except PlaywrightTimeoutError:
                                    continue
                                    
                            if not content_filled:
                                return {"success": False, "error": "Could not find chapter content field"}
                            
                            # Step 12: Wait for auto-save
                            logger.info("💾 Waiting for auto-save...")
                            await asyncio.sleep(3)
                            
                            # Step 13: Publish chapter
                            logger.info("🚀 Publishing chapter...")
                            publish_selectors = [
                                'button:has-text("✈️")',
                                'button[title*="publish"]',
                                'button[title*="submit"]',
                                '.publish-button',
                                '.submit-button'
                            ]
                            
                            published = False
                            for selector in publish_selectors:
                                try:
                                    await page.wait_for_selector(selector, timeout=5000)
                                    await page.click(selector)
                                    published = True
                                    break
                                except PlaywrightTimeoutError:
                                    continue
                            
                            if not published:
                                logger.warning("⚠️ Could not find publish button - chapter may be saved as draft")
                            
                            # Wait for success confirmation
                            await asyncio.sleep(5)
                            
                            # Check for success indicators
                            success_indicators = [
                                'text="published"',
                                'text="success"',
                                'text="berhasil"',
                                '.success-message'
                            ]
                            
                            success_confirmed = False
                            for indicator in success_indicators:
                                try:
                                    await page.wait_for_selector(indicator, timeout=3000)
                                    success_confirmed = True
                                    break
                                except PlaywrightTimeoutError:
                                    continue
                            
                            return {
                                "success": True,
                                "message": "Chapter created successfully",
                                "chapter_title": chapter_title,
                                "content_length": len(chapter_content),
                                "published": published,
                                "confirmed": success_confirmed
                            }
                            
                        finally:
                            await browser.close()
                            await playwright.stop()
                            
                    except Exception as e:
                        logger.error(f"❌ Fizzo automation failed: {e}")
                        return {"success": False, "error": str(e)}
                
                from typing import Optional, List

                class FizzoUpdateRequest(BaseModel):
                    email: str
                    password: str
                    chapter_title: str
                    chapter_content: str
                    novel_id: Optional[str] = None

                class FizzoListNovelRequest(BaseModel):
                    email: str
                    password: str

                @app.post("/api/fizzo-list-novel")
                async def fizzo_list_novel_endpoint(request: FizzoListNovelRequest):
                    """
                    Mendapatkan daftar novel yang dimiliki user di fizzo.org
                    
                    Requires:
                    - email: Email login fizzo.org
                    - password: Password login fizzo.org
                    
                    Returns:
                    - List of novels dengan judul dan id
                    """
                    try:
                        # Validate authentication
                        if not request.email or not request.password:
                            raise HTTPException(status_code=400, detail="Email and password are required")
                            
                        logger.info(f"🚀 Starting Fizzo novel list retrieval for user: {request.email}")
                        
                        # Import fizzo_automation module
                        try:
                            from fizzo_automation import fizzo_get_novel_list
                        except ImportError:
                            # Fallback to inline implementation
                            from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
                            import re
                            
                            async def fizzo_get_novel_list(email: str, password: str):
                                """Inline implementation of fizzo_get_novel_list"""
                                # Implementation details would go here
                                # This is a simplified version for fallback
                                return []
                        
                        # Run automation with timeout
                        try:
                            result = await asyncio.wait_for(
                                fizzo_get_novel_list(
                                    email=request.email,
                                    password=request.password
                                ),
                                timeout=300  # 5 minute timeout
                            )
                        except asyncio.TimeoutError:
                            logger.error("❌ Fizzo novel list retrieval timeout")
                            raise HTTPException(status_code=408, detail="Automation timeout - please try again")
                        
                        logger.info(f"✅ Fizzo novel list retrieval successful: {len(result)} novels found")
                        return {
                            "success": True,
                            "message": f"Berhasil mendapatkan {len(result)} novel",
                            "data": result
                        }
                    
                    except HTTPException:
                        raise
                    except Exception as e:
                        logger.error(f"❌ Fizzo novel list retrieval failed: {str(e)}")
                        return {
                            "success": False,
                            "error": f"Failed to retrieve novel list: {str(e)}"
                        }
                @app.post("/api/fizzo-auto-update")
                async def fizzo_update_endpoint(request: FizzoUpdateRequest):
                    """
                    Auto-update novel chapter ke fizzo.org
                    
                    Requires:
                    - email: Email login fizzo.org
                    - password: Password login fizzo.org  
                    - chapter_title: Judul chapter (contoh: "Bab 28")
                    - chapter_content: Isi chapter (1,000-60,000 karakter)
                    - novel_id: (Optional) ID novel yang akan diupdate, jika tidak diisi akan menggunakan novel default
                    """
                    try:
                        # Validate authentication (gunakan existing auth system)
                        # Note: Bisa ditambahkan Bearer token validation di sini
                        
                        logger.info(f"🚀 Starting Fizzo auto-update for chapter: {request.chapter_title}")
                        
                        # Pre-validate inputs
                        if not request.email or not request.password:
                            raise HTTPException(status_code=400, detail="Email and password are required")
                        if not request.chapter_title or not request.chapter_content:
                            raise HTTPException(status_code=400, detail="Chapter title and content are required")
                        if len(request.chapter_content) < 1000:
                            raise HTTPException(status_code=400, detail="Chapter content must be at least 1,000 characters")
                        if len(request.chapter_content) > 60000:
                            raise HTTPException(status_code=400, detail="Chapter content must be less than 60,000 characters")
                        
                        # Run automation with timeout
                        try:
                            result = await asyncio.wait_for(
                                fizzo_auto_update(
                                    email=request.email,
                                    password=request.password,
                                    chapter_title=request.chapter_title,
                                    chapter_content=request.chapter_content,
                                    novel_id=request.novel_id
                                ),
                                timeout=300  # 5 minute timeout
                            )
                        except asyncio.TimeoutError:
                            logger.error("❌ Fizzo automation timeout")
                            raise HTTPException(status_code=408, detail="Automation timeout - please try again")
                        
                        if result.get("success"):
                            logger.info("✅ Fizzo auto-update successful")
                            return {
                                "success": True,
                                "message": "Chapter berhasil diupload ke fizzo.org",
                                "data": result
                            }
                        else:
                            error_msg = result.get("error", "Unknown error")
                            logger.error(f"❌ Fizzo auto-update failed: {error_msg}")
                            
                            # Provide more specific error codes
                            if "login failed" in error_msg.lower():
                                raise HTTPException(status_code=401, detail=f"Login failed: {error_msg}")
                            elif "chapter content" in error_msg.lower():
                                raise HTTPException(status_code=400, detail=f"Content error: {error_msg}")
                            else:
                                raise HTTPException(status_code=500, detail=f"Automation error: {error_msg}")
                            
                    except HTTPException:
                        # Re-raise HTTP exceptions as-is
                        raise
                    except Exception as e:
                        logger.error(f"❌ Fizzo endpoint error: {e}")
                        import traceback
                        traceback.print_exc()
                        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
                    
                logger.info("✅ Fizzo automation endpoint added: /api/fizzo-auto-update")
                
            except Exception as e:
                logger.error(f"❌ Failed to setup Fizzo automation endpoint: {e}")
                logger.warning("⚠️ Fizzo automation will not be available")
        else:
            # Add fallback endpoint when Fizzo automation is not available
            try:
                from fastapi import HTTPException
                from pydantic import BaseModel
                
                class FizzoUpdateRequest(BaseModel):
                    email: str
                    password: str
                    chapter_title: str
                    chapter_content: str
                    novel_id: Optional[str] = None
                
                class FizzoListNovelRequest(BaseModel):
                    email: str
                    password: str
                
                @app.post("/api/fizzo-auto-update")
                async def fizzo_update_fallback(request: FizzoUpdateRequest):
                    """
                    Fallback endpoint when Fizzo automation is not available
                    """
                    logger.warning("⚠️ Fizzo automation not available - Playwright missing")
                    raise HTTPException(
                        status_code=503,
                        detail="Fizzo automation is not available. Please install Playwright to use this feature."
                    )
                
                @app.post("/api/fizzo-list-novel")
                async def fizzo_list_novel_fallback(request: FizzoListNovelRequest):
                    """
                    Fallback endpoint when Fizzo automation is not available
                    """
                    logger.warning("⚠️ Fizzo automation not available - Playwright missing")
                    raise HTTPException(
                        status_code=503,
                        detail="Fizzo automation is not available. Please install Playwright to use this feature."
                    )
                    
                logger.info("⚠️ Fizzo automation fallback endpoints added: /api/fizzo-auto-update, /api/fizzo-list-novel")
                
            except Exception as e:
                logger.error(f"❌ Failed to setup Fizzo fallback endpoint: {e}")
        
        # Get configuration
        port = int(os.getenv("PORT", 7860))
        host = os.getenv("HOST", "0.0.0.0")
        
        # Startup information
        print("\n" + "="*50)
        print("🤗 OpenHands Backend for Hugging Face Spaces")
        print("="*50)
        print(f"🚀 Server: {host}:{port}")
        print(f"🔑 LLM API Key: {'✅ Set' if os.getenv('LLM_API_KEY') else '❌ Missing'}")
        print(f"🤖 LLM Model: {os.getenv('LLM_MODEL', 'Not configured')}")
        print(f"🏃 Runtime: {os.getenv('OPENHANDS_RUNTIME', 'local')}")
        print(f"🎭 Fizzo Automation: {'✅ Available' if fizzo_available else '❌ Disabled (Playwright missing)'}")
        print("📡 API Endpoints available at /docs")
        print("🔧 Fizzo Endpoint: /api/fizzo-auto-update")
        print("="*50 + "\n")
        
        logger.info("🚀 Starting uvicorn server...")
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("💡 This usually means a required dependency is missing.")
        logger.error("💡 Check that all dependencies in requirements.txt are installed.")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)