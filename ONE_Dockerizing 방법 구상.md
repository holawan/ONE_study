## 관련 이슈

https://github.com/Samsung/ONE/issues/8232

### **How**

**Dockerfile**

- Based on Ubuntu 18.04 or 20.04
- Install `one-compiler`
- Set `onecc` as entrypoint

This dockerfile generates a docker image for `one-compiler` on Ubuntu 18.04 or 20.04.User can run a process in isolated container using this docker image with several `onecc` parameters.

**`onecc-docker` tool**

- Run docker container with `onecc` parameters and several docker run params

This `onecc-docker` tool runs docker container using above docker image. It sets user and group ids the same as those on host PC, mounts `/tmp` and `${HOME}` directory, adds `HOME` environment, and changes working directory to current directory.

**`one-compiler-docker` package**

- files
    - `Dockerfile`
    - `onecc-docker` files
- install
    - `Dockerfile` to `/usr/share/one/docker/`
    - `onecc-docker` to `/usr/share/one/bin/`
- postinst
    - Install symbolic link from `/usr/share/one/bin/onecc-docker` to `/usr/bin/onecc` with priority 0 using [update-alternatives](https://linux.die.net/man/8/update-alternatives) tool
- prerm
    - Remove symbolic link

**`one-compiler` package**

- postinst
    - Install symbolic link from `/usr/share/one/bin/onecc` to `/usr/bin/onecc` with priority 1 using [update-alternatives](https://linux.die.net/man/8/update-alternatives) tool(1 is higher priority than 0)
- prerm
    - Remove symbolic link

### 구현 계획

최종 목표 : **`one-compiler-docker` package (데비안 패키지) 생성**

1. Dockerfile 작성
    - ubuntu 18.04(support)버전으로 작성
        - 유저가 선택한 debian package를 wget로 받아오고, 해당 패키지 실행
    - 해당 Dockerfile 이용 이미지 생성, 컨테이너 빌드 후 `onecc-docker` 실행 시 circle file 생성하게 하기
2. Shell Script 작성(python 기반)
    - `onecc-docker` 파일 만들기
    - flag 및 parameter 지정
    - volume을 통해 `user directory`와 `docekr container directory` mount
    - `onecc-docker`와 함께 입력된 Argument들을 담아 커맨드 입력 시 , volume으로 *.cfg, *.pb, *.tflite 등을 mount, docker 컨테이너 내부에서 `onecc`를 실행 후 리턴된 circle file, nnpackage, [opt.circle](http://opt.circle) file들  또한 volume으로 mount

우리가 만들 것은 현재  `Dockerfile`, `onecc-docker` 가 추가된 Debian Package `one-compiler-docker`

### docker 시나리오

- `onecc-docker`를 어떻게 동작시켜야할까에 대해서 생각해본 2가지 방식

사전작업 : docker container 실행 시 volume 지정

**계획 1. onecc-docker를 실행하면 cmd input 기반 컨테이너를 실행 후 종료된다.**

- onecc-docker 실행 (and 버전 선택)
- Docker 컨테이너 내부에서 해당 버전과 directory 기반 *.cfg 파일로 circle file 생성

volume 매칭 관련 Issue

> This `onecc-docker`tool runs docker container using above docker image. It sets user and group ids the same as those on host PC, mounts `/tmp`and `${HOME}`directory, adds `HOME`environment, and changes working directory to current directory.

### 추가 구현 계획

- 유저의 버전 선택

    1. 유저가 `onecc-docker` 실행 시 command line에서 버전을 선택하게 한다

    2. debian package에  ubuntu 18.04 버전으로 작성한 Dockerfile과 

        ```
        onecc-docker
        ```

        포함

        - 유저가 `onecc-docker` 실행 시
        - github의 release 별 debian package를 API로 받아와서, 해당 버전 중 하나의 패키지 `onecc`로 실행

## 구현 방법

### Dockerfile

**Ubuntu 18.04 , Ubuntu 20.04 버전을 기반으로 2가지 Dockerfile을 작성한다.**

### onecc-docker

**onecc 및 관련 library를 상속받아 onecc-docker를 만든다.**

- how to
    - `onecc-docker`에 script를 작성하여 Dockerfile 기반으로 Docker image 생성 및 contianer를 구동하게 한 후, 입력된 인자들도 함께 Entrypoint에 넘긴다.
    - 끝?
