# ONECC문서 

## how-to-prepare-virtualenv.txt

#### About

- last update: 2020-09-15
- This document explains about 'one-prepare-venv' command.
    - 이 문서는 'one-prepare-venv'에 대해 설명함
- 'one-prepare-venv' willprepare python3.8 virtual enviroment with tensorflow-cpu version 2.3.9, recommanded 2.x version as of now, so that 'one-import-tf' command can execute properly.
    - 'one-prepare-venv'는 'one-import-tf'가 실행될 수 있또록, tensorflow-cpu 2.3.9v, 현재 권장 버전 2.x로 파이썬 가상환경을 준비한다.
- 'one-prepare-venv' will also prepare onnx and onnx-tensorflow version 1.7.0 so that 'one-import-onnx' command can execute properly.
    - 'one-prepare-venv'는 또한, 'one-import-onnx'가 제대로 실행될 수 있도록, 'onnx' 및 'onnx-tensorflow' 1.7.0을 준비한다. 



#### Prerequisite

- Please install these required packages before venv preparation.
    - 필수 패키지 설치 

```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install python3.8 python3-pip python3.8-venv
```

#### How to run for Ubuntu

- Just run 'one-prepare-venv' command
    - 실행 

```
$ one-prepare-venv
```

There will be venv folder as of result.

</hr>

## how-to-create-hdf5-dataset

#### About

- Last update: 2020-11-06

- This document briefly explains how to create an input dataset for one-quantize.
    - 이 문서는 one-quantize를 위한 입력 데이터 셋을 만드는 방법을 설명한다. 

- The input dataset of one-quantize has the form of hdf5.
    - one-quantize의 input은 hdf5의 형태를 갖는다. 
- For users who are not familiar with hdf5, we provide a tool to convert raw data to hdf5.
    - hdf5에 대해 익숙하지 않을 유저들을 위해 raw data를 hdf5로 변환할 수 있는 tool을 제공한다. 

- Workflow to generate input dataset (hdf5 file)

    - input dataset 생성 Workflow

    1. Pre-process input data for the target model and save them as raw data files
        - target model에 대한 input data를 전처리하여 raw data file로 저장한다. 

    2. Package the raw data files into the hdf5 file using rawdata2hdf5
        - rawdata2hdf5를 사용하여 raw data를 hdf5 파일로 패키징한다. 

- Note: Users should prepare raw data which can be fed to the target model.
    This is because we don't know which pre-processing logic was used for the target model.
    - user는 target model에 공급할 raw data를 준비해야한다. 
        - target model에 어떤 전처리 로직을 사용했는지 알 수 없기 때문 

#### rawdata2hdf5

- rawdata2hdf5 is a tool to package raw data files into an hdf5 file,which is the format of input dataset for one-quantize.
    - rawdata2hdf5는 raw data file을 hdf5 파일로 패키징하는 도구이며, 이는 one-quantize를 위한 input dataset의 형식이다. 

- Usage:  rawdata2hdf5 --data_list <path/to/text/file> --output_path <path/to/output/file>

#### Example

- Let's make an input dataset for InceptionV3 model.
    - InceptionV3 model의 input dataset을 만들어보자 
    - **Download sample images (You can use your own dataset)**
        - 샘플 이미지 다운로드 (자신의 이미지 사용해도 무방 )

```
$ wget https://github.com/Samsung/ONE/files/5499172/img_files.zip
$ unzip img_files.zip
$ tree img_files

img_files
├── bald-eagle.jpg
├── cow.jpg
├── deer-in-wild.jpg
├── fox.jpg
├── ladybird.jpg
├── orange-portocaliu.jpg
├── pink-lotus.jpg
├── red-church.jpg
├── tomatoes.jpg
└── young-dachshund.jpg
```

2. **Pre-process the images and save them as raw data files**

    - 이미지를 전처리하여 rsaw data file로 저장

    - In this example, we use Pillow and numpy for simple pre-processing.
        - 해당 예에서는, 간단한 전처리를 위해 Pillow와 numpy를 사용 

```bash
$ pip install Pillow numpy
```

- Pillow 설치 에러 시 pip 문제일 수 있으므로 pip 재설치

    ```
    pip install -U --force-reinstall pip 
    ```

    https://hg4535.tistory.com/entry/pip-%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8-%EC%97%90%EB%9F%AC-%EC%9E%AC%EC%84%A4%EC%B9%98-NoneType-object-has-no-attribute-bytes

