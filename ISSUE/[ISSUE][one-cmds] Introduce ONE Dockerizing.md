[toc]

# [one-cmds] Introduce ONE Dockerizing

## 1st

### What

**`ONE Dockerizing`**에 대해 소개합니다. 

### Why

현재, onecc는 오직 Ubuntu 18.04와 20.04(비공식 지원)에만 지원합니다.

그래서 사람들은 다른 환경에서 onecc를 사용하기 쉽지 않습니다.

우리의 `one-dockerizing`은 도커를 사용해 onecc를 유저들이 다른 환경에서 쉽게 사용할 수 있게 할 것입니다.

우리의 최종목표는 도커를 이용한 onecc를 Window,Mac 등에서 사용하게 할 것이지만, 현재 우리는 Linux 환경에서 작업하고, 현재 우리의 목표는 모든 리눅스 환경에서 `ONE-Dockerizing`을 실현하는 것입니다. 

### Scenario
#### System Scenario

1. 유저에게 입력된 커맨드를 받습니다.
2. 유저의 환경이 onecc-docker를 실행할 수 있는지 확인합니다. (python3, docker 등)
3. Docker 컨테이너를 실행합니다.
    - 도커 이미지가 존재하지 않을 때 
        - 도커 이미지를 생성합니다.
        - 컨테이너를 실행합니다.
    - 도커 이미지가 존재할 때 
        - 컨테이너를 실행합니다.
    - 도커 컨테이너는 볼륨으로 컨테이너와 유저의 /home 경로를 공유하며, 현재 유저의 working directory로 Working directory를 설정합니다.
        - `docker run --rm --name {container_name} -v /home:/home --workdir {user_pwd} {docker_image} {user_command}`
4. circlefile과 nnpackage를 `.cfg`파일과 Tensorflow 모델로 생성하고 공유된 볼륨을 통해 유저는 결과를 전달받습니다.

#### User Scenario

- onecc와 관련되어있는 옵션을 포함한 `*.cfg` 파일 및 Tensorflow 모델 파일을 생성합니다.
- 유저가 onecc-docker를 실행합니다.(유저가 원하는 flag를 포함해서 )
    - `onecc-docker -C *.cfg`
- 유저는 원하는 결과를 얻을 수 있으며, 아래와 같습니다.
    - version
    - circlefile,nnpackages
    - help message


### TODO

우리는 먼저 "onecc-docker"를 실행하기 위해 도커 관련 작업을 실행할 것이다. 도커 이미지를 만들려면 도커 파일이 필요하므로 도커 파일을 만듭니다.
둘째, "onecc-docker" 셸 스크립트를 작성하고 시스템에서 Docker를 실행할 것입니다.
마지막으로 Debian Package에 "onecc-docker"를 제공하고 싶습니다.

이 작업에 필요한 사항을 아래에 요약하여 업데이트하겠습니다.

- [ ] Create Dockerfile
    - [ ] 사용자가 입력한 명령을 사용하여 Docker 컨테이너를 성공적으로 실행합니다.
        - [ ] `-I,` `-C`, `-O`,..
- [ ] onec-docker shell script 만들기 
    - [ ] 도커 설치여부 확인 
    - [ ] python3 설치 여부 확인 
    - [ ] onecc 설치여부확인 
    - [ ] 이미지가 존재하면 Docker container 실행, 없으면 이미지 만들고 실행 
- [ ] `onecc-docker`가 포함된 Debian pakcage 생성 

related issue : #8232

