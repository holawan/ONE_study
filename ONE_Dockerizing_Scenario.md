[toc]

[@mhs4670go](https://github.com/mhs4670go)
Thank you for your comments.
I am attaching the scenario we planned. I don't know if the format you wanted is correct, but if you give me your opinion, I will revise it and upload it again. Thank you!

# ONE_Dockerizing_Scenario

## User Scenario

### Who?

- Users who cannot or do not want to use Linux OS (Ubuntu 18.04 or Ubuntu 20.04)
- Users who want to convert the TensorFlow model to Circle file using ONE

### What 

- Convert to TensorFlow model Circlefile using 'one-cmds' regardless of operating system

### When?

- Available when the TensorFlow Model file is ready to run `onecc` and when the `onecc` related Configure file is ready.

### Where?

- User's operating system

### Why?

- Currently, `onecc` and `one-build` are only available in Ubuntu 18.04 and Ubuntu 20.04, but this is to make the service available even if it is not in that environment.

### How 

1. Create a '*.cfg' containing the option you want to perform related to the TensorFlow Model file(`.pb`, `.tfilte` ..) and `onecc`

2. Execute `onec-docker` command

    - ex

        ```
        $ onecc-docker -C *.cfg
        $ onecc-docker -W *.workflow.json
        $ onecc-docekr -C *.cfg -O *.cfg
        ```

3. Select the `one-compiler` version 

4. Run Docker Container

    - When Docker Image is not present

        - Automatically create the docker image version that you want.

        - Run Docker Container


    - When Docker Image is present
        - Run the container with the desired version of Docker Image by the user


5. Create circle files and `nnpackages` with `*.cfg` and TensorFlow models shared as volumes inside the Docker container

## User Interface

###  `-v` , `--version`

- Run 'onecc-docker'

```
$ onecc-docker -v 
onecc-docker version 0.00.0
Copyright (c) 2020-2022 Samsung Electronics Co., Ltd. All Rights Reserved
Licensed under the Apache License, Version 2.0
https://github.com/Samsung/ONE
```

### `-h`, `--help`

- Run 'onecc-docker'

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

###  `-C`

- TensorFlow Model file and 'onec' related '*.cfg' preparation

```
$ tree
.
├── inception_v3.pb
├── inception_v3.tflite
├── inception_v3_2018_04_27.tgz
├── labels.txt
└── onecc.template.cfg
```

- Run 'onecc-docker'

```
$ onecc-docker -C *.cfg
```

- Execution Results

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