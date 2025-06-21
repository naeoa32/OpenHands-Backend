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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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

if __name__ == "__main__":
    # Set custom browser path
    os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/tmp/playwright_browsers")
    
    # Install browsers
    if install_playwright_browsers():
        logger.info("✅ Playwright browsers installed successfully")
        sys.exit(0)
    else:
        logger.error("❌ Failed to install Playwright browsers")
        
        # Try direct download with curl (Linux only)
        try:
            logger.info("🔄 Trying direct download with curl...")
            browser_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/tmp/playwright_browsers")
            curl_cmd = f"curl -o /tmp/playwright-browsers.zip https://playwright.azureedge.net/builds/chromium/1169/chromium-linux.zip && mkdir -p {browser_path}/chromium-1169 && unzip -o /tmp/playwright-browsers.zip -d {browser_path}/chromium-1169 && chmod +x {browser_path}/chromium-1169/chrome-linux/chrome"
            result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Direct download successful")
                sys.exit(0)
            else:
                logger.warning(f"⚠️ Direct download failed: {result.stderr}")
                sys.exit(1)
        except Exception as e:
            logger.warning(f"⚠️ Error during direct download: {e}")
            sys.exit(1)