- Run the pre-processing logic for the target model. We provide a short python script that scales the image data from -1 to 1.
    - 대상 모델에 대한 전처리 로직 실행. 우리는 이미지 데이터를 -1~1로 조정하는 짧은 python script를 제공한다.  

- (This is different from the original pre-processing of InceptionV3. Visit the below link to find the exact algorithm)
    - 이는 원래 Inception V3의 전처리 방식과는 다르며, 정확한 알고리즘을 확인하려면 아래 링크 참고 

https://github.com/tensorflow/models/blob/v2.3.0/research/slim/preprocessing/inception_preprocessing.py

```bash
$ cat > preprocess.py << EOF
```

```python
import os, shutil, PIL.Image, numpy as np

input_dir = 'img_files'
output_dir = 'raw_files'
list_file = 'datalist.txt'

if os.path.exists(output_dir):
  shutil.rmtree(output_dir, ignore_errors=True)
os.makedirs(output_dir)

for (root, _, files) in os.walk(input_dir):
  datalist = open(list_file, 'w')
  for f in files:
    with PIL.Image.open(root + '/' + f) as image:
        img = np.array(image.resize((299, 299),
                                    PIL.Image.ANTIALIAS)).astype(np.float32)
        img = ((img / 255) - 0.5) * 2.0
        output_file = output_dir + '/' + f.replace('jpg', 'data')
        img.tofile(output_file)
        datalist.writelines(os.path.abspath(output_file) + '\n')
  datalist.close()
EOF
```

```bash
$ python preprocess.py
```

- After running preprocess.py, 'raw_files' and 'datalist.txt' will be created.
    - raw_files: a directory where raw data files are saved
    - datalist.txt: a text file that contains the list of raw data files.
- preprocess.py를 실행하면 , 'raw_files'와, 'datalist.txt'가 생성된다.
    - raw_files: 원시 데이터 파일이 저장되는 디렉터리
    -  데이터 리스트txt: 원시 데이터 파일 목록을 포함하는 텍스트 파일.

3. **Run rawdata2hdf5 with datalist.txt**
    - datalist.txt 를 사용해 rawdata2hdf5 를 실행 

```
$ rawdata2hdf5 --data_list datalist.txt --output_path dataset.h5
```

- The contents of the hdf5 file can be printed in the console using h5dump
    - hdf5 파일의 내용은 h5dump를 사용해 console에서 출력할 수 있다.

```
$ h5dump dataset.h5
```

- Now you can call one-quantize with dataset.h5.
    - 이제 우리는 dataset.h5를 이용해 one-quantize를 호출할 수 있다.

</hr>

## how-to-use-one-commands

#### About

- Last update: 2020-10-29

- This document briefly explains how to use one-* commands. Detailed options are not explained here. Run the command to see options.
    - 해당 문서에서는 one-* command를 사용하는 방법을 설명한다. 자세한 옵션은 설명되지 않으며, 명령을 입력하면 옵션을 볼 수 있다.

- Compilation flow for running with onert;

    - 'onert'를 실행하기 위한 compile 흐름 

    1. one-import will import model files generated from famous frameworks
        - one-import는 유명한 프레임워크에서 생성된 model file을 import할 수 있다.

    2. one-optimize will optimize models. This step is optional.
        - one-optimize는 모델을 최적화한다. 해당 단계는 선택사항이다.

    3. one-quantize will quantize models. This step is also optional.
        - one-quantize는 모델을 quantize한다. 해당 단계도 선택 사항이다.

    4. one-pack will pack to nnpkg so that we can run the model with our onert runtime
        1. one-pack은 onert runtime으로 모델을 실행하도록 nnpkg로 패키징한다. 

- Compilation flow for NPU

    - NPU에 대한 컴파일 흐름 

    1. one-import will import model files generated from famous frameworks
        - one-import는 유명한 프레임워크에서 생성된 model file을 import할 수 있다.

    2. one-optimize will optimize models. This step is optional.
        - one-optimize는 모델을 최적화한다. 해당 단계는 선택사항이다.

    3. one-quantize will quantize models. Depending on the NPUs.
        - one-quantize는 모델을 quantize한다. 이는 NPU에 의존한다.

    4. one-codegen will compile to binary codes.
        - one-codegen은 binary code로 컴파일된다.

