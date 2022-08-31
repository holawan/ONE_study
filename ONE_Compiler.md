# ONE Compiler

## One compiler build 

### 1. 필요 패키지 설치 

- https://github.com/Samsung/ONE/blob/master/docs/howto/how-to-build-compiler.md

- 빌드에 필요한 CMake, libboost-all-dev 설치

    ```
    sudo apt-get update
    sudo apt-get install cmake libboost-all-dev
    ```

- 리눅스 시스템에 기본 개발 구성이 없으므로 추가 패키지 설치

    ```
    $ sudo apt-get install build-essential 
    $ sudo apt-get install clang-format-8 
    $ sudo apt-get install cmake 
    $ sudo apt-get install doxygen 
    $ sudo apt-get install git 
    $ sudo apt-get install hdf5-tools 
    $ sudo apt-get install lcov 
    $ sudo apt-get install libatlas-base-dev
    $ sudo apt-get install libboost-all-dev
    $ sudo apt-get install libgflags-dev 
    $ sudo apt-get install libgoogle-glog-dev \
    $ sudo apt-get install libgtest-dev \
    $ sudo apt-get install libhdf5-dev \
    $ sudo apt-get install libprotobuf-dev \
    $ sudo apt-get install protobuf-compiler \
    $ sudo apt-get install pylint \
    $ sudo apt-get install python3 \
    $ sudo apt-get install python3-pip \
    $ sudo apt-get install python3-venv \
    $ sudo apt install python3.8 python3.8-venv python3-venv python3-distutils
    $ sudo apt-get install scons \
    $ sudo apt-get install software-properties-common \
    $ sudo apt-get install unzip \
    $ sudo apt-get install wget
    
    $ mkdir /tmp/gtest
    $ cd /tmp/gtest
    $ cmake /usr/src/gtest
    $ make
    $ sudo mv *.a /usr/lib
    
    $ pip3 install yapf==0.22.0 numpy
    ```
    
    

### 2. One configure

- clone 위해 기존 경로로 이동하기 

- one repository clone

    ```
    $ git clone https://github.com/Samsung/ONE.git one
    $ cd one
    $ ./nncc configure
    $ ./nncc build
    ```

    

#### ./nncc configure 과정에서 에러 발생 

```
-- Found GTest: true
-- Configure CIRCLE-OPERATOR-TEST - Done
-- Configure LUCI-PASS-VALUE-TEST
CMake Error at /home/wan/one/compiler/luci-pass-value-test/CMakeLists.txt:8 (get_target_property):
  get_target_property() called with non-existent target "testDataGenerator".


-- Configure LUCI-PASS-VALUE-TEST - Done
-- Configuring incomplete, errors occurred!
See also "/home/wan/one/build/CMakeFiles/CMakeOutput.log".
See also "/home/wan/one/build/CMakeFiles/CMakeError.log".
```

- 에러로그 

    ```
    Determining if the pthread_create exist failed with the following output:
    Change Dir: /home/wan/one/build/CMakeFiles/CMakeTmp
    
    Run Build Command:"/usr/bin/make" "cmTC_38394/fast"
    /usr/bin/make -f CMakeFiles/cmTC_38394.dir/build.make CMakeFiles/cmTC_38394.dir/build
    make[1]: Entering directory '/home/wan/one/build/CMakeFiles/CMakeTmp'
    Building C object CMakeFiles/cmTC_38394.dir/CheckSymbolExists.c.o
    /usr/bin/cc    -o CMakeFiles/cmTC_38394.dir/CheckSymbolExists.c.o   -c /home/wan/one/build/CMakeFiles/CMakeTmp/CheckSymbolExists.c
    Linking C executable cmTC_38394
    /usr/bin/cmake -E cmake_link_script CMakeFiles/cmTC_38394.dir/link.txt --verbose=1
    /usr/bin/cc      -rdynamic CMakeFiles/cmTC_38394.dir/CheckSymbolExists.c.o  -o cmTC_38394 
    CMakeFiles/cmTC_38394.dir/CheckSymbolExists.c.o: In function `main':
    CheckSymbolExists.c:(.text+0x1b): undefined reference to `pthread_create'
    collect2: error: ld returned 1 exit status
    CMakeFiles/cmTC_38394.dir/build.make:97: recipe for target 'cmTC_38394' failed
    make[1]: *** [cmTC_38394] Error 1
    make[1]: Leaving directory '/home/wan/one/build/CMakeFiles/CMakeTmp'
    Makefile:126: recipe for target 'cmTC_38394/fast' failed
    make: *** [cmTC_38394/fast] Error 2
    
    File /home/wan/one/build/CMakeFiles/CMakeTmp/CheckSymbolExists.c:
    /* */
    #include <pthread.h>
    
    int main(int argc, char** argv)
    {
      (void)argv;
    #ifndef pthread_create
      return ((int*)(&pthread_create))[argc];
    #else
      (void)argc;
      return 0;
    #endif
    }
    
    ```

