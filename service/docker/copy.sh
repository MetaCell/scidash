#!/bin/bash
clone_url=$1
target_branch=$2
origin_branch=$3
default_branch=$4

#################################################################################################
# 
# Use it for copying repositories:
#   - org.geppetto.frontend
#   - org.geppetto.model
#   - org.geppetto.core
#   - etc
#
# It requires:
#   - target_branch: main branch to test ($TRAVIS_BRANCH)
#   - origin_branch: branch where the new code was written ($TRAVIS_PULL_REQUEST_BRANCH)
#   - default_branch: branch to use as main branch in case $main_branch does not exist
# 
#################################################################################################

name=`echo $clone_url | sed 's~^.*/~~g' | sed 's~.git~~g'`
mkdir $name

if [ -z $origin_branch ]; then   
  git ls-remote --heads --tags $clone_url | grep -E 'refs/(heads|tags)/'$target_branch > /dev/null
  if [ $? -eq 0 ]; then
    download_url=`echo $clone_url | sed 's~\.git~/archive/'$target_branch'.zip~g'`
    /bin/echo -e "\e[1;35mDownloading <$target_branch> branch for $name.\e[0m"
  else
    download_url=`echo $clone_url | sed 's~\.git~/archive/'$default_branch'.zip~g'`
    /bin/echo -e "\e[1;35mDownloading <$default_branch> branch for $name.\e[0m"
  fi
  curl -sL $download_url | bsdtar -xzf - -C $name --strip-components 1
else
  # clone repository
  /bin/echo -e "\e[1;35mCloning <$default_branch> branch for <$name> repository.\e[0m"
  git clone -b $default_branch $clone_url
  cd $name
  # check if target_branch exists in the repo and ckeckout default_branch if it does not
  git show-ref | grep -E 'refs/remotes/origin/'$target_branch > /dev/null
  if [ $? -eq 0 ]; then
    /bin/echo -e "\e[1;35mCheckout <$target_branch> branch.\e[0m"
    git checkout $target_branch
  else
    /bin/echo -e "\e[1;35m<$target_branch> branch does not exist in <$name> repository, we stay on <$default_branch> branch.\e[0m"
  fi
  # check if origin_branch exists in the repo and merge origin_branch in target branch if it does
  git show-ref | grep -E 'refs/remotes/origin/'$origin_branch > /dev/null
  if [ $? -eq 0 ]; then
    /bin/echo -e "\e[1;35mMerging <$origin_branch> branch into (<$target_branch>|<$default_branch>) for <$name> repository.\e[0m"
    git merge --no-edit --no-stat --no-summary --quiet --no-progress origin/$origin_branch
  else
    /bin/echo -e "\e[1;35m<$origin_branch> branch does not exist in <$name> repository, no merge will be performed on this repository.\e[0m"
  fi
  rm -rf .git
  cd ..
fi
