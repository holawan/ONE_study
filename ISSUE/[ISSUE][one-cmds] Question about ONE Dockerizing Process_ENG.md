#8232

## why

Regarding #8232 issue, we are going to do Dockerizing so that more users can easily use `one-cmds`.

I would like to ask for a view on the way in which I carry out.

## how

I currently proceeded with Dockerizing in the following way.

### summary

1. Import TensorFlow Model for Dockerizing and write Configure File.
2. Write a Dockerfile to create a Docker image and run the container.
    - When `onecc` is finished running, the container is terminated and deleted.
3. Check that circle file and nnpackage have been created.



### Import Tensorflow model for testing

First, I created the '/home/test/' path of my Linux (wsl), downloaded the model file to be tested[inception_v3](https://storage.googleapis.com/download.tensorflow.org/models/tflite/ After downloading model_zoo/upload_20180427/inception_v3_2018_04_27.tgz),  and created the Configure file.

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



### Create Dockerfile and run container

Write Dockerfile to create Docker image.

I used `ubuntu:18.04` image and wanted to run `onecc`using the current latest release version of `1.21.0` Debian package.

You created a Docker image and mounted the local path and the internal path of the Docker container.

If the container is successfully run, a circle file will be created and the container will be deleted after shutdown.

- docker version

    ```
    $ docker -v
    Docker version 20.10.17, build 100c701
    ```

    

- Dockerfile

    ```dockerfile
    FROM ubuntu:18.04
    
    RUN apt-get update
    
    RUN apt-get install -y sudo
    
    RUN apt-get install -y wget
    
    RUN wget https://github.com/Samsung/ONE/releases/download/1.21.0/one-compiler_1.21.0_amd64.deb
    
    RUN sudo apt install -y ./one-compiler_1.21.0_amd64.deb
    
    WORKDIR /home/
    
    RUN mkdir test
    
    WORKDIR /home/test
    
    CMD["onecc", "-C", "onecc.template.cfg"]
    ```

    - I wrote it for the syntax test that I put in the CMD, and will replace it with the Configure File that the user entered in the command line.

- create docker image

    ```
    $ docker build -t test:1 .
    ```

- Run docker container

    ```
    $ docker run --rm --name test_docker -v /home/test:/home/test test:1
    ```

    - The local path will be replaced by the path where the user's TensorFlow model is located.



## Todo

If the method is ok, I would like to write `onecc-docker` (working title) as a shell script so that if the user runs `onecc-docker`, the above process will be executed.

Furthermore, The user can also select a version of the Debian package for the desired results.

Of course, my current method is not perfect, and depending on the various options of `onecc` (`-O`, `-W` ...), I think a lot of additional modifications are needed.

I'd appreciate it if you could leave a comment.



Additionally, based on my linux, it took about 10 minutes to create a Docker image (using `one-compiler_1.21.0_amd64.deb`). I want to ask if the speed of creating an image is appropriate.