#### 해결

https://github.com/Samsung/ONE/pull/9429#issuecomment-1184214714

- `cmake 3.16.2`사용 

- 현재 Python 버전이` 3.6.9`인데, Tensorflow2.8 이용을 위한 명시적`python 3.8`을 사용 

##### Cmake update

- 다운로드

    ```
    sudo mkdir cmake
    cd cmake
    sudo wget https://cmake.org/files/v3.16/cmake-3.16.2.tar.gz
    ```

- 압축풀기 및 설치

    ```
    sudo tar -xvzf cmake-3.16.2.tar.gz
    cd cmake-3.16.2/
    sudo ./bootstrap --prefix=/usr/local
    
    sudo make
    sudo make install
    ```

- OPEN SSL 설치

    - Cmake install 중, OPEN SSL 에러 발생해, OPEN SSL 설치 

        ```
        sudo wget https://www.openssl.org/source/openssl-1.1.1q.tar.gz
        
        tar xvfz openssl-1.1.1q.tar.gz 
        
        cd openssl-1.1.1q/
        
        ./config shared
        
        make
        
        sudo make install
        ```

##### Python Error FIX

- ISSUE에 명시된 대로 버전 확인을 위한 CMakelists 수정 

```
wan@one:~/one/compiler/common-artifacts$ cat CMakeLists.txt 
#[[ Generate common python virtual enviornment ]]
find_package(PythonInterp 3.8 QUIET)
find_package(PythonLibs 3.8 QUIET)

+
+find_package(PythonInterp 3 QUIET)
+find_package(PythonLibs 3 QUIET)
+
+message(STATUS "!!!! PYTHONINTERP_FOUND=${PYTHONINTERP_FOUND}")
+message(STATUS "!!!! PYTHON_VERSION_MINOR=${PYTHON_VERSION_MINOR}")
+message(STATUS "!!!! PYTHON_VERSION_MAJOR=${PYTHON_VERSION_MAJOR}")
+message(STATUS "!!!! PYTHON_EXECUTABLE=${PYTHON_EXECUTABLE}")
+message(STATUS "!!!! PYTHON_VERSION_MINOR=${PYTHON_VERSION_MINOR}")
```



- python3.8 설치 했으나, 버전이 3.6으로 나옴

```
-- Configure CIRCLE-EVAL-DIFF - Done
-- Configure COMMON-ARTIFACTS
-- !!!! PYTHONINTERP_FOUND=FALSE
-- !!!! PYTHON_VERSION_MINOR=6
-- !!!! PYTHON_VERSION_MAJOR=3
-- !!!! PYTHON_EXECUTABLE=/usr/bin/python3
-- !!!! PYTHON_VERSION_MINOR=6
-- Build common-artifacts: FALSE (Python3 is missing)
```



- python 우선순위를 3.8로 변경

    - python 3.8 재설치

        ```
        $ sudo apt install python3.8
        ```

    - python 우선순위 설정 확인

        ```
        $ sudo update-alternatives --config python
        
        update-alternatives: error: no alternatives for python
        ```

        - 우선순위가 없다고 나옴 

    - python 3.8을 우선순위로 설정

        ```
        $ sudo update-alternatives --install /usr/bin/python3 python /usr/bin/python3.8 1
        ```
    
    - ubuntu 기본 python을 python 3.8로 설정 
    
        ```
        $ sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
        $ sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 2
        ```
    
        



**configure 성공 !** 



### One build



https://stackoverflow.com/questions/65359015/trying-to-update-python-3-9-giving-errors



https://devlog.jwgo.kr/2020/02/29/broken-pip-error/

```
 sudo ln -Tfs python3.8 python3
```

https://github.com/Samsung/ONE/issues/8800



#### Test 실패

```
The following tests FAILED:
         96 - record_minmax_conversion_test (Failed)
        102 - luci_value_test (Failed)
        103 - luci_value_tol_test (Failed)
        107 - circle_part_value_test (Failed)
        109 - luci_pass_value_test (Failed)
Errors while running CTest
```

