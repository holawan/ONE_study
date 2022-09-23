# onecc-docker

_onecc-docker_ is designed to improve user usability.

## Description

For now, `one-cmds` tools only support Ubuntu 18.04 and 20.04(not officially).
So, It is difficult for people in different environments to use our tools without using ubuntu18:04.

To overcome this limitation, we provide _onecc-docker_ that runs using a docker so that users can use `one-cmds` more widely.

This tool aims at the following objectives.

- Unsupported Ubuntu OS supports ONE tool
- Different versions of ONE tools can be used comfortably
- Install and use ONE tools lightly and quickly using Docker

## Requirements

- Any Linux distribution
- Docker

    - Requires root privileges.
            - _onecc-docker_ requires the current `user ID` to be included in the `docker group` because it requires the docker-related commands to be executed without `sudo` privileges.
                  - See "[Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/)"
- Python 3.8
