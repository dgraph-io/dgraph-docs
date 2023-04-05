#!/bin/bash

# obter o nome da branch de origem
PR_BRANCH=$(echo $GITHUB_REF | sed 's/refs\/pull\///;s/\/head//')

echo $PR_BRANCH
echo '---'
echo $PR_HASH
# obter o hash da commit de destino
PR_HASH=$(gh pr view $PR_NUMBER --json headRefOid --jq .headRefOid)

# ver as diferenças
git diff $PR_BRANCH $PR_HASH