#### common feature

[configuration file]

- You can run one-commands with configuration file as well as command line parameters. The
    configuration file should be written with the options the one-commands need to run.
    - 우리는 configuration file 및 command line parameter를 이용하여 one-commands를 실행할 수 있다.
    - configuration file은 'one-command'를 실행하는데 꼭 필요한 옵션과 함께 작성되어야 한다. 

```
# configuration_file.cfg

[The_driver_you_want_to_run]
input_path=/input/path/to/convert
output_path=...
option_0=...
option_1=...
...
```

- You can see a template file for how to write a configuration file in `one-build.template.cfg`.
    - 우리는 configuaration file 작성 방법에 대한 템플릿을 'one-build.template.cfg'에서 확인할 수 있다.

[options to write]

- Sometimes you want to change certain options without touching the configuration file. If you
    pass the option directly to the command line, the option is processed prior to the configuration
    file. A list of options can be found in each driver's help message with `-h` option.
    - 가끔 configuration file에 손대지 않고, 특정 옵션을 변경하려는 경우가 있다. 만약 옵션을 직접적으로 command line에 전달한다면, option이 configuration file보다 먼저 처리된다.
    - option 목록은 '-h' 옵션이 있는 각 driver's help message에서 확인할 수 있다.

e.g.
```
$ ./one-import tf -C my-conf.cfg -i path/to/overwrite.pb
```

#### one-build

- one-build is an integrated driver that can execute one-commands at once. It's nice to run each driver individually, but sometimes you'll want to put together the most frequently used commands and run them all at once. You can do this with one-build and its configuration file.
    - one-buiild는 한 번에 하나의 테스트를 실행하는 integrated driver이다. 
    - 각 드라이버를 개별적으로 실행하는 것은 좋지만, 가끔은 자주 사용하는 명령어를 조합하여 한 번에 실행하는 것이 더 좋을수도 있다.
    - 우리는 one-build 및 configuration file을 사용하여 해당 작업을 수행할 수 있다.

- For one-build, the configuration file needs 'one-build' section that consists of list of driver.
    - one-build의 경우, configuration file에는 driver 목록으로 구성된 'one-build' 섹션이 필요하다. 

```
# one-build.template.cfg
[one-build]
one-import-tf=True
one-import-tflite=False
one-import-bcq=False
one-optimize=True
one-quantize=False
one-pack=True
one-codegen=False
```

[one-import-tf]
...

[one-optimize]
...

[one-pack]

...

See 'one-build.template.cfg' for more details.

자세한 내용은 'one-build.template.cfg'를 참조하십시오.

#### one-import

- one-import will invokes one-import-* commands.
    - one-import는 one-import-* commands를 불러온다.

- Syntax: one-import [framework] [options]

- Currently supported frameworks are 'tf', 'tflite' for TensorFlow and TensorFlow lite.
    - 현재 지원되는 프레임워크는 'tf'와 'tflite'이다. 



#### one-import-bcq

- This will convert Tensorflow model file (.pb) to our circle model file with applying BCQ.
    - 텐서플로 모델파일(.pb)에 BCQ를 적용하여 ONE circlefile로 변환된다.
- To execute this command, original Tensorflow model file must include BCQ information.
    - 해당 명령을 실행하기 위해 원본 텐서플로 모델 파일에 BCQ 정보가 포함되어야 한다. 

- This command invokes following scripts internally.

    - 이 커맨드는 내부적으로 아래 스크립트들을 호출한다. 
    - generate_bcq_metadata : Generate BCQ metadata in the model
        - 모델에서 BCQ 메타데이터 생성 

    - generate_bcq_info : Designate BCQ information nodes as model output automatically
        - BCQ 정보 node를 자동으로 model output으로 지정 


    - tf2tfliteV2 : Convert Tensorflow model to tflite model
        - tf model을 tflite model로 변환 


    - tflite2circle : Convert Tensorflow Lite model to circle model. When this command is finished, BCQ information nodes will be removed if BCQ information was valid and applying BCQ is done correctly without any errors.
    - tflite 모델을 circle model로 변환. 해당 명령이 완료될 때, BCQ 정보가 유효하고, BCQ 적용이 오류없이 수행되면, BCQ 정보 노드가 제거된다. 


