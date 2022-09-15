[toc]

# [one-cmds] Introduce ONE Dockerizing

## 1st

### What

Let’s introduce **`ONE Dockerizing`**.

### Why

Currently, `onecc` is only supported on Ubuntu 18.04 and 20.04 (not offially).

Therefore, it is not easy for people to use `onecc` in other environments.

Our `ONE-Dockerizing` will use `Docker` to make `onecc` easy for users to use in other environments.
The ultimate goal will be to use `onecc` with Docker on Windows, Mac, etc., but we are currently working on Linux, and our goal is to do `ONE-Dockerizing` on all Linux environments.

### Scenario
#### System Scenario
1. Receive commands entered by the user.
2. Verify that `onecc-docker` can be run in the user's environment (existence of docker, installation of python3, etc.)
3. Run Docker Container
    - When Docker Image is not present
        - Create the docker image
        - Run Docker Container
    - When Docker Image is present
    - Run the docker container by specifying the volume as '/home:/home' and by specifying the location where the current user is running as WORKDIR.
        - `docker run --rm --name {container_name} -v /home:/home --workdir {user_pwd} {docker_image} {user_command}`
4. Create `circle files` and `nnnpackage` using the `.cfg` and TensorFlow models shared as volumes inside the docker container and provide them to the user.

#### User Scenario

- Create a `*.cfg` and TensorFlow Model file(`.pb`, `.tfilte` ..)  containing the option you want to perform related to the "onecc"

- The user runs the `onecc-docker`. (including the flag desired by the user)
  - `onecc-docker -C *.cfg `

- The user will get the desired result. Below is an example.
  - version
  - circlefile,nnpackages
  - help message


### TODO

We will first run Docker-related tasks to run "onecc-docker". Because this requires a Dockerfile to create a Docker Image, we will create it. 
Second, we're going to write an "onecc-docker" shell script and run Docker on the system. 
Finally, we would like to provide Debian Package with "onecc-docker".

I have summarized and will update what I need for this work below.

- [ ] Create Dockerfile
    - [ ] Make Docker container run successful with commands entered by the user
        - [ ] `-I,` `-C`, `-O`,..
- [ ] Create onec-docker shell script
    - [ ] Check for `docker` installation script
    - [ ] Check for `python3` installation script
    - [ ] Check for `onecc` installation script
    - [ ] run docker if docker image exists, and create a script to build if not.
- [ ] Create `onecc-docker` Debian Package

related issue : #8232

/cc [@Samsung/ootpg](https://github.com/orgs/Samsung/teams/ootpg)



## 2nd

### seanshpark

About the scenario, this is not that important but I'd like to mention this;

- It would be better to separate scenario in user point of view from internal implementation
- I think user would act like
    - create cfg file like mymodel.cfg with mymodel.pb model
    - run onecc-docker -C mymodel.cfg
    - user gets mymodel.circle
- other things are done inside our system which canbe multiple of solutions

### seanshpark

About todo...

- I actually don't understand fully about internal implementation details
- I think you first do describe how you are going to make it done before listing TO DOs.

### holawan

[@seanshpark](https://github.com/seanshpark)
Thank you for your opinion. :)

> About the scenario, this is not that important but I'd like to mention this;

I will add it considering the scenario of the user's position.

> About todo...

And I will revise Todo by referring to other issues.



## 3rd

### jyoungyun

> I think you first do describe how you are going to make it done before listing TO DOs.

**The final output results**

`onecc-docker` debian package
   - This team will generate a `onecc-docker` debian package including several scripts to run `onecc` and `Dockerfile` to build a docker image.

**User scenario**

1. Install `onecc-docker` debian package
2. Run `onecc-docker` script
   1. If `one-compiler` was installed before
      - Run `onecc` through `onecc-docker` script
   2. No installed `one-compiler`
      - Build docker image that contains the `one-compiler`
      - Run `onecc` through the built docker image

Would it be helpful to understand if I put more explanations like this?

/cc @seanshpark 

### seanshpark

> Install onecc-docker debian package

Q) so the user do not or cannot install one-compiler debian package?

