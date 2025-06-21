"""
Fizzo.org Novel Auto-Update Automation
Menggunakan Playwright untuk automation login dan upload chapter novel
"""
import asyncio
import logging
import re
from typing import Dict, Any, Optional, List
from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)

class FizzoAutomation:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.base_url = "https://fizzo.org"
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.start_browser()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close_browser()
        
    async def start_browser(self):
        """Start headless browser"""
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
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
            self.page = await self.browser.new_page()
            
            # Set user agent untuk mobile
            await self.page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15'
            })
            
            logger.info("✅ Browser started successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to start browser: {e}")
            raise
            
    async def close_browser(self):
        """Close browser"""
        try:
            if self.page:
                await self.page.close()
            if self.browser:
                await self.browser.close()
            logger.info("✅ Browser closed")
        except Exception as e:
            logger.error(f"⚠️ Error closing browser: {e}")
            
    async def login_to_fizzo(self, email: str, password: str) -> bool:
        """
        Login ke fizzo.org dengan email dan password
        Returns True jika berhasil login
        """
        try:
            logger.info("🌐 Navigating to fizzo.org...")
            await self.page.goto(self.base_url, wait_until='networkidle', timeout=30000)
            
            # Step 1: Klik hamburger menu
            logger.info("📱 Clicking hamburger menu...")
            hamburger_selector = 'button:has-text("☰"), [aria-label*="menu"], .menu-button'
            await self.page.wait_for_selector(hamburger_selector, timeout=10000)
            await self.page.click(hamburger_selector)
            await asyncio.sleep(1)
            
            # Step 2: Klik "Menulis Cerita"
            logger.info("✍️ Clicking 'Menulis Cerita'...")
            menulis_selector = 'text="Menulis Cerita"'
            await self.page.wait_for_selector(menulis_selector, timeout=10000)
            await self.page.click(menulis_selector)
            await asyncio.sleep(2)
            
            # Step 3: Klik "Lanjutkan dengan Email"
            logger.info("📧 Clicking 'Lanjutkan dengan Email'...")
            email_button_selector = 'text="Lanjutkan dengan Email"'
            await self.page.wait_for_selector(email_button_selector, timeout=10000)
            await self.page.click(email_button_selector)
            await asyncio.sleep(2)
            
            # Step 4: Fill email
            logger.info("📝 Filling email field...")
            email_input_selector = 'input[type="email"], input[placeholder*="email"], input[name*="email"]'
            await self.page.wait_for_selector(email_input_selector, timeout=10000)
            await self.page.fill(email_input_selector, email)
            
            # Step 5: Fill password
            logger.info("🔒 Filling password field...")
            password_input_selector = 'input[type="password"]'
            await self.page.wait_for_selector(password_input_selector, timeout=10000)
            await self.page.fill(password_input_selector, password)
            
            # Step 6: Klik "Lanjut"
            logger.info("🚀 Clicking 'Lanjut' button...")
            lanjut_button_selector = 'button:has-text("Lanjut"), input[type="submit"]'
            await self.page.click(lanjut_button_selector)
            
            # Step 7: Wait for dashboard
            logger.info("⏳ Waiting for dashboard...")
            await self.page.wait_for_url('**/mobile/**', timeout=15000)
            
            # Verify login success by checking for dashboard elements
            dashboard_indicators = [
                'text="New Chapter"',
                'text="Chapter"',
                'text="Story Info"',
                '.dashboard, .writer-dashboard'
            ]
            
            for indicator in dashboard_indicators:
                try:
                    await self.page.wait_for_selector(indicator, timeout=5000)
                    logger.info("✅ Login successful - Dashboard loaded")
                    return True
                except PlaywrightTimeoutError:
                    continue
                    
            logger.error("❌ Login failed - Dashboard not found")
            return False
            
        except Exception as e:
            logger.error(f"❌ Login failed: {e}")
            return False
            
    async def get_novel_list(self, email: str, password: str) -> List[Dict[str, Any]]:
        """
        Mendapatkan daftar novel yang dimiliki user setelah login ke fizzo.org
        Returns list of novels dengan judul dan id
        """
        try:
            # Login terlebih dahulu
            login_success = await self.login_to_fizzo(email, password)
            if not login_success:
                logger.error("❌ Tidak bisa mendapatkan daftar novel: Login gagal")
                return []
                
            logger.info("🔍 Mencari daftar novel user...")
            
            # Tunggu sampai halaman dashboard sepenuhnya dimuat
            await asyncio.sleep(2)
            
            # Cari elemen yang berisi daftar novel
            novel_selectors = [
                '.story-list .story-item',
                '.novel-list .novel-item',
                '.dashboard-stories .story',
                'a[href*="story/"]',
                'a[href*="novel/"]'
            ]
            
            novels = []
            
            # Coba berbagai selector untuk menemukan daftar novel
            for selector in novel_selectors:
                try:
                    # Cek apakah ada elemen yang cocok dengan selector
                    novel_elements = await self.page.query_selector_all(selector)
                    
                    if novel_elements and len(novel_elements) > 0:
                        logger.info(f"✅ Menemukan {len(novel_elements)} novel dengan selector: {selector}")
                        
                        # Ekstrak informasi dari setiap novel
                        for element in novel_elements:
                            try:
                                # Coba dapatkan judul novel
                                title_element = await element.query_selector('h2, h3, .title, .name')
                                title = await title_element.text_content() if title_element else None
                                
                                if not title:
                                    title = await element.text_content()
                                    
                                # Coba dapatkan ID novel dari href attribute
                                href = await element.get_attribute('href')
                                novel_id = None
                                
                                if href:
                                    # Ekstrak ID novel dari URL
                                    id_match = re.search(r'story/(\d+)|novel/(\d+)|id=(\d+)', href)
                                    if id_match:
                                        # Ambil grup yang tidak None
                                        novel_id = next((g for g in id_match.groups() if g is not None), None)
                                
                                if title and novel_id:
                                    # Tambahkan ke daftar novel
                                    novels.append({
                                        "title": title.strip(),
                                        "id": novel_id
                                    })
                                    logger.info(f"📚 Novel ditemukan: {title.strip()} (ID: {novel_id})")
                            except Exception as e:
                                logger.warning(f"⚠️ Gagal mengekstrak info novel: {e}")
                                continue
                                
                        # Jika berhasil menemukan novel, hentikan pencarian
                        if novels:
                            break
                except PlaywrightTimeoutError:
                    continue
                except Exception as e:
                    logger.warning(f"⚠️ Error saat mencari novel dengan selector {selector}: {e}")
                    continue
            
            if not novels:
                # Jika tidak menemukan novel dengan selector, coba cara alternatif
                logger.info("🔄 Mencoba cara alternatif untuk mendapatkan daftar novel...")
                
                try:
                    # Coba klik tombol "My Stories" atau sejenisnya jika ada
                    my_stories_selectors = [
                        'text="My Stories"',
                        'text="My Novels"',
                        'text="Cerita Saya"',
                        'text="Novel Saya"',
                        'a[href*="my-stories"]',
                        'a[href*="my-novels"]'
                    ]
                    
                    for selector in my_stories_selectors:
                        try:
                            my_stories_element = await self.page.query_selector(selector)
                            if my_stories_element:
                                logger.info(f"🖱️ Mengklik {selector}...")
                                await my_stories_element.click()
                                await asyncio.sleep(2)
                                
                                # Coba cari novel lagi setelah klik
                                novel_elements = await self.page.query_selector_all('a[href*="story/"], a[href*="novel/"]')
                                
                                if novel_elements and len(novel_elements) > 0:
                                    for element in novel_elements:
                                        try:
                                            title = await element.text_content()
                                            href = await element.get_attribute('href')
                                            
                                            if href:
                                                id_match = re.search(r'story/(\d+)|novel/(\d+)|id=(\d+)', href)
                                                if id_match:
                                                    novel_id = next((g for g in id_match.groups() if g is not None), None)
                                                    
                                                    if title and novel_id:
                                                        novels.append({
                                                            "title": title.strip(),
                                                            "id": novel_id
                                                        })
                                                        logger.info(f"📚 Novel ditemukan: {title.strip()} (ID: {novel_id})")
                                        except Exception:
                                            continue
                                
                                # Jika berhasil menemukan novel, hentikan pencarian
                                if novels:
                                    break
                        except PlaywrightTimeoutError:
                            continue
                        except Exception:
                            continue
                except Exception as e:
                    logger.warning(f"⚠️ Error saat mencoba cara alternatif: {e}")
            
            # Deduplikasi novel berdasarkan ID
            unique_novels = []
            seen_ids = set()
            
            for novel in novels:
                if novel["id"] not in seen_ids:
                    seen_ids.add(novel["id"])
                    unique_novels.append(novel)
            
            logger.info(f"✅ Berhasil mendapatkan {len(unique_novels)} novel")
            return unique_novels
            
        except Exception as e:
            logger.error(f"❌ Gagal mendapatkan daftar novel: {e}")
            return []
            
    async def create_new_chapter(self, chapter_title: str, chapter_content: str) -> Dict[str, Any]:
        """
        Buat chapter baru di fizzo.org
        """
        try:
            # Step 1: Klik "New Chapter"
            logger.info("📝 Clicking 'New Chapter' button...")
            new_chapter_selector = 'text="New Chapter", button:has-text("New Chapter")'
            await self.page.wait_for_selector(new_chapter_selector, timeout=10000)
            await self.page.click(new_chapter_selector)
            await asyncio.sleep(3)
            
            # Step 2: Fill chapter title
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
                    await self.page.wait_for_selector(selector, timeout=5000)
                    await self.page.fill(selector, chapter_title)
                    title_filled = True
                    break
                except PlaywrightTimeoutError:
                    continue
                    
            if not title_filled:
                logger.warning("⚠️ Could not find chapter title field")
            
            # Step 3: Fill chapter content
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
                    await self.page.wait_for_selector(selector, timeout=5000)
                    await self.page.fill(selector, chapter_content)
                    content_filled = True
                    break
                except PlaywrightTimeoutError:
                    continue
                    
            if not content_filled:
                raise Exception("Could not find chapter content field")
            
            # Step 4: Wait for auto-save
            logger.info("💾 Waiting for auto-save...")
            await asyncio.sleep(3)
            
            # Step 5: Publish chapter
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
                    await self.page.wait_for_selector(selector, timeout=5000)
                    await self.page.click(selector)
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
            
            success = False
            for indicator in success_indicators:
                try:
                    await self.page.wait_for_selector(indicator, timeout=3000)
                    success = True
                    break
                except PlaywrightTimeoutError:
                    continue
            
            result = {
                "success": True,
                "message": "Chapter created successfully",
                "chapter_title": chapter_title,
                "content_length": len(chapter_content),
                "published": published,
                "confirmed": success
            }
            
            logger.info("✅ Chapter creation completed")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to create chapter: {e}")
            return {
                "success": False,
                "error": str(e),
                "chapter_title": chapter_title
            }
            
    async def select_novel(self, novel_id: str) -> bool:
        """
        Memilih novel berdasarkan ID untuk menambahkan chapter baru
        Returns True jika berhasil memilih novel
        """
        try:
            logger.info(f"🔍 Mencoba memilih novel dengan ID: {novel_id}")
            
            # Coba berbagai cara untuk memilih novel
            
            # Cara 1: Cek apakah sudah berada di halaman novel yang tepat
            current_url = self.page.url
            if f"story/{novel_id}" in current_url or f"novel/{novel_id}" in current_url:
                logger.info("✅ Sudah berada di halaman novel yang tepat")
                return True
                
            # Cara 2: Cari link novel dengan ID yang sesuai dan klik
            novel_link_selectors = [
                f'a[href*="story/{novel_id}"]',
                f'a[href*="novel/{novel_id}"]',
                f'a[href*="id={novel_id}"]'
            ]
            
            for selector in novel_link_selectors:
                try:
                    novel_link = await self.page.query_selector(selector)
                    if novel_link:
                        logger.info(f"🖱️ Mengklik novel dengan ID: {novel_id}")
                        await novel_link.click()
                        await asyncio.sleep(2)
                        return True
                except Exception:
                    continue
            
            # Cara 3: Coba navigasi langsung ke URL novel
            try:
                logger.info(f"🌐 Mencoba navigasi langsung ke URL novel dengan ID: {novel_id}")
                await self.page.goto(f"{self.base_url}/mobile/story/{novel_id}", wait_until='networkidle', timeout=10000)
                await asyncio.sleep(2)
                
                # Verifikasi apakah berhasil navigasi ke halaman novel
                if f"story/{novel_id}" in self.page.url or f"novel/{novel_id}" in self.page.url:
                    logger.info("✅ Berhasil navigasi ke halaman novel")
                    return True
            except Exception as e:
                logger.warning(f"⚠️ Gagal navigasi langsung: {e}")
            
            logger.error(f"❌ Gagal memilih novel dengan ID: {novel_id}")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error saat memilih novel: {e}")
            return False
    
    async def auto_update_novel(self, email: str, password: str, chapter_title: str, chapter_content: str, novel_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Complete automation: Login + Create Chapter
        Jika novel_id diberikan, akan memilih novel tersebut sebelum membuat chapter baru
        """
        try:
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
            
            # Step 1: Login
            login_success = await self.login_to_fizzo(email, password)
            if not login_success:
                return {"success": False, "error": "Login failed"}
            
            # Step 2: Pilih novel jika ID diberikan
            if novel_id:
                logger.info(f"📚 Memilih novel dengan ID: {novel_id}")
                novel_selected = await self.select_novel(novel_id)
                if not novel_selected:
                    return {"success": False, "error": f"Gagal memilih novel dengan ID: {novel_id}"}
            
            # Step 3: Create chapter
            result = await self.create_new_chapter(chapter_title, chapter_content)
            
            logger.info("✅ Fizzo auto-update process completed")
            return result
            
        except Exception as e:
            logger.error(f"❌ Auto-update failed: {e}")
            return {"success": False, "error": str(e)}


async def fizzo_auto_update(email: str, password: str, chapter_title: str, chapter_content: str, novel_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Main function untuk auto-update novel ke fizzo.org
    Jika novel_id diberikan, akan memilih novel tersebut sebelum membuat chapter baru
    """
    async with FizzoAutomation() as automation:
        return await automation.auto_update_novel(email, password, chapter_title, chapter_content, novel_id)
        
async def fizzo_get_novel_list(email: str, password: str) -> List[Dict[str, Any]]:
    """
    Main function untuk mendapatkan daftar novel user di fizzo.org
    """
    async with FizzoAutomation() as automation:
        return await automation.get_novel_list(email, password)