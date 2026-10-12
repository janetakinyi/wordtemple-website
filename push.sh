#!/bin/bash

# Quick push script for Word Temple website
# Usage: ./push.sh "Your commit message"

cd ~/wordtemple-website

# Default message if none provided
MESSAGE="${1:-Update website content}"

echo "========================================="
echo "🚀 Pushing changes to GitHub..."
echo "========================================="
echo ""

# Check if there are changes
if [[ -z $(git status --porcelain) ]]; then
    echo "✅ No changes to commit"
    exit 0
fi

# Show what's changed
echo "📝 Changes detected:"
git status --short
echo ""

# Add all changes
echo "📦 Adding files..."
git add .

# Commit with message
echo "💾 Committing..."
git commit -m "$MESSAGE"

# Push to GitHub
echo "⬆️ Pushing to GitHub..."
git push origin main

echo ""
echo "========================================="
echo "✅ Successfully pushed to GitHub!"
echo "🌐 Live site: https://www.wordtemple.org"
echo "⏳ Render will redeploy in 2-3 minutes"
echo "========================================="
