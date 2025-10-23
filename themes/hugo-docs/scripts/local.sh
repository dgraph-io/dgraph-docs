#!/bin/bash

# WIP - a script to build a netlify preview with this theme.

set -e

GREEN='\033[32;1m'
RESET='\033[0m'
THEME_BRANCH=$(git rev-parse --abbrev-ref HEAD)
HOST="${HOST:-https://dgraph.io/docs}"

# create build directory
mkdir "$(dirname "$0")/../build" > /dev/null
# go into /build
pushd "$(dirname "$0")/../build" > /dev/null

# clean build dir if anything exists besides gitignore file
rm -rfv docs > /dev/null
rm -rfv cloud > /dev/null
rm -rfv ../public > /dev/null

git clone https://github.com/dgraph-io/dgraph-docs.git docs

# go into /build/docs
pushd docs > /dev/null

git clone https://github.com/dgraph-io/hugo-docs.git themes/hugo-docs > /dev/null

# go into /build/docs/themes/hugo-docs
pushd themes/hugo-docs > /dev/null

git checkout $THEME_BRANCH > /dev/null

# back into /build/docs
popd > /dev/null

LATEST_RELEASE=$(curl -s https://get.dgraph.io/latest \
  | grep -o '"majorReleases":.*]' \
  | grep -o -m 1 'v[0-9.]*' \
  | head -1)


export CURRENT_BRANCH="main"
export CURRENT_VERSION="main"
export CURRENT_LATEST_TAG=LATEST_RELEASE
export VERSIONS="main,$LATEST_RELEASE"
export DGRAPH_ENDPOINT=${DGRAPH_ENDPOINT:-"https://play.dgraph.io/query?latency=true"}
export CANONICAL_PATH="$HOST"

BASE_URL=""

if [[ $1 == "-p" || $1 == "--preview" ]]; then
  BASE_URL="$2"
else
  # This enables a live server in vs code
  BASE_URL=http://127.0.0.1:5500/public/
fi

build() # $1 = "main" | /v.+/ | "cloud"
{
  if [[ $1 == "main" ]]; then
    CURRENT_VERSION="main"
    BRANCH="main"
    DIR=""
  elif [[ $1 == "cloud" ]]; then
    CURRENT_VERSION=
    BRANCH=
    DIR=$1
  else
    CURRENT_VERSION=$1
    BRANCH="release/$1"
    DIR=$1
  fi

  HUGO_TITLE="Dgraph Theme Preview" \
    CANONICAL_PATH=${HOST} \
    VERSIONS="main,$LATEST_RELEASE" \
		CURRENT_BRANCH=$BRANCH \
		CURRENT_LATEST_TAG=$LATEST_RELEASE \
		CURRENT_VERSION=$CURRENT_VERSION \
    hugo \
		  --destination="../../public/$DIR" \
		  --baseURL="$BASE_URL/$DIR" 1> /dev/null
}

build "main"

git checkout "release/$LATEST_RELEASE" > /dev/null

build $LATEST_RELEASE

# back into /build
popd > /dev/null

# remove cloud repo copy. All content is now in the same repo !
# git clone https://github.com/dgraph-io/cloud-docs.git cloud > /dev/null
# git clone https://github.com/dgraph-io/hugo-docs.git cloud/themes/hugo-docs > /dev/null

# go into /build/cloud/themes/hugo-docs
# pushd cloud/themes/hugo-docs > /dev/null

# git checkout $THEME_BRANCH > /dev/null

# back into /build/
#popd > /dev/null

# go into /build/cloud
#pushd ./cloud > /dev/null

# build "cloud"

# back into /build
#popd > /dev/null

cd ../
rm -rfv build > /dev/null

# back into beginning dir
popd > /dev/null

echo -e "$GREEN Completed Build. View the public directory at $BASE_URL $RESET"
echo -e "If building locally port 5500 may need to be set staticaly in VScode settings. Alternatively pass your own public directory path using the -p flag."
