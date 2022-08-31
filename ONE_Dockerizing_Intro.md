# ONE Dockerizing Intro

- Artificial intelligence (AI) techniques are getting popular and utilized in various products and services. 
    - 인공지능(AI) 기술은 다양한 제품과 서비스에서 활용되며 각광받고 있다.

- Cloud-based AI techniques have been used to perform computation/memory intensive inferences because of the powerful servers on cloud.
    - 클라우드 기반 AI 기술은 클라우드의 강력한 서버로 인해, 계산과 메모리 집약적 추론을 위해 사용되었다.

- On-device AI technologies are recently drawing attention from the mobile industry for **response time reduction, privacy protection, and connection-less** AI service.
    - On-Device AI 기술은 최근 모바일 업계에서 **응답 시간 단축**, **개인 정보 보호**, **무연결** AI 서비스로 주목받고 있다.



## ONE dockerizing

**ONE : On-device Neural Engine**

### Prior knowledge

#### One Compiler 

- A tool that compiles a given model file to run on the target NPU(backend).
    - 대상 NPU(백엔드)에 실행되도록 지정된 모델 파일을 컴파일 하는 도구 
        - NPU : 인공지능 학습과 실행에 최적화된 프로세서를 말함 
- Various NPUs(backends) can be supported through implementation.
    - 구현을 통해 다양한 NPU 지원 가능 

#### TOOLCHAIN

- A set of all tools that can compile models for use in target npu using ONE compiler.
    - 하나의 컴파일러를 사용하여 대상 npu에 사용할 모델을 컴파일할 수 있는 모든 도구 집합입니다.

#### Docker 

- Configures an isolation environment to ensure consistent results without being affected by other environment or functions.
    - 다른 환경이나 기능의 영향을 받지 않고 일관된 결과를 보장하도록 격리 환경을 구성합니다.
- Guaranteeing various working environments;
    - 다양한 근무환경 보장
- Use Linux OS on Windows & Mac
    - Windows 및 Mac에서 Linux OS 사용
- Docker is lightweight and fast.
    - 도커는 가볍고 빠르다.

#### Debian Package

- Contains all of the files necessary to implement a set of related commands or features. (e.g., binary file, config file and libraries etc.)
    - 관련 명령 또는 기능 집합을 구현하는 데 필요한 모든 파일을 포함합니다. (예: 이진 파일, 구성 파일 및 라이브러리 등)

- Uses this package format in Debian, Ubuntu, Linux Mint etc.
    - Debian, Ubuntu, Linux Mint 등에서 이 패키지 형식을 사용합니다.



### Purpose 

- Supports ONE tool in an unsupported environment
    - For now, ONE is only supported in Ubuntu 18.04. (Ubuntu 20.04 unofficial support)
- Different versions of ONE tools can be used comfortably
    - When installed in the Ubuntu filesystem, only one version can be installed and used, but using the docker, this allows user to use various versions of toolchains at the same time.
- Installs and uses toolchain lightly and quickly using Docker
    - The docker itself is fast, light and supports reuse of once generated docker images.



### How

- Implement a Debian package for ONE Compiler using docker.
    - It contains a single script file and Dockerfile to build docker container.
    - If there is an one tool in filesystem, a single script file runs the one tool.
    - If there is not installed an one tool in filesystem, a single script file builds a Docker image and run one tool using the generated Docker image.
    - User can select the ONE Compiler Debian package version.

- 도커를 사용하여 하나의 컴파일러를 위한 데비안 패키지를 구현합니다.
    - 여기에는 단일 스크립트 파일과 도커 컨테이너를 빌드하는 도커 파일이 포함되어 있습니다.
    - 파일 시스템에 하나의 도구가 있는 경우 단일 스크립트 파일이 하나의 도구를 실행합니다.
    - 파일 시스템에 하나의 도구가 설치되어 있지 않은 경우, 단일 스크립트 파일은 도커 이미지를 작성하고 생성된 도커 이미지를 사용하여 하나의 도구를 실행합니다.
    - 사용자는 ONE 컴파일러 데비안 패키지 버전을 선택할 수 있습니다.

- Implement ONE toolchain in ONE-Vscode.

    - Create ONE backend toolchain and interoperate with a Debian package for ONE Compiler using docker.

    - Toolchain view shows a toolchain called ONE.

    - Compile the model file with the selected ONE toolchain.

- ONE-VScode에서 ONE toolchain을 구현합니다. 

    - 하나의 백엔드 툴체인을 만들고 도커를 사용하여 하나의 컴파일러용 데비안 패키지와 상호 운용합니다.
    - Toolchain view는 ONE이라는 툴체인을 보여준다.
    - 선택한 하나의 도구 체인으로 모델 파일을 컴파일합니다.
