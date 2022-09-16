[ONE_Dockerizing] Discussion of Docker Image Shrinking Process

당신의 의견에 따라, `--no-install-recommends`, `rm -rf /var/lib/apt/lists/*`를 Docker 실행 과정에 포함하려 했습니다. 

하지만 이 과정에서 문제가 발생했습니다. 
1. `--no-install-recommends` 관련
`--no-install-recommends` 를 추가하면 `--no-check-certificate`가 적용되지 않아, https 인증 문제가 발생하는 것으로 보입니다. 저의 에러 로그를 첨부합니다. 
```
--2022-09-16 05:42:53--  https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb
Resolving github.com (github.com)... 20.200.245.247
Connecting to github.com (github.com)|20.200.245.247|:443... connected.
ERROR: cannot verify github.com's certificate, issued by 'CN=DigiCert TLS Hybrid ECC SHA384 2020 CA1,O=DigiCert Inc,C=US':
  Unable to locally verify the issuer's authority.
To connect to github.com insecurely, use `--no-check-certificate'
```

2. `rm -rf /var/lib/apt/lists/*` 관련 
`rm -rf /var/lib/apt/lists/*`를 debian package 설치 전에 적용하면, python3에 관한 의존성 문제가 발생합니다. 저의 에러 로그를 첨부합니다.
```
The following packages have unmet dependencies:
 one-compiler : Depends: python3-venv but it is not installable
                Depends: python3-pip but it is not installable
                Depends: python3.8 but it is not installable
                Depends: python3.8-venv but it is not installable
E: Unable to correct problems, you have held broken packages.
The command '/bin/sh -c wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb &&    apt-get install -y ./one-compiler_1.21.0_amd64.deb      && rm -rf /var/lib/apt/lists/*' returned a non-zero code: 100
```

3. 마지막으로 성공한 도커파일 예시에 대해 첨부합니다.
```
FROM ubuntu:18.04 

RUN apt-get update && apt-get install -qqy \ 
    wget \ 
    && apt clean 
 
RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb \ 
    && apt-get install -y ./one-compiler_1.21.0_amd64.deb \ 
    && rm -rf /var/lib/apt/lists/* 
 
ENTRYPOINT ["onecc"] 
```

귀하가, 이런 예시에 대해서 고려한 후, 필요한 패키지를 추가로 설치하라는 뜻인지 아직 확실하지 않아, 두 옵션에 대해 제거 후 이미지 빌드를 성공할 수 있었습니다. 이 내용에 관해 의견을 주실 수 있습니까?