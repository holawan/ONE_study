# [one-cmds] Introduce ONE Dockerizing

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

- Create a `*.cfg` and TensorFlow Model file(`.pb`, `.tfilte` ..) containing the option you want to perform related to the "onecc"
- The user runs the `onecc-docker`. (including the flag desired by the user)
    - `onecc-docker -C *.cfg`
- The user will get the desired result. Below is an example.
    - version
    - circlefile,nnpackages
    - help message

### TODO

We will first run Docker-related tasks to run "onecc-docker". Because this requires a Dockerfile to create a Docker Image, we will create it.
Second, we're going to write an "onecc-docker" shell script and run Docker on the system.
Finally, we would like to provide Debian Package with "onecc-docker".

I have summarized and will update what I need for this work below.

- 

     

    Create Dockerfile

    -  

        Make Docker container run successful with commands entered by the user

        -  `-I,` `-C`, `-O`,..

- 

     

    Create onec-docker shell script

    -  Check for `docker` installation script
    -  Check for `python3` installation script
    -  Check for `onecc` installation script
    -  run docker if docker image exists, and create a script to build if not.

-  Create `onecc-docker` Debian Package

related issue : [#8232](https://github.com/Samsung/ONE/issues/8232)

/cc [@Samsung/ootpg](https://github.com/orgs/Samsung/teams/ootpg)