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

>  _check_subtool_exists()

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

> subtool_keys 구문 

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

> if len(sys.argv) > 1 and sys.argv[1] in subtool_keys 이하 구문 

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

- sys.argv 

    - 사용자가 입력한 인자 중 python 이후 cmd에 입력된 인자값들을 띄어쓰기 단위로 리스트로 묶어 출력하는 것 

    - 현재 레포 형태에서는 어떤 값을 주고, 어떤 값을 출력할지 모르겠음

        ```
        $ python one-cmds/onecc.py hello world
        ['one-cmds/onecc.py', 'hello', 'world']
        ```

> _call_driver

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

> \_utils._run

```python
#utils.py
def _run(cmd, err_prefix=None, logfile=None):
    """Execute command in subprocess

    Args:
        cmd: command to be executed in subprocess
        err_prefix: prefix to be put before every stderr lines
        logfile: file stream to which both of stdout and stderr lines will be written
    """
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



## onecc 실행 

1. 가상환경 설치

    ```
    $ cd one/compiler/one-cmds/
    ~/one/compiler/one-cmds$ onecc
    ```

2. 가상환경 설치

    ```
    $ sudo apt-get update
    $ sudo apt-get upgrade
    $ sudo apt-get install python3.8 python3-pip python3.8-venv
    
    $ one-prepare-venv
    ```

    

3. onecc 실행

    ```
    onecc -v
    onecc version 1.21.0
    Copyright (c) 2020-2022 Samsung Electronics Co., Ltd. All Rights Reserved
    Licensed under the Apache License, Version 2.0
    https://github.com/Samsung/ONE
    ```

3. 