- As tf2tfliteV2.py runs TensorFlow lite converter, you need to have TensorFlow installed in your system. We recommand to use 2.3.0 for now.
    - tf2tfliteV2.py에서 Tensorflow lite converter를 실행하기 때문에, 시스템에 TensorFlow가 설치되어 있어야 함. 일단 2.3.0 version을 사용하는 것이 좋음 

- We provide python virtual environment and one-import-bcq will enter and leave this environment so that you don't need to explictly 'activate' virtual environment.
    - Python 가상환경을 제공하고, one-import-bcq가 해당 환경에 들어오기 때문에, 가상환경을 명시적으로 활성화 할 필요는 없음 

#### one-import-tflite

- You can use one-import-tflite to convert TensorFlow lite model (.tflite) file to our circle model. Internally this will invoke tflite2circle.
    - one-import-tflite를 사용해서 tflite 파일을 circle model로 변환할 수 있다. 내부적으로 이는 tflite2circle을 호출한다. 



#### one-optimize

- one-optimize provides network or operator transformation shown below.
    - one-optimize는 아래에 표시된 network 또는 operator transformation을 제공한다. 

**Current transformation options are**

- disable_validation : This will turn off operator validations.
   - 연산자 유효성 검사 해제 
- expand_broadcast_const : This will expand broadcastable constant node inputs
   - broadcast가능한 constant node input 확장 
- fold_add_v2 : This removes AddV2 operation which can be folded
   - folded 가능한 V2 추가 작업을 제거 
- fold_cast : This removes Cast operation which can be folded
   - folded 가능한 Cast operation을 제거한다. 
- fold_densify: This removes Densify operator which can be folded
   - folded 가능한 Densify 연산자 제거 
- fold_dequantize : This removes Dequantize operation which can be folded
   - folded 가능한 Dequantize 연산자 제거 
- fold_dwconv : This folds Depthwise Convolution operation which can be folded
   - folded 가능한 Depthwise Convolution 연산자 제거 
- fold_gather : This removes Gather operation which can be folded
   - folded 가능한 Gather 연산자 제거 
- fold_sparse_to_dense : This removes SparseToDense operation which can be folded
   - folded 가능한 SparseToDense 연산자 제거 
- forward_reshape_to_unaryop: This will move Reshape after UnaryOp for centain condition
   - Certain condition 하에 UnaryOp 후 Reshape로 이동 
- fuse_add_with_fully_connected: This fuses Add operator with the preceding FullyConnected operator if possible
   - 가능한 경우 Add 연산자를 이전 FullyConnected 연산자와 결합
- fuse_add_with_tconv: This fuses Add operator with the preceding TConv operator if possible
   - 가능한 경우 Add 연산자와 선행되는 TConv 연산자를 결합 
- fuse_batchnorm_with_conv : This fuses BatchNorm operator to convolution operator
   - BatchNorm 연산자를 Convolution 연산자에 결합 
- fuse_batchnorm_with_dwconv : This fuses BatchNorm operator to depthwise convolution operator
   - Batchnorm 연산자를 depthwise convolution 연산자에 결합 
- fuse_batchnorm_with_tconv : This fuses BatchNorm operator to transpose convolution operator
   - Batchnorm 연산자를 transfer convolution 연산자에 결합 
- fuse_bcq: This enables Binary-Coded-bases Quantized DNNs
   - Binary-Code 기반 Quantized된 DNN 사용 
   - read https://arxiv.org/abs/2005.09904 for detailed information
- fuse_instnorm: This will convert instance normalization related operators to one InstanceNormalization operator that our onert provides for faster execution.
  - 인스턴스 정규화 관련 연산자가 하나의 인스턴스 정규화 연산자로 변환되어 더 빠른 실행을 할 수 있음
- fuse_preactivation_batchnorm: This fuses batch normalization operators of pre-activations to Conv operators.
   - 사전 활성화된 Conv 연산자에 batch normalization 연산자를 결합한다. 
- fuse_activation_function: This fuses Activation function to a preceding operator.
   - 이전 작동자와 활성화 기능이 결합된다.
