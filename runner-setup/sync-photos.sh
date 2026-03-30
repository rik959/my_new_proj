#!/bin/bash
echo "============================================"
echo " 📸 Syncing photos to deployment volume"
echo "============================================"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PHOTOS_SRC="$SCRIPT_DIR/../photos"
PHOTOS_DST="$HOME/love-pipeline-photos"

mkdir -p "$PHOTOS_DST"

echo "Source: $PHOTOS_SRC"
echo "Dest:   $PHOTOS_DST"
echo ""

# Copy folder structure + new photos (don't overwrite existing)
cp -rn "$PHOTOS_SRC"/* "$PHOTOS_DST/" 2>/dev/null

echo "✅ Photos synced!"
echo "   Container mounts $PHOTOS_DST as the photos directory."
echo "   Drop new photos in the date folders and they'll appear in the app."