/cc [@Samsung/ootpg](https://github.com/orgs/Samsung/teams/ootpg)



## 2nd

### seanshpark

그다지 중요하지 않지만 시나리오에 관해 언급하고 싶은 것들이 있다.

- 사용자 관점에서 시나리오를 내부 구현과 분리하는 것이 좋다
- 나는 다음과 같이 유저가 행동할 것으로 본다. 
    - model.pb, model.cfg와 같은 cfg 파일을 만든다. 
    - `oneccdocker -C mymodel.cfg` 형태로 실행한다.
    - 유저는 circle파일을 받는다.
- 여러 솔루션이 될 수 있는 다른 것들이 시스템 안에서 수행된다. 

### seanshpark

todo에 대해서는 

- 나는 실제로 내부 구현 로직에 대해 완벽히 파악할 수 없다.
- todo 항목을 나열하기 전에 먼저 수행방법을 설명해주는 것이 좋을 것 같다. 

### holawan

[@seanshpark](https://github.com/seanshpark)
의견 고맙습니다. 

> About the scenario, this is not that important but I'd like to mention this;

나는 유저 입장의 시나리오을 고려해볼게요.

> About todo...

다른 이슈를 고려해 Todo를 개선하겠습니다. 



## 3rd

### jyoungyun

> I think you first do describe how you are going to make it done before listing TO DOs.

**최종 결과물 **

`onecc-docker` debian package

   - 이 팀은 도커 이미지를 구축하기 위해 onecc와 Dockerfile을 실행하는 여러 스크립트가 포함된 onecc-docker debian 패키지를 생성할 예정이다.

**User scenario**

1. `onecc-docker` debian package 설치
2. `onecc-docker` script 실행
   1. If `one-compiler` was installed before
      - onecc-docker 스크립트를 통해 onecc 실행
   2. No installed `one-compiler`
      -  `one-compiler`가 포함된 도커 이미지 빌드
      - 빌드된 도커 이미지를 통해 'onecc' 실행

제가 이렇게 설명을 더 하면 이해하는데 도움이 될까요?

/cc @seanshpark 

### seanshpark

> Install onecc-docker debian package

Q) 그래서 유저는 `one-compiler` debian package를 설치하지 않거나 설치할 수 없나요?

- 미래에 macosx의 경우, 만약 우리(또는 누군가) `onecc-docker.dmg`를 제공하면, 사용자는 `onec-docker`를 통해 Docker 내부에서 `onecc`를 실행할 수 있을까요?

> If one-compiler was installed before

Q)이 라인에서 "one-compiler" 데비안 패키지가 기본적으로 설치되어있나요 아니면 Docker image를 통해 설치되나요?

> No installed one-compiler

Q) 이것은 `one-compiler` debian package로 보이는데 맞나요?
Q) 이후 도커 내부에서 `onecc`가 실행됩니다. 
만약 사용자가 `one-compiler`를 설치하면, onecc가 도커와 네이티브에 생기게 됩니다. 
다른 버전일 수도 있습니다. 버전 불일치에 대한 계획이 있나요? 
Q) 둘다 설치된 경우 `onecc` (도커 또는 네이티브)를 선택할 수 있는 옵션이 있나요? 아니면 도커가 더 우선순위가 높게 실행되나요?
Q) `one-docker`가 단순성을 위해 첫번째 구현에 대해서만 Docker 이미지를 생성한다는 시나리오를 수정할 수 있나요? 



### jyoungyun

> Q) 그래서 유저는 `one-compiler` debian package를 설치하지 않거나 설치할 수 없나요?

`onecc-docker` 데비안 설치 여부와 관계없이, `one-compiler` 데비안패키지를 설치할 수 있습니다. 

> - 미래에 macosx의 경우, 만약 우리(또는 누군가) `onecc-docker.dmg`를 제공하면, 사용자는 `onec-docker`를 통해 Docker 내부에서 `onecc`를 실행할 수 있을까요?

네 그것이 우리의 궁극적 목표입니다. (비록 SSAFY는 mac용 패키지를 만들지는 않습니다. )

> Q)이 라인에서 "one-compiler" 데비안 패키지가 기본적으로 설치되어있나요 아니면 Docker image를 통해 설치되나요?

이것은 `one-compiler` 데비안 패키지가 파일 시스템에 설치되어있음을 의미합니다. 

> Q) 이것은 `one-compiler` debian package로 보이는데 맞나요?

