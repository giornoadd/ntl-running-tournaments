#!/usr/bin/env bash
set -e

# Change to root of the repo
cd "$(dirname "$0")/.."

echo "🚀 Preparing React Website Assets..."
python3 src/build_react_assets.py

echo "📦 Building React Application..."
cd webapp-react
npm install
npm run build
cd ..

echo "✅ Build complete! Assets deployed to html/ directory."
