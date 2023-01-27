#!/bin/bash
# This script runs in a loop (configurable with LOOP), checks for updates to the
# Hugo docs theme or to the docs on certain branches and rebuilds the public
# folder for them. It has be made more generalized, so that we don't have to
# hardcode versions.

# Warning - Changes should not be made on the server on which this script is running
# becauses this script does git checkout and merge.

set -e

# Important for clean builds on Netlify
if ! git remote | grep -q origin ; then
    git remote add origin https://github.com/dgraph-io/dgraph-docs.git
    git fetch --all
fi

GREEN='\033[32;1m'
RESET='\033[0m'
HOST="${HOST:-https://dgraph.io/docs}"
# Name of output public directory
PUBLIC="${PUBLIC:-public}"
# LOOP true makes this script run in a loop to check for updates
LOOP="${LOOP:-true}"
# Binary of hugo command to run.
HUGO="${HUGO:-hugo}"
THEME_BRANCH="${THEME_BRANCH:-main}"

# Place the latest version at the beginning so that version selector can
# append '(latest)' to the version string, followed by the main version,
# and then the older versions in descending order, such that the
# build script can place the artifact in an appropriate location.

getMajorVersions=$(curl -s https://get.dgraph.io/latest \
| grep -o '"majorReleases":.*]' | grep -o '".*"' |  grep -o '"[^[]*$' \
| sed  "s/\"//g"  | sed  "s/\,/ /g" | sed  "s/v20.03/ /g" | sed  "s/v21.12/ /g" | sed "s/v20.07/ /g")
echo $getMajorVersions
export MAJOR_VERSIONS=(
  $getMajorVersions
)
echo ${MAJOR_VERSIONS:0}
echo ${MAJOR_VERSIONS[@]:1}

export VERSIONS_ARRAY=(
  'v22.0'
  ${MAJOR_VERSIONS:0}
  ${MAJOR_VERSIONS[@]:1}
  'main'
  'v21.12'
)
echo ${VERSIONS_ARRAY[@]:0}
for version in "${VERSIONS_ARRAY[@]}"
do
  echo "version"
  echo $version
  latest_version=$(curl -s https://get.dgraph.io/latest | grep -o '"latest": *"[^"]*' | grep -o '[^"]*$' | sed  "/^v21.12/d" | sed  "/^v20.03/d" | sed  "/^v20.07/d" | grep  "$version" | sort | uniq | head -n1)
  echo "latest version"
  echo $latest_version
done
