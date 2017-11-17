#!/bin/bash

### Run tests comparing three branches
###
###   20171116/original
###
### for Git repository
###
###   https://github.com/drbitboy/isis_socetframesettings

### Unzip modified CUBs

unzip -o gittests.zip

### Empty saved branch basename so no diff is on first pass through loop

unset savebranchbn

### Loop over branches

for branch in 20171116/original 20171116/add-orx 20171116/cleanup ; do

  ### Get last slash-separate token of branch name

  branchbn=$(basename $branch)

  ### Check out that branch

  git checkout $branch

  ### Build socetframesetting ISIS app

  ./buildsfs.bash

  ### Generate .set files from CUBs
  ./rungittests.bash $branchbn

  previousbranchbn=$savebranchbn
  savebranchbn=$branchbn

  [ "$previousbranchbn" ] || continue

  ### Compare .set files from current branch to previous branch

  echo "@Differences $previousbranchbn => $branchbn@" | tr @ \\n

  diff gittests/$previousbranchbn/ gittests/$branchbn/ -yW200 --suppress-common-lines |grep -v diff.-y| awk '{printf "%25.20lf %lg\n", $5-$2,$5-$2}'

  echo ""

done
