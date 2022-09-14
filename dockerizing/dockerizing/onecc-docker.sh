#!/usr/bin/env bash

if command -v onecc > /dev/null 
        then
        version=( $(onecc --version) )
        exec "python3" "onecc-docker.py" "${version[2]}" "$@" 
        exit 0
else
        exec "python3" "onecc-docker.py" "0" "$@" 
        exit 0
fi

# exec "docker" "build"  "-t" "onecc-docker" "."
# exec "docker" "create" "--name" "onecc-docker" "onecc-docker"
# exec "docker" "start" "onecc-docker"
# versions=( $(git ls-remote -t --refs https://github.com/Samsung/ONE/ ) )
# echo ${versions[@]}
# git ls-remote --tags https://github.com/Samsung/ONE/ --sort=v:refname ->버전 가져오기