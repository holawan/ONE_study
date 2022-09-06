[toc]

# ONECC

## onecc 파일 구조

```python
#onecc
#!/usr/bin/env bash
''''export SCRIPT_PATH="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)" # '''
''''export PY_PATH=${SCRIPT_PATH}/venv/bin/python                                       # '''
''''test -f ${PY_PATH} && exec ${PY_PATH} "$0" "$@"                                     # '''
''''echo "Error: Virtual environment not found. Please run 'one-prepare-venv' command." # '''
''''exit 255                                                                            # '''

# Copyright (c) 2021 Samsung Electronics Co., Ltd. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import configparser
import os
import subprocess
import sys

from onelib.CfgRunner import CfgRunner
from onelib.WorkflowRunner import WorkflowRunner
import utils as _utils

# TODO Find better way to suppress trackback on error
sys.tracebacklimit = 0

subtool_list = {
    'compile': {
        'import': 'Convert given model to circle',
        'optimize': 'Optimize circle model',
        'quantize': 'Quantize circle model',
    },
    'package': {
        'pack': 'Package circle and metadata into nnpackage',
    },
    'backend': {
        'codegen': 'Code generation tool',
        'profile': 'Profile backend model file',
        'infer': 'Infer backend model file'
    },
}


def _call_driver(driver_name, options):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    driver_path = os.path.join(dir_path, driver_name)
    cmd = [driver_path] + options
    _utils._run(cmd)


def _check_subtool_exists():
    """verify given arguments"""
    subtool_keys = [n for k, v in subtool_list.items() for n in v.keys()]
    if len(sys.argv) > 1 and sys.argv[1] in subtool_keys:
        driver_name = 'one-' + sys.argv[1]
        options = sys.argv[2:]
        _call_driver(driver_name, options)
        sys.exit(0)


def _get_parser():
    onecc_usage = 'onecc [-h] [-v] [-C CONFIG] [-W WORKFLOW] [-O OPTIMIZATION] [COMMAND <args>]'
    onecc_desc = 'Run ONE driver via several commands or configuration file'
    parser = argparse.ArgumentParser(description=onecc_desc, usage=onecc_usage)

    _utils._add_default_arg(parser)

    opt_name_list = _utils._get_optimization_list(get_name=True)
    opt_name_list = ['-' + s for s in opt_name_list]
    if not opt_name_list:
        opt_help_message = '(No available optimization options)'
    else:
        opt_help_message = '(Available optimization options: ' + ', '.join(
            opt_name_list) + ')'
    opt_help_message = 'optimization name to use ' + opt_help_message
    parser.add_argument('-O', type=str, metavar='OPTIMIZATION', help=opt_help_message)

    parser.add_argument(
        '-W', '--workflow', type=str, metavar='WORKFLOW', help='run with workflow file')

    # just for help message
    compile_group = parser.add_argument_group('compile to circle model')
    for tool, desc in subtool_list['compile'].items():
        compile_group.add_argument(tool, action='store_true', help=desc)

    package_group = parser.add_argument_group('package circle model')
    for tool, desc in subtool_list['package'].items():
        package_group.add_argument(tool, action='store_true', help=desc)

    backend_group = parser.add_argument_group('run backend tools')
    for tool, desc in subtool_list['backend'].items():
        backend_group.add_argument(tool, action='store_true', help=desc)

    return parser


def _parse_arg(parser):
    args = parser.parse_args()
    # print version
    if args.version:
        _utils._print_version_and_exit(__file__)

    return args


def _verify_arg(parser, args):
    """verify given arguments"""
    # check if required arguments is given
    if not _utils._is_valid_attr(args, 'config') and not _utils._is_valid_attr(
            args, 'workflow'):
        parser.error('-C/--config or -W/--workflow argument is required')
    # check if given optimization option exists
    opt_name_list = _utils._get_optimization_list(get_name=True)
    opt_name_list = [_utils._remove_prefix(s, 'O') for s in opt_name_list]
    if _utils._is_valid_attr(args, 'O'):
        if ' ' in getattr(args, 'O'):
            parser.error('Not allowed to have space in the optimization name')
        if not getattr(args, 'O') in opt_name_list:
            parser.error('Invalid optimization option')


def main():
    # check if there is subtool argument
    # if true, it executes subtool with argv
    # NOTE:
    # Why call subtool directly without using Argparse?
    # Because if Argparse is used, options equivalent to onecc including
    # '--help', '-C' are processed directly onecc itself.
    # So options cannot be delivered to subtool.
    _check_subtool_exists()

    # parse arguments
    # since the configuration file path is required first,
    # parsing of the configuration file proceeds after this.
    parser = _get_parser()
    args = _parse_arg(parser)

    # verify arguments
    _verify_arg(parser, args)

    bin_dir = os.path.dirname(os.path.realpath(__file__))
    if _utils._is_valid_attr(args, 'config'):
        runner = CfgRunner(args.config)
        runner.detect_import_drivers(bin_dir)
        if _utils._is_valid_attr(args, 'O'):
            runner.add_opt(getattr(args, 'O'))
        runner.run(bin_dir)
    elif _utils._is_valid_attr(args, 'workflow'):
        runner = WorkflowRunner(args.workflow)
        runner.run(bin_dir)


if __name__ == '__main__':
    _utils._safemain(main, __file__)

```

