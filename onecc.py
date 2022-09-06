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
    #실행 
    _utils._run(cmd)



def _check_subtool_exists():
    """verify given arguments"""
    #subtool_list의 value들을 순회하며 value들의 key 값을 subtool_keys에 추가 
    subtool_keys = [n for k, v in subtool_list.items() for n in v.keys()]
    #출력된 리스트의 길이가 1보다 크고, 1번째(zero-base) 값이 subtool_keys리스트에 있을 때  
    if len(sys.argv) > 1 and sys.argv[1] in subtool_keys:
        #dirver_name을 one-import 형식으로 변환 
        driver_name = 'one-' + sys.argv[1]
        #나머지 인자들은 옵션 
        options = sys.argv[2:]
        #_calldriver 호출 
        _call_driver(driver_name, options)
        #프로세스 종료 
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
    #argument에 version이 있으면 버젼 출력 후 종료 
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
    print(123)
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
