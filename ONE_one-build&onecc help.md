# ONECC

## one-build/onecc help

### one-build

```
$ one-build --help
usage: one-build [-h] [-v] [-V] [-C CONFIG] [-O OPTIMIZATION]

command line tool to run ONE drivers in customized order

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -V, --verbose         output additional information to stdout or stderr
  -C CONFIG, --config CONFIG
                        run with configuation file
  -O OPTIMIZATION       optimization name to use (No available optimization options)
```

- optional argument
    - -h, --help : 도움말 메시지 표시 및 종료
    - -v, --version : 프로그램 버젼을 표시하고 종료
    - -V, --verbose : stdout혹은 stderr에 추가 정보 출력 
    - -C CONFIG, --config CONFIG : 구성파일을 사용해서 실행
    - -O OPTIMIZATION : 사용할 최적화 이름 (사용 가능한 최적화 옵션 없음 )

### onecc

```
$ onecc -h
usage: onecc [-h] [-v] [-C CONFIG] [-W WORKFLOW] [-O OPTIMIZATION] [COMMAND <args>]

Run ONE driver via several commands or configuration file

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -V, --verbose         output additional information to stdout or stderr
  -C CONFIG, --config CONFIG
                        run with configuation file
  -O OPTIMIZATION       optimization name to use (No available optimization options)
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

- optional argument
    - h, --help : 도움말 메시지 표시 및 종료
    - -v, --version : 프로그램 버젼을 표시하고 종료
    - -V, --verbose : stdout혹은 stderr에 추가 정보 출력 
    - -C CONFIG, --config CONFIG : 구성파일을 사용해서 실행
    - -O OPTIMIZATION : 사용할 최적화 이름 (사용 가능한 최적화 옵션 없음 )
    - -W WORKFLOW, --workflow WORKFLOW : workflow file 실행
- compile to circle model
    - import : 주어진 모델을 circle로 변환
    - optimize: circle model 최적화
    - quantize : circle model 양자화
- package circle model
    - pack : 패키지 써클 및 메타디에터를 nnpackage에 포함
- run backend tools
    - codgen : 코드 생성 도구
    - profile : 백엔드 모델 파일 개요
    - infer : 백엔드 모델 파일 추론 
