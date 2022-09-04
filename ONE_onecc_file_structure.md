[toc]

# ONECC

## onecc 파일 구조

```python
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
        
        #driver_name은 예를 들어,sys.argv가 ['one-cmds/onecc.py', 'import']이고, sys.argv[1]이 import일 경우 'one-import' 형태 
        driver_name = 'one-' + sys.argv[1]
        
        #나머지 리스트의 값들은 옵션 
        options = sys.argv[2:]
       
    	#driver_name과 options를 인자로 _call_driver 호출 
        _call_driver(driver_name, options)
        sys.exit(0)
```

##### sys.argv 

- 사용자가 입력한 인자 중 python 이후 cmd에 입력된 인자값들을 띄어쓰기 단위로 리스트로 묶어 출력하는 것 

- 현재 레포 형태에서는 어떤 값을 주고, 어떤 값을 출력할지 모르겠음

    ```
    $ python one-cmds/onecc.py hello world
    ['one-cmds/onecc.py', 'hello', 'world']
    ```

### _call_driver

```python
def _call_driver(driver_name, options):
    
    #dir_path는 현재 디렉토리 선언 
    ## one/compiler/one_cmds
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    #현재 디렉토리 하위에 driver_name으로 폴더 생성 
    ## import가 sys.argv의 1번 인자였다면, one-import 경로 생성
    ## one/compiler/one_cmds/one-import
    driver_path = os.path.join(dir_path, driver_name)
    
    #cmd는 driver_path에, option 추가 
    ## option이 hello라면 
    ## ["/home/holawan/one/compiler/one-cmds/one-import",'hello']
    cmd = [driver_path] + options
    _utils._run(cmd)

```

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

        - 