- fuse_mean_with_mean: This fuses two consecutive ReduceMean operations into one.
- fuse_transpose_with_mean: This fuses ReduceMean with a preceding Transpose under certain conditions.
- make_batchnorm_gamma_positive: This makes negative gamma of batch normalization into a small positive value (1e-10).
  Note that this pass can change the execution result of the model.
  So, use it only when the impact is known to be acceptable.
- mute_warnings : This will turn off warning messages.
- generate_profile_data : This will turn on profiling data generation.
- remove_fakequant : This will remove all fakequant operators.
- remove_quantdequant : This will remove all Quantize-Dequantize sequence.
- remove_redundant_quantize : This removes redundant quantize operators.
- remove_redundant_reshape : This fuses or removes redundant reshape operators.
- remove_redundant_transpose : This fuses or removes redundant transpose operators.
- remove_unnecessary_reshape : This removes unnecessary reshape operators.
- remove_unnecessary_slice : This removes unnecessary slice operators.
- remove_unnecessary_strided_slice : This removes unnecessary strided slice operators.
- remove_unnecessary_split : This removes unnecessary split operators.
- replace_cw_mul_add_with_depthwise_conv: This will replace channel-wise Mul/Add with DepthwiseConv2D.
- resolve_customop_add: This will convert Custom(Add) to normal Add operator
- resolve_customop_batchmatmul: This will convert Custom(BatchMatMul) to normal BatchMatMul operator
- resolve_customop_matmul: This will convert Custom(MatMul) to normal MatMul
  operator
- resolve_customop_max_pool_with_argmax: This will convert Custom(MaxPoolWithArgmax)
  to net of builtin operators.
- shuffle_weight_to_16x1float32 : This will convert weight format of FullyConnected to SHUFFLED16x1FLOAT32.
  Note that it only converts weights whose row is a multiple of 16.
- substitute_pack_to_reshape : This will convert single input Pack to Reshape.
- substitute_padv2_to_pad : This will convert certain condition PadV2 to Pad.
- substitute_splitv_to_split : This will convert certain condition SplitV to Split.
- substitute_squeeze_to_reshape : This will convert certain condition Squeeze to Reshape.
- substitute_strided_slice_to_reshape : This will convert certain condition StridedSlice to Reshape.
- substitute_transpose_to_reshape : This will convert certain condition Transpose to Reshape.
- transform_min_max_to_relu6: This will transform Minimum-Maximum pattern to Relu6 operator.
- transform_min_relu_to_relu6: This will transform Minimum(6)-Relu pattern to Relu6 operator.

#### one-quantize

- one-quantize will quantize float32 model to uint8 so that the model can benefit for speed that our onert runtime and NPU provides. For convolution type operators we currently support layer-wise quantization. Later we will support int16 and channel-wise quantization.
    - one-quantize는 float32 모델을 unit8으로 quantize하여 모델이 우리의 onert 런타임과 NPU가 제공하는 속도에 향상을 줄 수 있다.
    - Convolution 유형의 연산자일 경우,현재 계층별 quantization을 지원한다. 추후, int16 및 채널벌 quantization을 제공할 것이다.  

- Internally this calls circle-quantizer and record-minmax tools.

    - 내부적으로 이것은 Circle-quantizer나 record-minmax tool로 불리운다. 

    

#### one-pack

- one-pack will generate a package from circle model to nnpackage for our onert runtime.
    - one-pack은 onert 런타임에 대한 nn패키지의 circle model에서  패키저를 생성한다. 

- Output is a folder with the model(s) and meta information.
    - output은 model 및 meta 정보가 있는 폴더이다. 

ex) if you have a model named '20200719.circle' and want to pack to 'testnnpack'

```
$ one-pack -i 20200709.circle -o testnnpack

$ tree testnnpack
testnnpack
└── 20200709
    ├── 20200709.circle
    └── metadata
        └── MANIFEST
```

#### one-codegen

- one-codegen, like one-import will invoke backend code generation commands. As of now, our ONE repo does not provide any code generation commands yet.
    - one-codgen은 one-import와 마찬가지로 백엔드 코드 생성 명령을 호출한다. 현재 ONE repo는 아직 어떠한 코드 생성 명령도 지원하지 않는다. 

Syntax: one-codegen [target-backend] [options]

This will invoke [target-backend]-compile command if available.
