[toc]

# one-cmds -O 

https://github.com/Samsung/ONE/issues/7513

https://github.com/Samsung/ONE/issues/5784

https://github.com/Samsung/ONE/pull/7868

## 개요

- one-cmds의 one-build나 onecc 과정에서는 수많은 optimization 옵션이 있다. 
- ONE 프로젝트에서는 optimization 옵션을 configure 파일에 일일이 작성하여, onecc나 one-build를 진행하게 되는데, **이를 목적에 맞게 미리 세트로 구성해놓은 후, -O 옵션으로 적용할 수 있도록 한 것이 -O 옵션이다.**

## 실행 구조

### _get_parser()

```python
#onecc
def _get_parser():
    onecc_usage = 'onecc [-h] [-v] [-C CONFIG] [-W WORKFLOW] [-O OPTIMIZATION] [COMMAND <args>]'
    onecc_desc = 'Run ONE driver via several commands or configuration file'
    parser = argparse.ArgumentParser(description=onecc_desc, usage=onecc_usage)
    print(f'parser: {parser}')
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

```

### _get_optimization_list()

```python
#utils.py
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
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    # optimization folder
    files = [f for f in glob.glob(dir_path + '/../optimization/O*.cfg', recursive=True)]
    print(dir_path + '/../optimization/O*.cfg')
    # exclude if the name has space
    files = [s for s in files if not ' ' in s]

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

- onecc 파일은 입력된 command를 대상으로 _get_parser 함수를 실행하는데, 해당 과정에서, command에 `-O` 이하의 입력에 대해 파일이 `~/.local/optimization/O*.cfg`에 존재하면 해당 configure 파일을 현재 compile optimizer에 적용한다. 

## 파일 생성 및 커맨드 실행

### cfg 생성

- 원하는 optimizer를 담은 configure 파일을 `~/.local/optimization` 아래에 `O*.cfg `형태 이름으로 생성한다.

    ```
    ~/.local/optimization$ tree
    .
    └── O1.cfg
    
    ~/.local/optimization$ cat O1.cfg 
    [one-optimize]
    convert_nchw_to_nhwc=True
    nchw_to_nhwc_input_shape=True
    ```

### 실행 

- configure 선언 이후 cfg 파일 이름으로 command를 입력하면, one-build or cc 과정에서 해당 optimization을 수행한다. 

    ```bash
    onecc -C onecc.template.cfg -O1
    ```

    
