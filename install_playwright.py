"""
Script untuk install Playwright browsers
Dijalankan saat startup untuk ensure browser tersedia
"""
import subprocess
import sys
import logging

logger = logging.getLogger(__name__)

def install_playwright_browsers():
    """Install Playwright browsers"""
    try:
        logger.info("🎭 Installing Playwright browsers...")
        
        # Install only Chromium (lightest option)
        result = subprocess.run([
            sys.executable, "-m", "playwright", "install", "chromium"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            logger.info("✅ Playwright Chromium installed successfully")
            return True
        else:
            logger.error(f"❌ Playwright install failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("❌ Playwright install timeout")
        return False
    except Exception as e:
        logger.error(f"❌ Playwright install error: {e}")
        return False

if __name__ == "__main__":
    install_playwright_browsers()