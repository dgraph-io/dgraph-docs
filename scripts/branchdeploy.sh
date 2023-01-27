#!/bin/bash

set -e

GREEN='\033[32;1m'
RESET='\033[0m'

# script used to build a release branch
# expect the branch to be named release/<version>
# argument is the netlify base url

releaseVersion=$(git rev-parse --abbrev-ref HEAD | sed 's/release\///')


run() {
  export DGRAPH_ENDPOINT=${DGRAPH_ENDPOINT:-"https://play.dgraph.io/query?latency=true"}
  export HUGO_TITLE="Dgraph Doc - Preview" \

  pushd "$(dirname "$0")/.." > /dev/null
  pushd themes > /dev/null

  if [ ! -d "hugo-docs" ]; then
    echo -e "$(date) $GREEN  Hugo-docs repository not found. Cloning the repo. $RESET"
    git clone https://github.com/dgraph-io/hugo-docs.git
  else
    echo -e "$(date) $GREEN  Hugo-docs repository found. Pulling the latest version from master. $RESET"
    pushd hugo-docs > /dev/null
    git checkout master
    git pull
    popd > /dev/null
  fi
  popd > /dev/null

    echo -e "$(date) $GREEN  Generating documentation static pages in the public folder. $RESET"
      hugo --destination="public/docs/$releaseVersion" --baseURL="$1/docs/$releaseVersion" 1> /dev/null
    cp "public/docs/$releaseVersion/sitemap.xml" public > /dev/null
    echo -e "$(date) $GREEN  Done building. $RESET"

  popd > /dev/null
}

run "$1"
