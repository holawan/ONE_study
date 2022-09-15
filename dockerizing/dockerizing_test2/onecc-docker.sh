#!/usr/bin/env bash

if ! command -v docker > /dev/null
        then
        echo "docker must be installed"
        exit 0
fi

if ! command -v python3 > /dev/null
        then
        echo "python3 must be installed"
        exit 0
fi

exec "python3" "onecc-docker.py" "$@"
