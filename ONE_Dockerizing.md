

[toc]

# ONE Dockerizing

https://github.com/Samsung/ONE/pull/7332

https://github.com/Samsung/ONE/issues/8232

https://github.com/Samsung/ONE/pull/7319

## Intro

### What 

Let's consider how to use `one-cmds` tools easily for more people.

For now, `one-cmds` tools only support Ubuntu 18.04 and 20.04(not officially).
So people in other environments can't use our tools unless they upgrade the OS (or install Ubuntu OS).

IMO, in this case, docker can be a good solution.

[Docker](https://www.docker.com/) is an open source containerization platform. It supports developer to provide applications into containers. And docker is already available on a variety of Linux platforms, macOS and Windows 10 through Docker Desktop. So if we provide `one-compiler` tool using docker, we can support many types of environment at once.

------

더 많은 사람들이 `one-cmds` toll을 쉽게 사용할 수 있는 방법을 고려해봅시다.

현재 `one-cmds` tool은 Ubuntu 18.04와 20.04(비공식) 만 지원하고 있습니다. 

따라서, 다른 환경에서는 OS를 업그레이드하거나, Ubuntu OS를 사용하지 않는다면 `one-cmds`를 이용할 수 없습니다.

나는 이 경우에 docker가 좋은 해결책이 될 수 있다고 생각합니다.

Docker는 Open source 컨테이너화 플랫폼으로, 개발자가 컨테이너에 어플리케이션을 제공할 수 있게 지원합니다.

그리고 도커는 이미 다양한 Linux Platforms, MacOS, Window10에서 Docker Desktop을 통해 이용할 수 있도록 되어있습니다.

그래서, 우리가 도커를 사용하여 하나의 컴파일러 도구를 제공할 때, 우리는 한 번에 많은 종류의 환경을 지원할 수 있다고 생각합니다. 

-----

### HOW

#### Dockerfile

- Based on Ubuntu 18.04 or 20.04
    - Ubuntu 18.04 또는 20.04 기반
- Install `one-compiler`
    - `one-comiler` 설치 
- Set `onecc` as entrypoint 
    - entrypoint를 onecc로 설정 

This dockerfile generates a docker image for `one-compiler` on Ubuntu 18.04 or 20.04.
User can run a process in isolated container using this docker image with several `onecc` parameters.

-----

이 도커파일은 Ubuntu 18.04 또는 20.04에서 `one-compiler`에 대한 docker image를 생성합니다. 

사용자는 여러 `onecc` parameter가 있는 Docker Image를 사용하여 격리된 컨테이너에서 프로세스를 실행할 수 있습니다. 

-----

#### `one-cc docker` tool

- Run docker container with `onecc` parameters and several docker run params
    - onecc parameter와 여러 도커 실행 params를 사용해 Docker container를 실행합니다. 

This `onecc-docker` tool runs docker container using above docker image. It sets user and group ids the same as those on host PC, mounts `/tmp` and `${HOME}` directory, adds `HOME` environment, and changes working directory to current directory.

-----

이 `onecc-docker` tool은 위의 docker image를 사용하여 docker container를 실행합니다. 사용자 및 그룹 ID를 호스트 PC와 동일하게 설정하고, `\tmp` 및 `${HOME}` 디렉토리를 mount하여 'HOME' 환경 작업 디렉토리를 현재 디렉토리로 변경합니다. 

-----

#### `one-compiler-docker` package 

- files 
    - `Dockerfile`
    - `onecc-docker` files 
- install
    - `Dockerfile` to `/usr/share/one/docker/`
    - `onecc-docker` to `/usr/share/one/bin/`
- postinst(설치 후)
    - Install Symbolic link from `/usr/share/one/bin/onecc-docker` to `/usr/bin/onecc` with priority 0 using [update-alternatives](https://linux.die.net/man/8/update-alternatives) tool 
        - update-alternatives tool을 사용해  `/usr/share/one/bin/onecc-docker` 에서 `/usr/bin/onecc`로 Symbolic 링크를 우선순위 0으로 설치 
- prerm (삭제 전)
    - Remove sympolic link

-----

#### `one-compiler` package

- postinst (설치 후 )
    - Install symbolic link from `/usr/share/one/bin/onecc` to `/usr/bin/onecc` with priority 1 using [update-alternatives](https://linux.die.net/man/8/update-alternatives) tool (1 is higher priority than 0)
        - update-alternative tool을 사용해 `/usr/share/one/bin/onecc`에서 `/usr/bin/onecc`로 Symbolic link를 우선순위 1로 설치 (1이 0보다 우선순위임 )
- prerm
    - Remove Symbolic link

-----

### Todo

dockerfile apt-source and version management

dockerfile 및 apt-source 버전 관리 

-----



## Q&A

### 1. 도커 이미지 관련 

#### 질문 

It seems that users should build a docker image with `Dockerfile` when they start from scratch. Is it impossible to let users to pull the pre-built image from docker hub or somewhere?

------

도커파일 및 도커 이미지를 사용자들이 처음부터 구축해야 하는 것으로 보이는데, 사용자가 Docker hub나 다른 곳에서 미리 build된 이미지를 가져오는 것이 불가능할까요 ?

-----

#### 답변

We can upload Docker image. But it means that we have one more thing to manage. Now we only manage `Dockerfile` however if we upload Docker Image, we need to manage a job related docker image. So it has designed to provide `Dockerfile` directly.

-----

Docker image를 업로드 할 수 있습니다. 하지만 그것은 ONE에서 관리해야하는 것이 하나 더 늘어난다는 것을 의미합니다. 지금은 Dockerfile만 관리하지만, Docker image를 업로드 할 경우 작업에 관련된 Docker image까지 관리해야 합니다. 그래서 현재 Dcoekrfile을 유저가 직접 제공하도록 설계되어 있습니다.

### 2. driver 관련 

#### 질문

`onecc` and `onecc-docker` are different drivers and users can know about it because we are not supporting ubuntu 16.04 officially. So, how about not use same symbolic link? I mean user would use `onecc-docker` and `onecc` as a different driver. We can let users who are working on ubuntu 16.04 to use `onecc-docker` by a message like "You can use `onecc-docker`" when they run `onecc` driver.

`onecc`와 `onecc-docker`는 서로 다른 driver이며, 공식적으로 ubuntu 16.04를 지원하지 않기 때문에 사용자가 이를 알 수 있습니다. 그렇다면, 같은 symbolic link를 사용하지 않는 것은 어떨까요? 제 말의 의미는 유저가 `onecc-docker`와 `onecc`를 다른 driver로 사용할 것이라는 것입니다. ubuntu 16.04에서 작업중인 사용자가 `onecc` driver를 실행할 때, `onecc-docker`를 사용할 수 있습니다.

-----

#### 답변 

It is an idea to extend existing `onecc` tool. Existing tool only supports specific environment. However new designed `onecc` will support all environment even though our tool does not support that environment.

I thought it was appropriate to provide the user in one tool than the multiple tools that the user should use depending on the environment.

-----

이는 기존 `onecc` tool을 확장하자는 아이디어입니다. 기존 tool은 특정 환경(Ubuntu 18.04 or 20.04)만 지원합니다. 그러나 ONE이 해당 환경들을 지원하지 않더라고, 새로운 디자인의 `onecc`는 모든 환경을 지원할 것입니다.

환경에 따라 사용자가 사용해야하는 여러 tool 보다는 하나의 도구를 사용자에게 제공하는 것이 더 적절하다고 생각했습니다. 
