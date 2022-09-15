#8232

## why
#8232 issue와 관련하여 더 많은 유저가 쉽게 `one-cmds`를 사용할 수 있도록, Dockerizing을 하려고 합니다.

간단히, 제가 수행하고 있는 방식에 대한 견해를 묻고자 이슈를 남깁니다.

## how
나는 현재 아래 방식으로 Dockerizing을 진행했습니다. 

### 요약 

1. Dockerizing을 위한 TensorFlow Model을 가져오고, Configure File을 작성합니다.
2. Docker Image 생성을 위한 Dockerfile을 작성하고, 컨테이너를 구동합니다. 
    - `onecc`를 실행이 끝나면 컨테이너는 종료되며 삭제됩니다. 
3. circle file 및 nnpackage가 생성되었는지 확인합니다. 



### Import  Tensorflow model for testing

먼저, 저의 리눅스(wsl)의 `/home/test/` 경로를 생성하고, 테스트를 진행할 모델 file을 [inception_v3](https://storage.googleapis.com/download.tensorflow.org/models/tflite/model_zoo/upload_20180427/inception_v3_2018_04_27.tgz) 다운로드 받은 후, Configure file을 생성했습니다. 

```
# /home/test/
$ wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/model_zoo/upload_20180427/inception_v3_2018_04_27.tgz

$ tar -xvf inception_v3_2018_04_27.tgz

$ vi onecc.template.cfg

$ tree
.
├── inception_v3.pb
├── inception_v3.tflite
├── inception_v3_2018_04_27.tgz
├── labels.txt
└── onecc.template.cfg
```

- onecc.template.cfg

    ```
    [onecc]
    one-import-tf=True
    one-import-tflite=False
    one-import-bcq=False
    one-import-onnx=False
    one-optimize=True
    one-quantize=False
    one-parition=False
    one-pack=True
    one-codegen=False
    
    [one-import-tf]
    input_path=inception_v3.pb
    output_path=inception_v3.circle
    input_arrays=input
    input_shapes=1,299,299,3
    output_arrays=InceptionV3/Predictions/Reshape_1
    converter_version=v1
    model_format=graph_def
    
    [one-optimize]
    input_path=inception_v3.circle
    output_path=inception_v3.opt.circle
    generate_profile_data=False
    
    [one-pack]
    input_path=inception_v3.opt.circle
    output_path=inception_v3_pack
    ```

    

### Dockerfile 생성 및 컨테이너 구동 

Docker image 생성을 위해 Dockerfile을 작성합니다. 

`ubuntu:18.04` image를 사용했으며, 현재 최신 릴리즈 버전인 1.21.0 debian package를 사용해 `onecc`를 실행하고자 했습니다. 

Docker image를 생성하고, local 경로와 docker container 내부 경로를 mount 했습니다.

성공적으로 container가 구동된다면, circle file이 생성될 것이며 컨테이너는 종료 후 삭제될 것입니다. 

- 나의 도커 버전

    ```
    $ docker -v
    Docker version 20.10.17, build 100c701
    ```

    

- Dockerfile 

    ```
    FROM ubuntu:18.04
    
    RUN apt-get update
    
    RUN apt-get install -y sudo 
    
    RUN apt-get install -y wget
    
    RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb
    
    RUN sudo apt install -y ./one-compiler_1.21.0_amd64.deb
    
    WORKDIR /home/
    
    RUN mkdir test
    
    WORKDIR /home/test 
    
    CMD ["onecc", "-C", "onecc.template.cfg"]
    ```

    - 내가 CMD에 넣은 구문 테스트용으로 작성하였으며, 은 User가 커맨드 라인에 입력한 Configure File로 대체할 예정입니다.

- create docker image

    ```
    $ docker build -t test:1 .
    ```

- docker container 실행 

    ```
    $ docker run --rm --name test_docker -v /home/test:/home/test test:1
    ```

    - local 경로는 user의 TensorFlow model이 있는 경로로 대체할 예정입니다.

### 실행 결과 

이것은 나의 실행 결과입니다. circle file 및 nnpackage가 잘 생성되었고, 현재까지 나의 방식에 특별한 문제가 없다고 생각이 듭니다. 

도커 컨테이너 또한 성공적으로 제거되었습니다. 

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



## Todo

나는 해당 방식이 괜찮다면, Shell Script로  `onecc-docker`(가제)를 작성해 만약 user가 `onecc-docker`를 실행하면,  위 과정이 수행되게 하고 싶습니다. 

나아가, 유저가 원하는 결과를 얻게 하기 위해 debian package의 버전을 선택하게 할 것입니다.

물론 현재 나의 방식이 완벽하다는 것은 아니며, `onecc`의 다양한 옵션(`-O`, `-W` ...)에 따라, 추가적인 수정이 많이 필요하다고 생각합니다. 

의견을 남겨주시면 고맙겠습니다. 



추가로, 제 linux를 기준으로 Docker image 생성(`one-compiler_1.21.0_amd64.deb` 사용)에 약 10분정도 소요되었습니다. image를 만드는 속도가 적절한지도 묻고싶네요. 