네 맞습니다. 

> Q) 이후 도커 내부에서 `onecc`가 실행됩니다. 
> 만약 사용자가 `one-compiler`를 설치하면, onecc가 도커와 네이티브에 생기게 됩니다. 
> 다른 버전일 수도 있습니다. 버전 불일치에 대한 계획이 있나요? 

그래서 우리는, `onecc-docker` 스크립트의 버전 인자를 고려합니다.

현재 우리는 ,버전에 대해 크게 신경쓰지 않습니다. 따라서, `onecc`가 네이티브로 설치되면 `onecc`를 사용하게 되고, 설치된 `onecc`가 없다면 도커 이미지 내부에 최신 `onecc`를 사용할 것입니다. (도커 이미지를 만들 때 최신 `one-compiler`패키지를 사용하기 때문입니다. 

이후, 우리가 버전을 지원한다면, 버전 번호를 입력하게 할 것입니다. 그리고 정확히 일치하는 `one-compiler`가 설치되어있다면, 네이티브로 사용할 것입니다. 하지만 사용자 입력에 설치된 버전이 일치하지 않으면, 도커 이미지의 `onecc`를 사용할 것입니다. 

사용자가 버전 번호를 입력하지 않으면 네이티브 `onecc`가 docker image의 `onecc`보다 우선됩니다. 

> Q) 둘다 설치된 경우 `onecc` (도커 또는 네이티브)를 선택할 수 있는 옵션이 있나요? 아니면 도커가 더 우선순위가 높게 실행되나요?

네이티브 `onecc`의 우선순위가 높습니다. 

> Q)  `one-docker`가 단순성을 위해 첫번째 구현에 대해서만 Docker 이미지를 생성한다는 시나리오를 수정할 수 있나요? 

좀 더 설명해주시겠어요? 당신의 의도를 파악하기 어렵습니다. 



### seanshpark

> 좀 더 설명해주시겠어요? 당신의 의도를 파악하기 어렵습니다. 

시나리오에 따르면, `onecc-docker`는 Native 설치 또는 Docker 버전에서 `onecc`를 실행할 수 있습니다. 

첫 번째 구현의 경우 Docker 버전에만 중점을 두고 있습니다. 

네이티브 `one-compiler` 패키지가 설치되어있는지 여부는 신경쓰지 마십시오. 

이 작업이 정상적이고 안정적이면 Native 버전이 설치되어있는지 확인하기 위해 수정할 것입니다.

그래서 시간이 허락할 때까지는 시나리오가 조금 복잡합니다. 





### jyoungyun

> by the scenario, `onecc-docker` can either run `onecc` in Native installed or the Docker version.
> for the first implementation, let's just focus on running ONLY in the Docker version.
> do not care if there is Native `one-compiler` package installed or not.

오, 좋은 생각이야. 저는 이 접근 방식이 명확하고 안전한 디자인이 될 것이라고 생각합니다.
이것에 대해 어떻게 생각하세요?

/cc [@Samsung/ootpg](https://github.com/orgs/Samsung/teams/ootpg) [@Samsung/ootpg_docker](https://github.com/orgs/Samsung/teams/ootpg_docker)



### holawan

> 오, 좋은 생각이야. 저는 이 접근 방식이 명확하고 안전한 디자인이 될 것이라고 생각합니다.
> 이것에 대해 어떻게 생각하세요?

시나리오를 수정할 필요가 있다는 뜻 같습니다. 

유저의 네이티브 `one-compiler` 설치 여부는 확인하지 않고 (버전 불일치, 설치 여부 등) 도커를 이용한 "onecc-docker"를 문제없이 실행하는 것에 집중하라는 말씀이실까요? 


- "onecc-docker"를 실행할 때, 유저에게 "circle file"이나 "nnpackages" 제공 등

내가 이해한게 맞다면, 곧 스켈레톤 코드를 첨부하여 추가적인 PR을 드리겠습니다 :) 

의견주셔서 감사합니다:)