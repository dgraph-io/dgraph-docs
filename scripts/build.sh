#!/bin/bash

# Hugo Multi-Version Documentation Build Script
# This script builds documentation from multiple branches
# Usage: ./build.sh [baseURL]
# Example: ./build.sh http://localhost:1313
#          ./build.sh https://docs.dgraph.io

set -e

# Configuration
OUTPUT_DIR="public"
TEMP_DIR=".hugo-versions-temp"
VERSION_BRANCHES=("release/v25.0" "release/v24.1")  # Add your version branches here
# The first branch in the list builds to root public/
ROOT_BRANCH=${VERSION_BRANCHES[0]}
# Get current working branch
WORKING_BRANCH=$(git branch --show-current)

# Parse baseURL parameter (default: http://localhost:1313)
BASE_URL_PARAM=${1:-"http://localhost:1313"}

DGRAPH_ENDPOINT=${DGRAPH_ENDPOINT:-"https://play.dgraph.io/query?latency=true"}
HUGO_TITLE="Dgraph documentation"
# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting multi-version Hugo build...${NC}"

# Clean up previous builds
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# Build all versions in a loop
for branch in "${VERSION_BRANCHES[@]}"; do
    # Determine version: if branch doesn't have version prefix, use the branch name
    if [[ "$branch" =~ ^release/ ]]; then
        VERSION=$(echo "$branch" | sed 's|release/||')
    else
        VERSION=$branch
    fi
    
    echo -e "${GREEN}Building version $VERSION from branch $branch...${NC}"
    
    # Determine output directory and baseURL: first branch goes to public, others to public/VERSION
    if [ "$branch" = "$ROOT_BRANCH" ]; then
        BUILD_OUTPUT_DIR="$OUTPUT_DIR"
        BASE_URL="$BASE_URL_PARAM/"
    else
        BUILD_OUTPUT_DIR="$OUTPUT_DIR/$VERSION"
        BASE_URL="$BASE_URL_PARAM/$VERSION/"
    fi
    
    # If this is the root branch AND we're currently on it, use current directory; otherwise use worktree
    if [ "$branch" = "$ROOT_BRANCH" ] && [ "$branch" = "$WORKING_BRANCH" ]; then
        echo "Building from current branch (root branch), using current directory..."
        hugo --minify -d "$BUILD_OUTPUT_DIR" --baseURL "$BASE_URL"
    else
        # Create temporary directory for this version
        BRANCH_DIR="$TEMP_DIR/$VERSION"
        
        # Remove worktree if it already exists
        if [ -d "$BRANCH_DIR" ]; then
            git worktree remove "$BRANCH_DIR" --force 2>/dev/null || rm -rf "$BRANCH_DIR"
        fi
        
        # Clone the specific branch into temp directory
        git fetch origin "$branch"
        git worktree add "$BRANCH_DIR" "$branch"
        
        # Build Hugo site for this version
        pushd "$BRANCH_DIR"
        hugo --minify -d "../../$BUILD_OUTPUT_DIR" --baseURL "$BASE_URL"
        popd
        
        # Clean up worktree
        git worktree remove "$BRANCH_DIR"
    fi
    
    echo -e "${GREEN}Version $VERSION built successfully${NC}"
done

# Clean up temp directory
rm -rf "$TEMP_DIR"

# Create versions.json for the version selector
echo -e "${BLUE}Creating versions.json...${NC}"
cat > "$OUTPUT_DIR/versions.json" << EOF
{
  "versions": [
EOF

# Add version entries
FIRST=true
for branch in "${VERSION_BRANCHES[@]}"; do
    # Determine version: if branch doesn't have version prefix, use "main"
    if [[ "$branch" =~ ^release/ ]]; then
        VERSION=$(echo "$branch" | sed 's|release/||')
        VERSION_TITLE="$VERSION"
        # First entry always has URL "/" regardless of version
        if [ "$FIRST" = true ]; then
            VERSION_URL="/"
        else
            VERSION_URL="/$VERSION/"
        fi
    else
        VERSION="main"
        VERSION_TITLE="Latest (main)"
        VERSION_URL="/"
    fi
    
    if [ "$FIRST" = true ]; then
        FIRST=false
        cat >> "$OUTPUT_DIR/versions.json" << EOF
    {
      "version": "$VERSION",
      "title": "$VERSION_TITLE",
      "url": "$VERSION_URL"
    }
EOF
    else
        cat >> "$OUTPUT_DIR/versions.json" << EOF
,
    {
      "version": "$VERSION",
      "title": "$VERSION_TITLE",
      "url": "$VERSION_URL"
    }
EOF
    fi
done

cat >> "$OUTPUT_DIR/versions.json" << EOF

  ]
}
EOF

echo -e "${GREEN}Build complete! Documentation available in $OUTPUT_DIR/${NC}"
echo -e "${BLUE}Versions built:${NC}"
for branch in "${VERSION_BRANCHES[@]}"; do
    # Determine version: if branch doesn't have version prefix, use "main"
    if [[ "$branch" =~ ^release/ ]]; then
        VERSION=$(echo "$branch" | sed 's|release/||')
        VERSION_URL="/$VERSION/"
    else
        VERSION="main"
        VERSION_URL="/"
    fi
    echo "  - $VERSION -> $VERSION_URL"
done