### _check_subtool_exists()

```python
#onecc
subtool_list = {
    'compile': {
        'import': 'Convert given model to circle',
        'optimize': 'Optimize circle model',
        'quantize': 'Quantize circle model',
    },
    'package': {
        'pack': 'Package circle and metadata into nnpackage',
    },
    'backend': {
        'codegen': 'Code generation tool',
        'profile': 'Profile backend model file',
        'infer': 'Infer backend model file'
    },
}

def _check_subtool_exists():
    """verify given arguments"""
    #
    subtool_keys = [n for k, v in subtool_list.items() for n in v.keys()]
    if len(sys.argv) > 1 and sys.argv[1] in subtool_keys:
        driver_name = 'one-' + sys.argv[1]
        options = sys.argv[2:]
        _call_driver(driver_name, options)
        sys.exit(0)
```

#### subtool_keys 구문 

- #1과 #2의 동작 방식은 같다. 

```python
#1
subtool_keys = [n for k, v in subtool_list.items() for n in v.keys()]

print(subtool_keys)
#2 
subtool_keys = []

##subtool_list의 key와 value를 순회하며
### key: compile, 
'''
value
 'import': 'Convert given model to circle',
 'optimize': 'Optimize circle model',
 'quantize': 'Quantize circle model',
'''
for k,v in subtool_list.items() :
    
    ##value들의 key를 순회하며 
    ### value들의 key : import,optimize, quantize 
    for n in v.keys() :
        
        #해당 값들 리스트에 추가 
        subtool_keys.append(n)

print(subtool_keys)
#['import', 'optimize', 'quantize', 'pack', 'codegen', 'profile', 'infer']
```

#### if len(sys.argv) > 1 and sys.argv[1] in subtool_keys 이하 구문 

```python
    #출력된 리스트의 길이가 1보다 크고, 1번째(zero-base) 값이 subtool_keys리스트에 있을 때  
    if len(sys.argv) > 1 and sys.argv[1] in subtool_keys:
        
        #driver_name은 예를 들어,sys.argv가 ['onecc', 'import']이고, sys.argv[1]이 import일 경우 'one-import' 형태 
        driver_name = 'one-' + sys.argv[1]
        
        #나머지 리스트의 값들은 옵션 
        options = sys.argv[2:]
       
    	#driver_name과 options를 인자로 _call_driver 호출 
        _call_driver(driver_name, options)
        #subtool_keys가 입력에 존재할 때, _call_driver를 호출 후 해당 compile 종료
        sys.exit(0)
```

##### sys.argv 

- 사용자가 입력한 인자 중 python 이후 cmd에 입력된 인자값들을 띄어쓰기 단위로 리스트로 묶어 출력하는 것 

    ```
    $ onecc import tflite -i inception_v3.tflite -o inception_v3_import.circle
    ['one-cmds/onecc.py', 'hello', 'world']
    ```

#### 정리

- 입력된 커맨드의 1번째 요소에 import, optimize 등 subtool_list에 있는 인자일 때, 해당 인자에 `one-`를 붙이고, 나머지 값들은 option으로 `_call_driver` 함수를 실행 
- 실행 후 compile 종료  

### _call_driver

