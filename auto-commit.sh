#!/bin/bash

# Auto-commit and push script for AI Voice Chat Assistant
# This script automatically commits and pushes changes to GitHub

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Auto-commit starting...${NC}"

# Navigate to project directory
cd "$(dirname "$0")"

# Check if there are changes
if [[ -z $(git status -s) ]]; then
    echo -e "${GREEN}✅ No changes to commit${NC}"
    exit 0
fi

# Show what changed
echo -e "${BLUE}📝 Files changed:${NC}"
git status -s

# Add all changes
git add .

# Generate commit message with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
COMMIT_MSG="Auto-save: $TIMESTAMP

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Commit changes
git commit -m "$COMMIT_MSG"

# Push to GitHub
echo -e "${BLUE}📤 Pushing to GitHub...${NC}"
git push origin main 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
else
    echo -e "${RED}❌ Failed to push. You may need to set up the remote first.${NC}"
    echo -e "${BLUE}Run: git push -u origin main${NC}"
fi
