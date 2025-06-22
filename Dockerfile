# Dockerfile lengkap untuk Hugging Face Spaces dengan Playwright
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright_browsers
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0
ENV DEBIAN_FRONTEND=noninteractive

# Update system dan install dependencies yang diperlukan Playwright
RUN apt-get update && apt-get install -y \
    # Basic utilities
    wget \
    curl \
    gnupg \
    ca-certificates \
    apt-transport-https \
    software-properties-common \
    # Fonts
    fonts-liberation \
    fonts-noto-color-emoji \
    fonts-noto-cjk \
    # Audio
    libasound2 \
    libpulse0 \
    # Graphics dan rendering
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo-gobject2 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    # X11 dan display
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcb-dri3-0 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxkbcommon0 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    # Browser dependencies
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libxshmfence1 \
    # System utilities
    xdg-utils \
    # Additional dependencies dari error log
    libglib2.0-0 \
    libgconf-2-4 \
    libxfont2 \
    libxinerama1 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    ca-certificates \
    fonts-liberation \
    libappindicator1 \
    libnss3 \
    lsb-release \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create directory untuk Playwright browsers
RUN mkdir -p /tmp/playwright_browsers && chmod 777 /tmp/playwright_browsers

# Copy requirements terlebih dahulu untuk better Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers dengan semua dependencies
RUN python -m playwright install chromium
RUN python -m playwright install-deps chromium

# Verify Playwright installation
RUN python -c "from playwright.sync_api import sync_playwright; print('Playwright installed successfully')"

# Copy semua file aplikasi
COPY . .

# Set permissions
RUN chmod -R 755 /app

# Expose port untuk Hugging Face Spaces
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run aplikasi
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]