#!/bin/bash
set -e
# Important for clean builds on Netlify
if ! git remote | grep -q origin ; then
    git remote add origin https://github.com/dgraph-io/dgraph-docs.git
    git fetch --all
fi

GREEN='\033[32;1m'
RESET='\033[0m'

# script used to build a release branch
# expect the branch to be named release/<version>
# argument $1 is the netlify base url
# argument $2 is the $HEAD netlify variable which is the branch name

echo "branchdeploy URL $1 branch $2"
releaseVersion=$(echo $2 | sed 's/.*\///')
echo "version '$releaseVersion'"
VERSION_STRING="$releaseVersion"
# In Unix environments, env variables should also be exported to be seen by Hugo
export VERSIONS=${VERSION_STRING}

run() {
  export DGRAPH_ENDPOINT=${DGRAPH_ENDPOINT:-"https://play.dgraph.io/query?latency=true"}
  export HUGO_TITLE="Dgraph Doc - ${releaseVersion}"

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

    echo -e "$(date) $GREEN  Generating documentation static pages in the folder public/docs/$releaseVersion. $RESET"

    CURRENT_VERSION=${releaseVersion} \
    VERSIONS=${VERSION_STRING} \
      hugo --destination="public/docs/$releaseVersion" --baseURL="$1/docs/$releaseVersion" 1> /dev/null
    cp "public/docs/$releaseVersion/sitemap.xml" public > /dev/null
    echo -e "$(date) $GREEN  Done building. $RESET"

  popd > /dev/null
}

run "$1"