```python
#onecc
def _call_driver(driver_name, options):
    
    #dir_path는 cmd를 실행할 .local/bin
    ## /home/holawan/.local/bin
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    #현재 디렉토리 하위에 driver_name 명령을 변수로 선언 
    ## import가 sys.argv의 1번 인자였다면, one-import 경로 생성
    ## /home/holawan/.local/bin/one-import
    driver_path = os.path.join(dir_path, driver_name)
    
    #cmd는 driver_path에, option 추가 
    ## driver_name이 import이고, 옵션이 ['tflite', '-i', 'inception_v3.tflite', '-o', 'inception_v3_import.circle'] 다음과 같다면  
    ## cmd는 해당 명령 
    ### ['/home/holawan/.local/bin/one-import', 'tflite', '-i', 'inception_v3.tflite', '-o', 'inception_v3_import.circle']
    cmd = [driver_path] + options
    _utils._run(cmd)

```

#### 정리

- `~/.local/bin` 경로에서,  입력된 커맨드에 따른 명령을 실행

    - ex)

        ```
        onecc import tflite -i inception_v3.tflite -o inception_v3_import.circle
        ```

        - 해당 명령이 있을 때, 1번자가 import로, subtool_keys에 있어서 `if len(sys.argv) > 1 and sys.argv[1] in subtool_keys` 이하 구문 으로 들어옴. 
        - 그렇다면, `_call_driver`를 호출해 , 해당 커맨드를 실행하고, 종료됨 

#### \_utils._run

```python
#utils.py
import argparse
import configparser
import glob
import importlib
import ntpath
import os
import subprocess
import sys

def _run(cmd, err_prefix=None, logfile=None):
    """Execute command in subprocess
		하위 프로레스에 명령 실행 
    Args:
        cmd: command to be executed in subprocess
        cmd : 하위 프로세스에 실행할 명령 
        err_prefix: prefix to be put before every stderr lines
        err_prefix : 모든 stderr 행 앞에 붙이는 접두사 
        logfile: file stream to which both of stdout and stderr lines will be written
        logfile : stdout 및 stderr 행이 모두 기록될 파일 스트림 
    """
    #cmd를 인자로 받고, stdout과 stderr을 PIPE에서 가져옴 
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        import select
        inputs = set([p.stdout, p.stderr])
        while inputs:
            readable, _, _ = select.select(inputs, [], [])
            for x in readable:
                line = x.readline()
                if len(line) == 0:
                    inputs.discard(x)
                    continue
                if x == p.stdout:
                    out = sys.stdout
                if x == p.stderr:
                    out = sys.stderr
                    if err_prefix:
                        line = f"{err_prefix}: ".encode() + line
                out.buffer.write(line)
                out.buffer.flush()
                if logfile != None:
                    logfile.write(line)
    if p.returncode != 0:
        sys.exit(p.returncode)
```

##### with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:

https://soooprmx.com/python-subprocess-1/

- subsprocess는 파이썬 스크립트에서 쉘 명령 등 다른 프로세스를 실행하고 출력 결과를 가져올 수 있게 하는 라이브러리로, subprocess 모듈은 os.system, os.spawn* 등을 대체하기 위해 만들어진 모듈이다. 

- Subprocess

    - 서브 프로세스는 외부 운영체제 명령을 실행할 때 사용되는 프로세스이며, 나중에 출력을 조작해 서브 프로세스 모드에서 새 명령을 생성할 수 있도록 함 

    - 프로세스는 stdin, stdout, stderr를 PIPE option에 입력하고, 작성된 코드를 반환함 

        - ex) `df-h`를 실행하면 사용된 마운트의 크기를 반환하는데, 이를 subproecess로 작성하면

            ```python
            cmd = "df -h"
            subprocess.Popen(cmd, shell=True)
            ```

            - out

                ```bash
                $ python utils.py 
                Filesystem            Size  Used Avail Use% Mounted on
                C:/Program Files/Git  476G  148G  329G  31% /
                D:                    477G  113M  477G   1% /d
                ```

        - 오류인 경우 입력 

            ```python
            cmd = "df -asdasdh"
            subprocess.Popen(cmd, shell=True)
            ```

            - out

                ```bash
                $ python utils.py 
                df: unknown option -- f
                Try 'df --help' for more information.
                ```

        

