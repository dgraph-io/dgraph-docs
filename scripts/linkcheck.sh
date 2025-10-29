#!/bin/bash
# Script to check for broken links in the Hugo-generated site

set -e

GREEN='\033[32;1m'
RED='\033[31;1m'
YELLOW='\033[33;1m'
RESET='\033[0m'

echo -e "${GREEN}Building Hugo site...${RESET}"
hugo --destination=public --baseURL=http://example.com 1> /dev/null

echo -e "${GREEN}Checking for broken links...${RESET}"

# Option 1: htmltest (uses .htmltest.yml config)
if command -v htmltest &> /dev/null; then
    echo -e "${YELLOW}Using htmltest...${RESET}"
    htmltest -c .htmltest.yml
# Option 2: HTMLProofer (requires Ruby and html-proofer gem)
elif command -v htmlproofer &> /dev/null; then
    echo -e "${YELLOW}Using HTMLProofer...${RESET}"
    htmlproofer \
        --allow-hash-href \
        --check-html \
        --disable-external \
        --empty-alt-ignore \
        --url-ignore "/#/" \
        ./public
else
    echo -e "${RED}HTMLProofer not found.${RESET}"
    echo "Install it with: gem install html-proofer"
    exit 1
fi

echo -e "${GREEN}Link check complete!${RESET}"

