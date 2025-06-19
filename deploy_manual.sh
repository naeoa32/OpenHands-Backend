#!/bin/bash
# 🚀 MANUAL DEPLOY TO HUGGING FACE SPACES
# Script untuk menghapus semua file lama dan upload file baru yang bersih

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}🔧 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if required arguments are provided
if [ $# -lt 2 ]; then
    print_error "Usage: $0 <space-name> <hf-token>"
    echo "Example: $0 username/my-openhands-backend hf_xxxxxxxxxxxx"
    echo ""
    echo "Get your HF token from: https://huggingface.co/settings/tokens"
    exit 1
fi

SPACE_NAME="$1"
HF_TOKEN="$2"
TEMP_DIR=$(mktemp -d)

# Essential files to deploy
ESSENTIAL_FILES=(
    "app.py"
    "requirements.txt"
    "Dockerfile"
    "README.md"
    "PERSONAL_TOKEN_GUIDE.md"
    "README_HF_DEPLOYMENT.md"
    ".env.example"
    ".gitignore"
)

ESSENTIAL_FOLDERS=(
    "openhands"
    "microagents"
)

cleanup() {
    print_status "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

print_status "Starting HF Spaces deployment..."
echo "📁 Source: $(pwd)"
echo "🌐 Target: $SPACE_NAME"
echo "📂 Temp dir: $TEMP_DIR"
echo "=" * 60

# Check if huggingface_hub is installed
print_status "Checking dependencies..."
if ! python -c "import huggingface_hub" 2>/dev/null; then
    print_warning "Installing huggingface_hub..."
    pip install huggingface_hub
fi
print_success "Dependencies OK"

# Clone HF Space
print_status "Cloning HF Space: $SPACE_NAME"
cd "$TEMP_DIR"
if ! git clone "https://oauth:$HF_TOKEN@huggingface.co/spaces/$SPACE_NAME" hf_space; then
    print_error "Failed to clone HF Space"
    print_warning "Make sure:"
    echo "   - Space exists and you have access"
    echo "   - HF token has write permissions"
    echo "   - Space name format: username/space-name"
    exit 1
fi
print_success "Cloned HF Space"

# Clean HF Space (remove all files except .git)
print_status "Cleaning HF Space (removing all files except .git)..."
cd hf_space
find . -maxdepth 1 -not -name '.git' -not -name '.' -exec rm -rf {} \; 2>/dev/null || true
print_success "HF Space cleaned"

# Copy essential files
print_status "Copying essential files..."
SOURCE_DIR="$(dirname "$(dirname "$TEMP_DIR")")/workspace/OpenHands-Backend"

for file in "${ESSENTIAL_FILES[@]}"; do
    if [ -f "$SOURCE_DIR/$file" ]; then
        cp "$SOURCE_DIR/$file" .
        print_success "Copied: $file"
    else
        print_warning "File not found: $file"
    fi
done

# Copy essential folders
for folder in "${ESSENTIAL_FOLDERS[@]}"; do
    if [ -d "$SOURCE_DIR/$folder" ]; then
        cp -r "$SOURCE_DIR/$folder" .
        print_success "Copied folder: $folder"
    else
        print_warning "Folder not found: $folder"
    fi
done

# Create HF Spaces configuration
print_status "Creating HF Spaces configuration..."
if [ -f "README.md" ]; then
    # Add HF Spaces header if not present
    if ! head -1 README.md | grep -q "^---"; then
        cat > temp_readme.md << 'EOF'
---
title: Personal OpenHands Backend
emoji: 💕
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

EOF
        cat README.md >> temp_readme.md
        mv temp_readme.md README.md
        print_success "Added HF Spaces header to README.md"
    fi
fi

# Configure git
git config user.name "OpenHands Deploy Bot"
git config user.email "deploy@openhands.dev"

# Commit and push
print_status "Committing and pushing changes..."
git add -A

if [ -z "$(git status --porcelain)" ]; then
    print_warning "No changes to commit"
else
    git commit -m "🚀 CLEAN DEPLOY: Remove duplicates, deploy essential files only

✅ Files deployed:
- app.py (all-in-one backend)
- requirements.txt (minimal deps)
- Dockerfile (HF optimized)
- Complete documentation
- openhands/ (agents)
- microagents/ (templates)

🗑️ Removed all duplicate files
💕 Ready for personal use!"

    if git push origin main; then
        print_success "Successfully deployed to HF Spaces"
    else
        print_error "Failed to push to HF Space"
        exit 1
    fi
fi

echo ""
echo "=" * 60
print_success "DEPLOYMENT SUCCESSFUL!"
echo "🌐 Your space: https://huggingface.co/spaces/$SPACE_NAME"
echo "⏱️  Build will start automatically (5-10 minutes)"
echo "🔧 Don't forget to set environment variables in HF Spaces settings:"
echo "   - LLM_API_KEY=your_openrouter_key"
echo "   - PERSONAL_ACCESS_TOKEN=your_password"
echo "💕 Enjoy your personal AI backend!"