- **with**

    - with 절은 자원을 획득하고, 사용하고, 반납할 때 주로 사용한다.

    - 파이썬의 컨택세트 매니저는 리소스를 `with`문법을 통해 `with`절에서만 액세스 가능헤가 하고, 블록을 나가면 리소스를 해제한다. 

    ```python
    with {expression} as {valiable} :
        block..
    ```

    - 샘플코드

        - 파일을 읽고 종료하는 코드 

            - 기존

            ```python
            f = open('myFile.txt', 'w', encoding='utf8')
            f.write('test')
            f.close 
            ```

        - with 절 사용

            ```python
            with open('mytextfile.txt', 'r', encoding='utf-8') as f: 
                f.write('test')
            ```

    

- **Popen**

    - 다양한 옵션을 통해 call(), check_output()명령어보다 훨씬 유연하게 서브프로세스를 실행하고, 결과값을 가져옴 

    - subprocess.PIPE 

        - 표준 출력 내용 또는 표준 에러로 출력된 내용

        - [`Popen`](https://docs.python.org/ko/3/library/subprocess.html#subprocess.Popen)의 *stdin*, *stdout* 또는 *stderr* 인자로 사용할 수 있고 표준 스트림에 대한 파이프를 열어야 함을 나타내는 특수 값. [`Popen.communicate()`](https://docs.python.org/ko/3/library/subprocess.html#subprocess.Popen.communicate)에서 가장 유용합니다.

            https://docs.python.org/ko/3/library/subprocess.html

        - ```python
            cmd = ["df", "-h"]
            test = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out,err = test.communicate()
            
            print(f'out: {out}')
            print(f'err :{err}')
            # 표준 출력
            out: b'Filesystem            Size  Used Avail Use% Mounted on\nC:/Program Files/Git  476G  148G  329G  32% /\nD:                    477G  113M  477G   1% /d\n'
            err :b''
            #오류
            ## cmd의 1번째 인자를 -asdf로 바꿀 때 
            out: b''
            err :b"df: unknown option -- s\nTry 'df --help' for more information.\n"
            ```


### get_parser()

```python
#onecc
def _get_parser():
    onecc_usage = 'onecc [-h] [-v] [-C CONFIG] [-W WORKFLOW] [-O OPTIMIZATION] [COMMAND <args>]'
    onecc_desc = 'Run ONE driver via several commands or configuration file'
    #설명은 onecc-=_dsec, usage=onec_usage로 parser 생성 parser instacne 
    parser = argparse.ArgumentParser(description=onecc_desc, usage=onecc_usage)
    
    #_utils에 정의된 기본 argument추가 
    ## version, verbose, config, section
    _utils._add_default_arg(parser)
	
    #~/.local/optimization/ 에 위치한 O*.cfg 파일 모두 가져오기 
    opt_name_list = _utils._get_optimization_list(get_name=True)
    opt_name_list = ['-' + s for s in opt_name_list]
    #정의된 파일이 없다면 사용가능한 옵션이 없음을 표시 
    if not opt_name_list:
        opt_help_message = '(No available optimization options)'
    #있다면 사용 가능한 옵션들 표시 
    else:
        opt_help_message = '(Available optimization options: ' + ', '.join(
            opt_name_list) + ')'
    opt_help_message = 'optimization name to use ' + opt_help_message
    #optimization 관련 argument추가 
    parser.add_argument('-O', type=str, metavar='OPTIMIZATION', help=opt_help_message)
	
    #workflow 관련 argument 추가 
    parser.add_argument(
        '-W', '--workflow', type=str, metavar='WORKFLOW', help='run with workflow file')

    # just for help message
    ## subtool_list에 있는 옵션들 argument에 추가 
    compile_group = parser.add_argument_group('compile to circle model')
    for tool, desc in subtool_list['compile'].items():
        compile_group.add_argument(tool, action='store_true', help=desc)

    package_group = parser.add_argument_group('package circle model')
    for tool, desc in subtool_list['package'].items():
        package_group.add_argument(tool, action='store_true', help=desc)

    backend_group = parser.add_argument_group('run backend tools')
    for tool, desc in subtool_list['backend'].items():
        backend_group.add_argument(tool, action='store_true', help=desc)

    return parser
```



#### argparse

- 코드가 너무 긴 관계로, 형식 설명 

- argparse 모듈은 사용자 친화적인 명령행 인터페이스를 쉽게 작성하도록 도움 
- 프로그램이 필요한 인자를 정의하면, argparse는 sys.argv를 어떻게 파싱할지 파악함
- 또한 argparse 모듈은 도움말과 사용법 메시지를 자동 생성하고, 사용자가 프로그램에 잘못된 인자를 줄 때, 에러를 발생시킴 

- **parser**는 ArgumentParser의 객체로 파일이 실행될 때, 설명 및 help 메시지를 담는 역할로 파악됨 
    - parser 객체는 명령행을 파이썬 데이터형으로 파싱하는데 필요한 모든 정보를 가지고 있음 
- parser instance를 선언하고, description이나 usage, default value를 지정
- `parser.add_argument()` method를 통해 프로그램의 인자에 대한 정보를 채움 
- `parse_args()`라는 method로 명령창에서 주어진 인자를 parsing함 

- **ArgumentParser의 인자**

    - usage : 프로그램 사용법을 설명하는 문자열 (기본값: 파서에 추가된 인자로부터 만들어지는 값 )

    - description : 인자 도움말 전에 표시할 텍스트 (기본값: none)
    - add_help : 파서에 `-h/--help` 옵션을 추가 (기본값 : none)

- **예**

    ```python
    import argparse
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')
    
    args = parser.parse_args()
    print(args.accumulate(args.integers))
    ```

    - **실행 결과 **

        ```
        $ python argparse_test.py -h
        usage: argparse_test.py [-h] [--sum] N [N ...]
        
        Process some integers.
        
        positional arguments:
          N           an integer for the accumulator
        
        optional arguments:
          -h, --help  show this help message and exit
          --sum       sum the integers (default: find the max)
        ```

        ```
        $ python argparse_test.py 
        usage: argparse_test.py [-h] [--sum] N [N ...]
        argparse_test.py: error: the following arguments are required: N
        ```

        

#### -get_optimization_list(get_name=False)

```python
def _get_optimization_list(get_name=False):
    """
    returns a list of optimization. If `get_name` is True,
    only basename without extension is returned rather than full file path.

    [one hierarchy]
    one
    ├── backends
    ├── bin
    ├── doc
    ├── include
    ├── lib
    ├── optimization
    └── test

    Optimization options must be placed in `optimization` folder
    """
    #dir_path: ~/.local/bin
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # optimization folder
    #optimization/O*cfg 파일을 모두 files에 담음 
    files = [f for f in glob.glob(dir_path + '/../optimization/O*.cfg', recursive=True)]

    # exclude if the name has space
    #파일명에 공백이 있으면 제거 
    files = [s for s in files if not ' ' in s]
	
    #optimization lsit 
    opt_list = []
    for cand in files:
        base = ntpath.basename(cand)
        if os.path.isfile(cand) and os.access(cand, os.R_OK):
            opt_list.append(cand)

    if get_name == True:
        # NOTE the name includes prefix 'O'
        # e.g. O1, O2, ONCHW not just 1, 2, NCHW
        opt_list = [ntpath.basename(f) for f in opt_list]
        opt_list = [_remove_suffix(s, '.cfg') for s in opt_list]

    return opt_list
```

- ~/.local/optimization 폴더 하위 모든 O*.cfg 파일을 가져와서 리스트에 추가
- 상위 root 제거 후 파일 이름만 리스트에 저장 
- .cfg 제거 후 파일 명만 리스트에 저장 
- 해당 리스트 리턴 
- 리턴된 리스트는 `_get_parser()` 아래 opt_name_list의 출력값으로 parsing 결과에 사용가능한 Optimization으로 표시됨 



### _verify_arg(parser,args) 

```python
def _verify_arg(parser, args):
    """verify given arguments"""
    # check if required arguments is given
    
    #만약 config 커맨드나 workflow 커맨드가 없다면 에러 리턴 
    if not _utils._is_valid_attr(args, 'config') and not _utils._is_valid_attr(
            args, 'workflow'):
        parser.error('-C/--config or -W/--workflow argument is required')
    # check if given optimization option exists
    #optimization 파일들의 유효성 검사 
    opt_name_list = _utils._get_optimization_list(get_name=True)
    opt_name_list = [_utils._remove_prefix(s, 'O') for s in opt_name_list]
    if _utils._is_valid_attr(args, 'O'):
        if ' ' in getattr(args, 'O'):
            parser.error('Not allowed to have space in the optimization name')
        if not getattr(args, 'O') in opt_name_list:
            parser.error('Invalid optimization option')
```

- argument 유효성 검사 
    - 커맨드에 config나 workflow가 없다면 
