#!/bin/bash
# 🚀 STANDALONE DEPLOY TO HUGGING FACE SPACES
# Script yang bisa di-download dan dijalankan langsung
# Download files dari GitHub dan deploy ke HF Spaces

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
    print_error "Usage: $0 <space-name> <hf-token> [github-repo] [branch]"
    echo "Example: $0 Minatoz997/Backend66 hf_xxxxxxxxxxxx"
    echo "Example: $0 Minatoz997/Backend66 hf_xxxxxxxxxxxx Minatoz997/Backendkugy main"
    echo ""
    echo "Available repos:"
    echo "  - Minatoz997/Backend (default)"
    echo "  - Minatoz997/Backendkugy"
    echo "  - Minatoz997/Huggingface-kugy"
    echo ""
    echo "Get your HF token from: https://huggingface.co/settings/tokens"
    exit 1
fi

SPACE_NAME="$1"
HF_TOKEN="$2"
GITHUB_REPO="${3:-Minatoz997/Backend}"  # Default to Backend repo
GITHUB_BRANCH="${4:-main}"              # Default to main branch
TEMP_DIR=$(mktemp -d)

# Essential files to download and deploy
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

print_status "🚀 Starting HF Spaces CLEAN deployment..."
echo "🌐 Target HF Space: $SPACE_NAME"
echo "📂 Temp directory: $TEMP_DIR"
echo "📥 Source: GitHub $GITHUB_REPO ($GITHUB_BRANCH)"
echo "=" * 60

# Check dependencies
print_status "Checking dependencies..."
if ! command -v git &> /dev/null; then
    print_error "Git is required but not installed"
    exit 1
fi

if ! command -v curl &> /dev/null; then
    print_error "Curl is required but not installed"
    exit 1
fi

print_success "Dependencies OK"

# Create working directory
cd "$TEMP_DIR"
mkdir -p source_files

# Download essential files from GitHub
print_status "Downloading files from GitHub..."
BASE_URL="https://raw.githubusercontent.com/$GITHUB_REPO/$GITHUB_BRANCH"

for file in "${ESSENTIAL_FILES[@]}"; do
    print_status "Downloading: $file"
    if curl -s -f "$BASE_URL/$file" -o "source_files/$file"; then
        print_success "Downloaded: $file"
    else
        print_warning "Could not download: $file (might not exist)"
    fi
done

# Download essential folders (as zip and extract)
print_status "Downloading repository archive..."
if curl -s -L "https://github.com/$GITHUB_REPO/archive/$GITHUB_BRANCH.zip" -o repo.zip; then
    if command -v unzip &> /dev/null; then
        unzip -q repo.zip
        REPO_DIR="OpenHands-Backend-$GITHUB_BRANCH"
        
        # Copy folders
        for folder in "${ESSENTIAL_FOLDERS[@]}"; do
            if [ -d "$REPO_DIR/$folder" ]; then
                cp -r "$REPO_DIR/$folder" "source_files/"
                print_success "Copied folder: $folder"
            else
                print_warning "Folder not found: $folder"
            fi
        done
    else
        print_error "Unzip is required to extract folders. Please install unzip."
        exit 1
    fi
else
    print_error "Failed to download repository archive"
    exit 1
fi

# Clone HF Space
print_status "Cloning HF Space: $SPACE_NAME"
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
print_status "🧹 Cleaning HF Space (removing all files except .git)..."
cd hf_space
find . -maxdepth 1 -not -name '.git' -not -name '.' -exec rm -rf {} \; 2>/dev/null || true
print_success "HF Space cleaned"

# Copy essential files
print_status "📋 Copying essential files..."
for file in "${ESSENTIAL_FILES[@]}"; do
    if [ -f "../source_files/$file" ]; then
        cp "../source_files/$file" .
        print_success "Copied: $file"
    else
        print_warning "File not found: $file"
    fi
done

# Copy essential folders
for folder in "${ESSENTIAL_FOLDERS[@]}"; do
    if [ -d "../source_files/$folder" ]; then
        cp -r "../source_files/$folder" .
        print_success "Copied folder: $folder"
    else
        print_warning "Folder not found: $folder"
    fi
done

# Create HF Spaces configuration
print_status "⚙️ Creating HF Spaces configuration..."
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
print_status "📤 Committing and pushing changes..."
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
💕 Ready for personal use!

Deployed via: https://github.com/$GITHUB_REPO"

    if git push origin main; then
        print_success "Successfully deployed to HF Spaces"
    else
        print_error "Failed to push to HF Space"
        exit 1
    fi
fi

echo ""
echo "=" * 60
print_success "🎉 DEPLOYMENT SUCCESSFUL!"
echo "🌐 Your space: https://huggingface.co/spaces/$SPACE_NAME"
echo "⏱️  Build will start automatically (5-10 minutes)"
echo ""
echo "🔧 NEXT STEPS:"
echo "1. Go to: https://huggingface.co/spaces/$SPACE_NAME/settings"
echo "2. Set environment variables:"
echo "   - LLM_API_KEY=your_openrouter_key"
echo "   - PERSONAL_ACCESS_TOKEN=your_password"
echo "3. Wait for build to complete"
echo "4. Test: https://$(echo $SPACE_NAME | tr '/' '-').hf.space/health"
echo ""
echo "💕 Enjoy your clean personal AI backend!"