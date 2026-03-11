#!/usr/bin/env bash
set -e

# Change to root of the repo
cd "$(dirname "$0")/.."

echo "📊 Regenerating data.js from latest CSV data..."
python3 src/build_website_data.py

echo "🚀 Preparing React Website Assets..."
python3 src/build_react_assets.py

echo "📦 Building React Application..."
cd webapp-react
npm install
npm run build
cd ..

echo "🏠 Generating landing page at docs/index.html..."
python3 src/generate_landing_page.py

echo "✅ Build complete! Assets deployed to docs/ directory."
