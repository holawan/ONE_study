[toc]

# ONE TEST

## tests

- one/compiler/one-cmds 하위에는 test라는 폴더가 있음

    ```
    $ tree
    .
    ├── CMakeLists.txt
    ├── OONE-BUILD_014.cfg
    ├── OONECC_024.cfg
    ├── README.txt
    ├── inception_v3.circle
    ├── inception_v3.circle.log
    ├── inception_v3.opt.circle
    ├── inception_v3.opt.circle.log
    ├── inception_v3.pb
    ├── inception_v3.tflite
    ├── inception_v3_2018_04_27.tgz
    ├── labels.txt
    ...
    2 directories, 304 files
    
    ```

- 해당 파일들 test해보기 

- 파일 자동 실행(?)을 위한 python 파일 작성

    ```
    import os
    import time
    for i in range(1,15) :
        os.system(f'one-build -C one-build_00{i}.cfg')
        time.sleep(10)
        print(f'one-build -C one-build_00{i}: ','SUCCESS!')
                
    print('test clear')
    
    ```

### test 1,2 성공

```bash
$ python test.py 
WARNING:absl:Please consider providing the trackable_obj argument in the from_concrete_functions. Providing without the trackable_obj argument is deprecated and it will use the deprecated conversion path.
Estimated count of arithmetic ops: 11.460 G  ops, equivalently 5.730 G  MACs
one-build -C one-build_001:  SUCCESS!
WARNING:absl:Please consider providing the trackable_obj argument in the from_concrete_functions. Providing without the trackable_obj argument is deprecated and it will use the deprecated conversion path.
Estimated count of arithmetic ops: 11.460 G  ops, equivalently 5.730 G  MACs
model2nnpkg.sh: Generating nnpackage inception_v3.opt in inception_v3_pkg
one-build -C one-build_002:  SUCCESS!
```

### test3

- configure file 

    ```
    [one-build]
    one-import-tf=True
    one-import-tflite=False
    one-import-bcq=False
    one-optimize=False
    one-quantize=True
    one-pack=False
    one-codegen=False
    
    [one-import-tf]
    input_path=inception_v3.pb
    output_path=inception_v3.circle
    input_arrays=input
    input_shapes=1,299,299,3
    output_arrays=InceptionV3/Predictions/Reshape_1
    converter_version=v1
    
    [one-quantize]
    input_path=inception_v3.circle
    output_path=inception_v3.quantized.circle
    input_data=inception_v3_test_data.h5
    
    ```

- 확인결과, inception_v3_test_data.h5파일이 input으로 필요함 

    - https://github.com/Samsung/ONE/issues/3864
    - [inception_v3_test_data.zip](https://github.com/Samsung/ONE/files/5139370/inception_v3_test_data.zip)
        - 해당 파일 다운로드 후 압축해제

    ```
    $ unzip inception_v3_test_data.zip
    Archive:  inception_v3_test_data.zip
      inflating: inception_v3_test_data.h
    ```

- 실행 성공

    ```
    $ python test.py 
    Estimated count of arithmetic ops: 11.460 G  ops, equivalently 5.730 G  MACs
    Recording 0'th data
    Recording 1'th data
    Recording 2'th data
    Recording 3'th data
    Recording 4'th data
    Recording 5'th data
    Recording 6'th data
    Recording 7'th data
    Recording 8'th data
    Recording 9'th data
    Recording finished. Number of recorded data: 10
    one-build -C one-build_003:  SUCCESS!
    ```

    

### test4

- configurefile

    ```
    [one-build]
    one-import-tf=True
    one-import-tflite=False
    one-import-bcq=False
    one-optimize=False
    one-quantize=False
    one-pack=False
    one-codegen=True
    
    [one-import-tf]
    input_path=inception_v3.pb
    output_path=inception_v3.circle
    input_arrays=input
    input_shapes=1,299,299,3
    output_arrays=InceptionV3/Predictions/Reshape_1
    converter_version=v1
    
    [one-codegen]
    backend=dummy
    command=-o sample.tvn inception_v3.circle
    ```

- dummy가 없음 
    - https://github.com/Samsung/ONE/pull/5436
