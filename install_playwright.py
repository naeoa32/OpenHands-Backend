"""
Script untuk install Playwright browsers
Dijalankan saat startup untuk ensure browser tersedia
"""
import subprocess
import sys
import logging

logger = logging.getLogger(__name__)

def install_playwright_browsers():
    """Install Playwright browsers with robust error handling"""
    try:
        logger.info("🎭 Installing Playwright browsers...")
        
        # Try to install with --with-deps first (recommended)
        try:
            logger.info("🔄 Attempting installation with --with-deps...")
            result = subprocess.run(
                [sys.executable, "-m", "playwright", "install", "chromium", "--with-deps"],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.info("✅ Playwright browsers installed successfully with dependencies")
                return True
            else:
                logger.warning(f"⚠️ Installation with --with-deps failed: {result.stderr}")
        except Exception as e:
            logger.warning(f"⚠️ Error during installation with --with-deps: {e}")
        
        # Fallback: Try without --with-deps
        try:
            logger.info("🔄 Attempting installation without --with-deps...")
            result = subprocess.run(
                [sys.executable, "-m", "playwright", "install", "chromium"],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.info("✅ Playwright browsers installed successfully (without deps)")
                return True
            else:
                logger.error(f"❌ Installation failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"❌ Error during installation: {e}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("❌ Playwright install timeout")
        return False
    except Exception as e:
        logger.error(f"❌ Playwright install error: {e}")
        return False

if __name__ == "__main__":
    install_playwright_browsers()