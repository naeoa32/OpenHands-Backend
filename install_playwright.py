"""
Script untuk install Playwright browsers
Dijalankan saat startup untuk ensure browser tersedia
"""
import subprocess
import sys
import logging
import os
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

def install_playwright_browsers():
    """Install Playwright browsers with robust error handling"""
    try:
        logger.info("🎭 Installing Playwright browsers...")
        
        # Create a custom browser path in /tmp to avoid permission issues
        browser_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/tmp/playwright_browsers")
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = browser_path
        
        # Create the directory if it doesn't exist
        Path(browser_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Using custom browser path: {browser_path}")
        
        # Set HOME to a temporary directory to avoid .cache permission issues
        temp_home = tempfile.mkdtemp()
        os.environ["HOME"] = temp_home
        logger.info(f"🏠 Using temporary HOME directory: {temp_home}")
        
        # Try to install with --with-deps first (recommended)
        try:
            logger.info("🔄 Attempting installation with --with-deps...")
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