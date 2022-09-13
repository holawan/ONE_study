# ONE_Dockerizing 시나리오

## User Scenario

### Who

- Linux OS(Ubuntu 18.04 or Ubuntu 20.04)를 사용할 수 없거나, 사용하고 싶지 않은 유저
- ONE을 이용해 TensorFlow 모델을 Circle file로 변환하고 싶은 유저 

### What

- 운영체제에 구애받지 않고, `one-cmds`를 이용해 TensorFlow 모델 Circlefile로 변환 

### When

- `onecc`를 실행하기 위한 TensorFlow Model file과 `onecc` 관련 Configure 파일이 준비되었을 때 

### Where

- 사용자의 운영체제 

### Why

- 현재 `onecc`, `one-build`는 Ubuntu 18.04, Ubuntu 20.04에서만 이용할 수 있지만, 해당 환경이 아니라도 서비스를 이용할 수 있게 하기 위함입니다.

### How

1. TensorFlow Modle file(`.pb`, `.tfilte` ..)와 `onecc` 관련  수행하고 싶은 옵션을 담은 `*.cfg`를 생성

2. `onecc-docker` 커맨드 실행 

    - ex

        ```
        $ onecc-docker -C *.cfg
        $ onecc-docker -W *.workflow.json
        $ onecc-docekr -C *.cfg -O *.cfg
        ```

3. 원하는 one-compiler version 선택 

4. Docker container 실행

    - User가 선택한 버전의 Docker image가 존재하는지 확인 

    - Docker Image가 없을 때 

        - User가 원하는 버전의 Docker Image 자동 생성 (write_dockerfile, docker image build)

        - Docker container 구동 (docker container run)

    - Docker Image가 있을 때 
        - User가 원하는 버전의 Docker Image로 컨테이너 구동 (docker container run)

5. Docker container 내부에서 volume으로 공유받은 `*.cfg` 및 TensorFlow Model로 Circle file 및 nnpackage 생성 

## User Interface

### `-v` , `--version`

- `onecc-docker` 실행

    ```
    $ onecc-docker -v 
    onecc-docker version 0.00.0
    Copyright (c) 2020-2022 Samsung Electronics Co., Ltd. All Rights Reserved
    Licensed under the Apache License, Version 2.0
    https://github.com/Samsung/ONE
    ```

### `-h`, `--help`

- `onecc-docker` 실행

    ```
    $ onecc-docker -h
    Run ONE driver via several commands or configuration file
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -V, --verbose         output additional information to stdout or stderr
      -C CONFIG, --config CONFIG
                            run with configuation file
      -O OPTIMIZATION       optimization name to use (Available optimization options: -O1)
      -W WORKFLOW, --workflow WORKFLOW
                            run with workflow file
    
    compile to circle model:
      import                Convert given model to circle
      optimize              Optimize circle model
      quantize              Quantize circle model
    
    package circle model:
      pack                  Package circle and metadata into nnpackage
    
    run backend tools:
      codegen               Code generation tool
      profile               Profile backend model file
      infer                 Infer backend model file
    ```

### `-C`

- TensorFlow Model file 및 `onecc` 관련 `*.cfg` 준비 

    ```
    $ tree
    .
    ├── inception_v3.pb
    ├── inception_v3.tflite
    ├── inception_v3_2018_04_27.tgz
    ├── labels.txt
    └── onecc.template.cfg
    ```

- `onecc-docker` 실행 

    ```
    $ onecc-docker -C *.cfg
    ```

- 실행 결과 

    ```
    $ tree
    .
    ├── inception_v3.circle
    ├── inception_v3.circle.log
    ├── inception_v3.opt.circle
    ├── inception_v3.opt.circle.log
    ├── inception_v3.pb
    ├── inception_v3.tflite
    ├── inception_v3_2018_04_27.tgz
    ├── inception_v3_pack
    │   └── inception_v3.opt
    │       ├── inception_v3.opt.circle
    │       └── metadata
    │           └── MANIFEST
    ├── inception_v3_pack.log
    ├── labels.txt
    └── onecc.template.cfg
    ```
