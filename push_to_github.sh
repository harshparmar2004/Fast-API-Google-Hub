#!/bin/bash
# Run this script from your local machine to push the code to your GitHub repo

# Ensure we are in the correct directory
cd "$(dirname "$0")"

echo "Initializing git repository..."
git init

echo "Adding files..."
git add .

echo "Committing files..."
git commit -m "Initial commit of FastAPI backend for Google Hub"

echo "Setting branch to main..."
git branch -M main

echo "Adding remote repository..."
git remote add origin https://github.com/harshparmar2004/Fast-API-Google-Hub.git

echo "Pushing to GitHub..."
echo "Note: You will be prompted for your GitHub credentials if not already authenticated."
git push -u origin main

echo "Done! You can now deploy this repository on Render."