- like in the future, say for mac osx, if we (or someone else) provide `onecc-docker.dmg` somehow, then the user can run `onecc` inside the Docker through `onecc-docker` ?

> If one-compiler was installed before

Q) is this line `one-compiler` debian package install in native or is it through Docker image?

> No installed one-compiler

Q) Seems this is native `one-compiler` debian package. Am I right?
Q) After this, there will be `onecc` running inside Docker.
If the user installs `one-compiler` then there will be `onecc` inside Docker and in the Native
Which may be in different version. Have any plans for version mismatch?
Q) Is there any selection option to choose which `onecc`(Docker or Native) if both installed? Or just run Docker in higher priority ?
Q) Can we fix the senario that `one-docker` will ONLY run Docker image for first implementation for simplicity?



### jyoungyun

> Q) so the user do not or cannot install one-compiler debian package?

You can install `one-compiler` debian package regardless of whether `onecc-docker` debian package is installed.

> - like in the future, say for mac osx, if we (or someone else) provide `onecc-docker.dmg` somehow, then the user can run `onecc` inside the Docker through `onecc-docker` ?

Yes, that's what we're ultimately trying to do. :) (Although this SSAFY does not create a package for mac..)

> Q) is this line `one-compiler` debian package install in native or is it through Docker image?

It means that `one-compiler` debian package is installed in your file system.

> Q) Seems this is native `one-compiler` debian package. Am I right?

Yes, you're correct. :)

> Q) After this, there will be `onecc` running inside Docker.
> If the user installs `one-compiler` then there will be `onecc` inside Docker and in the Native
> Which may be in different version. Have any plans for version mismatch?

And so, we consider the version argument from `onecc-docker` script file.
For now, we don't care about the version. So if the `onecc` is installed in Native, we will use `onecc`. And if there is no installed `onecc`, we will use the latest `onecc` inside Docker image. (Because we use the latest `one-compiler` package when we build the docker image.)

Afterward, if we support the version, we will input the version number. And then if the exactly matched `one-compiler` is already installed, we will use it in Native. However if the installed version is not matched from user inputs, we will use `onecc` in docker image.
If user does not input any version number, the native `onecc` has a higher priority than `onecc` in the latest docker image.

> Q) Is there any selection option to choose which `onecc`(Docker or Native) if both installed? Or just run Docker in higher priority ?

The native `onecc` has a higher priority.

> Q) Can we fix the senario that `one-docker` will ONLY run Docker image for first implementation for simplicity?

Could you explain a little more? I can't catch your intention. :)



### seanshpark

> Could you explain a little more? I can't catch your intention. :)

by the scenario, `onecc-docker` can either run `onecc` in Native installed or the Docker version.
for the first implementation, let's just focus on running ONLY in the Docker version.
do not care if there is Native `one-compiler` package installed or not.

after this works OK and stable, we can revise to check if Native version is installed... and so one with more complicate scenarios until the time permits.



### jyoungyun

> by the scenario, `onecc-docker` can either run `onecc` in Native installed or the Docker version.
> for the first implementation, let's just focus on running ONLY in the Docker version.
> do not care if there is Native `one-compiler` package installed or not.

Oh, that's a good idea. I think this approach will be a clear and safe design.
What do you think of this?

/cc [@Samsung/ootpg](https://github.com/orgs/Samsung/teams/ootpg) [@Samsung/ootpg_docker](https://github.com/orgs/Samsung/teams/ootpg_docker)



### holawan

> Oh, that's a good idea. I think this approach will be a clear and safe design.
> What do you think of this?

I think it means that the scenario needs to be modified.

Are you saying that we should focus on running `onecc-docker` using docker without checking whether the user's native `one-compiler` is installed (version mismatch, installation, etc.)?

- When running `onecc-docker`, provide `circle file` or `nnpackages` to the user

If I understand correctly, I will attach the skeleton code and give you additional PR soon :)

Thank you for your opinion :)