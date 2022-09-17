# ONE_DOCKERIZING



### 1. Dockerfile 생성 

```
FROM ubuntu:18.04 
RUN apt-get update 
RUN apt-get install -y wget 
RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb 
RUN apt install -y ./one-compiler_1.21.0_amd64.deb 
WORKDIR /home/ 
RUN mkdir test 
WORKDIR /home/test 
CMD ["onecc", "-C", "onecc.template.cfg"]

```

### 2. 도커 이미지 생성

- Dockerfile이 있는 위치에서 실행하거나, CommandLine에 Dockerfile 위치 명시

```bash
docker build -t onecc:1.21.0 .
```

### 3. 도커 컨테이너 빌드 

#### 3-1) 실행 후 종료

- Volume으로 공유할 경로는 현재 사용자가 임의로 지정할 수 있으며, Dockerfile과 유저의 `*.cfg`, TensorFlow 파일이 있는 경로를 공유  

```bash
docker run --rm --name onecc_1.21.0 -v /home/test:/home/test onecc:1.21.0
```

#### 3-2) 실행 후 유지 

```
docker run -itd --name onecc_1.21.0 -v /home/test:/home/test onecc:1.21.0
```

### 4. 실행 결과 

```bash
Estimated count of arithmetic ops: 11.460 G  ops, equivalently 5.730 G  MACs
model2nnpkg.sh: Generating nnpackage inception_v3.opt in inception_v3_pack
```

