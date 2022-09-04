# How to build package

https://nnfw.readthedocs.io/en/latest/howto/how-to-build-package.html

## Overview

이 문서는 'onert' runtime에 모델을 실행하기 위한 패키지를 빌드하는 방법에 대해 설명합니다.

이 패키지는 다음과 같이 구성됩니다. 

추가 파일 사용자는 commandl line tool을 통해 패키지를 작성할 수 있습니다. 

NOTE: 아래 표시된 각 명령의 예와 옵션은 이 문서 작성 버전(1.21.0)에서 가져온 것입니다. 이는 최신 버전 명령인 1.9.0과 다를 수 있습니다. 필요한 경우 Issue를 등록하거나, PR을 게시해 수정하십시오. 

## Import model

### 개요

현재 작성된 문서에서는 Tensorflow, Tensorflow lite model이 지원됩니다.

모델을 가져오려면 model의 framework key 및  argument와 함께 `one-import`를 수행하세요

```bash
$ one-import FRAMEWORK [argument]
```

key 없이 `one-import`를 실행하면 지원되는 프레임워크 목록이 표시됩니다.

- `one-import` 명령의 예(1.21.0)

    ```
    $ one-import
    Usage: one-import [FRAMEWORK] ...
    Available FRAMEWORK drivers:
    bcq
    tf
    tflite
    ```

- **현재에는 지원되는 프레임워크가 아닌  에러 발생 및 driver 요구**

    ```
    $ one-import
    usage: one-import [-h] [-C CONFIG] [-v] driver
    one-import: error: the following arguments are required: driver
    ```

- `one-import -h` 실행 결과  현재 지원하는 모델은 `tf`, `tflite`, `bcq`, `onnx`인 것으로 확인됨

    ```bash
    $one-import -h
    usage: one-import [-h] [-C CONFIG] [-v] driver
    
    command line tool to convert various format to circle
    
    positional arguments:
      driver                driver name to run (supported: tf, tflite, bcq, onnx)
    
    optional arguments:
      -h, --help            show this help message and exit
      -C CONFIG, --config CONFIG
                            run with configuation file
      -v, --version         show program's version number and exit
    ```

### Example for Tensorflow

**다음은 TensorFlow 모델을 가져오는 예제입니다.**

```bash
$ one-import tf --input_path mymodel.pb --output_path mymodel.circle \
--input_arrays input1,input2 --input_shapes "1,224,224,3:1000" \
--output_arrays output
```

- 실행해보기

    ```bash
    $ one-import tf --input_path inception_v3.pb --output_path inception_v3.circle \
    --input_arrays input --input_shapes "1,299,299,3" \
    --output_arrays InceptionV3/Predictions/Reshape_1
    Estimated count of arithmetic ops: 11.460 G  ops, equivalently 5.730 G  MACs
    ```

    - inception_v3.pb 다운 경로

        ```bash
        $ wget https://storage.googleapis.com/download.tensorflow.org/models/tflite/model_zoo/upload_20180427/inception_v3_2018_04_27.tgz
        $ tar -xvf inception_v3_2018_04_27.tgz
        ```

- `--help`로 실행하면 현재 필수/선택적 인자가 표시됩니다.

    ```
    $ one-import-tf --help
    usage: one-import-tf [-h] [-v] [-V] [-C CONFIG] [--v1 | --v2] [--graph_def | --saved_model | --keras_model] [-i INPUT_PATH] [-o OUTPUT_PATH] [-I INPUT_ARRAYS]
                         [-s INPUT_SHAPES] [-O OUTPUT_ARRAYS] [--save_intermediate]
    
    command line tool to convert TensorFlow to circle
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -V, --verbose         output additional information to stdout or stderr
      -C CONFIG, --config CONFIG
                            run with configuation file
      --save_intermediate   Save intermediate files to output folder
    
    converter arguments:
      --v1                  use TensorFlow Lite Converter 1.x
      --v2                  use TensorFlow Lite Converter 2.x
      --graph_def           use graph def file(default)
      --saved_model         use saved model
      --keras_model         use keras model
      -i INPUT_PATH, --input_path INPUT_PATH
                            full filepath of the input file
      -o OUTPUT_PATH, --output_path OUTPUT_PATH
                            full filepath of the output file
      -I INPUT_ARRAYS, --input_arrays INPUT_ARRAYS
                            names of the input arrays, comma-separated
      -s INPUT_SHAPES, --input_shapes INPUT_SHAPES
                            shapes corresponding to --input_arrays, colon-separated (ex:"1,4,4,3:1,20,20,3")
      -O OUTPUT_ARRAYS, --output_arrays OUTPUT_ARRAYS
                            names of the output arrays, comma-separated
    ```

### Example for TensorFlow liste

**다음은 TensorFlowlite 모델을 가져오는 예입니다.**

```
$ one-import tflite --input_path mymodel.tflite --output_path mymodel.circle
```

- 실행

    ```
    $ one-import tflite --input_path inception_v3.tflite --output_path inception_v3_tflite.circle
    ```

- `--help`로 실행하면 현재 필수/선택적 인자가 표시됩니다.

    ```
    $ one-import-tflite --help
    usage: one-import-tflite [-h] [-v] [-V] [-C CONFIG] [-i INPUT_PATH] [-o OUTPUT_PATH]
    
    command line tool to convert TensorFlow lite to circle
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -V, --verbose         output additional information to stdout or stderr
      -C CONFIG, --config CONFIG
                            run with configuation file
    
    converter arguments:
      -i INPUT_PATH, --input_path INPUT_PATH
                            full filepath of the input file
      -o OUTPUT_PATH, --output_path OUTPUT_PATH
                            full filepath of the output file
    ```

### Example for TensorFlow Model Including BCQ Information

다음은 BCQ 정보를 포함하는 TensorFlow 모델을 가져오는 예입니다. 이 명령의 결과로 BCQ 정보 노드가 보존됩니다.

```
$ one-import bcq --input_path bcqmodel.pb --output_path bcqmodel.circle
```

- 실행

    ```
    $ one-import bcq --input_path inception_v3.pb --output_path bcqmodel.circle \
    --input_arrays input --input_shapes "1,299,299,3" \
    --output_arrays InceptionV3/Predictions/Reshape_1
    Estimated count of arithmetic ops: 11.460 G  ops, equivalently 5.730 G  MACs
    ```

    

- `--help`로 실행하면 현재 필수/선택적 인자가 표시됩니다.

    ```
    $ one-import-bcq -h
    usage: one-import-bcq [-h] [-v] [-V] [-C CONFIG] [--v1 | --v2] [-i INPUT_PATH] [-o OUTPUT_PATH] [-I INPUT_ARRAYS] [-s INPUT_SHAPES] [-O OUTPUT_ARRAYS]
    
    command line tool to convert TensorFlow with BCQ to circle
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -V, --verbose         output additional information to stdout or stderr
      -C CONFIG, --config CONFIG
                            run with configuation file
    
    converter arguments:
      --v1                  use TensorFlow Lite Converter 1.x
      --v2                  use TensorFlow Lite Converter 2.x
      -i INPUT_PATH, --input_path INPUT_PATH
                            full filepath of the input file
      -o OUTPUT_PATH, --output_path OUTPUT_PATH
                            full filepath of the output file
      -I INPUT_ARRAYS, --input_arrays INPUT_ARRAYS
                            names of the input arrays, comma-separated
      -s INPUT_SHAPES, --input_shapes INPUT_SHAPES
                            shapes corresponding to --input_arrays, colon-separated (ex:"1,4,4,3:1,20,20,3")
      -O OUTPUT_ARRAYS, --output_arrays OUTPUT_ARRAYS
                            names of the output arrays, comma-separated
    ```

    

## Optimize circle model

circle model은 더 나은 성능과 더 작은 크기를 위해 최적화될 수 있다. 이를 위한 일반적인 최적화 알고리즘은 일부 연산자 패턴을 하나의 퓨전 연산자에 결합하는 것이다.

다음은 circle model을 최적화 하는 예입니다.

```
$ one-optimize --all --input_path mymodel.circle --output_path optmodel.circle
```

- 실행

    - 현재 `--all`이라는 옵션은 없어진 것 같음 

    ```
    $ one-optimize --input_path inception_v3.circle --output_path optmodel.circle
    ```

    

- `--help`로 실행하면 현재 필수/선택 인자가 표시됩니다.

    ```
    command line tool to optimize circle model
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -V, --verbose         output additional information to stdout or stderr
      -C CONFIG, --config CONFIG
                            run with configuation file
    
    arguments for utility:
      -p, --generate_profile_data
                            generate profiling data
      --change_outputs CHANGE_OUTPUTS
                            Experimental: Change first subgraph output nodes to CSV names
    
    arguments for optimization:
      -i INPUT_PATH, --input_path INPUT_PATH
                            full filepath of the input file
      -o OUTPUT_PATH, --output_path OUTPUT_PATH
                            full filepath of the output file
      --convert_nchw_to_nhwc
                            Experimental: This will convert NCHW operators to NHWC under the assumption that input model is NCHW.
      --expand_broadcast_const
                            expand broadcastable constant node inputs
      --nchw_to_nhwc_input_shape
                            convert the input shape of the model (argument for convert_nchw_to_nhwc)
      --nchw_to_nhwc_output_shape
                            convert the output shape of the model (argument for convert_nchw_to_nhwc)
      --fold_add_v2         fold AddV2 op with constant inputs
      --fold_cast           fold Cast op with constant input
      --fold_densify        fold Densify op with sparse constant input
      --fold_dequantize     fold Dequantize op
      --fold_dwconv         fold Depthwise Convolution op with constant inputs
      --fold_gather         fold Gather op
      --fold_sparse_to_dense
                            fold SparseToDense op
      --forward_reshape_to_unaryop
                            Forward Reshape op
      --fuse_add_with_tconv
                            fuse Add op to Transposed
      --fuse_add_with_fully_connected
                            fuse Add op to FullyConnected op
      --fuse_batchnorm_with_conv
                            fuse BatchNorm op to Convolution op
      --fuse_batchnorm_with_dwconv
                            fuse BatchNorm op to Depthwise Convolution op
      --fuse_batchnorm_with_tconv
                            fuse BatchNorm op to Transposed Convolution op
      --fuse_bcq            apply Binary Coded Quantization
      --fuse_preactivation_batchnorm
                            fuse BatchNorm operators of pre-activations to Convolution op
      --fuse_mean_with_mean
                            fuse two consecutive Mean ops
      --fuse_transpose_with_mean
                            fuse Mean with a preceding Transpose under certain conditions
      --make_batchnorm_gamma_positive
                            make negative gamma of BatchNorm to a small positive value (1e-10). Note that this pass can change the execution result of the model. So, use it
                            only when the impact is known to be acceptable.
      --fuse_activation_function
                            fuse Activation function to a preceding operator
      --fuse_instnorm       fuse ops to InstanceNorm operator
      --replace_cw_mul_add_with_depthwise_conv
                            replace channel-wise Mul/Add with DepthwiseConv2D
      --remove_fakequant    remove FakeQuant ops
      --remove_quantdequant
                            remove Quantize-Dequantize sequence
      --remove_redundant_quantize
                            remove redundant Quantize ops
      --remove_redundant_reshape
                            fuse or remove subsequent Reshape ops
      --remove_redundant_transpose
                            fuse or remove subsequent Transpose ops
      --remove_unnecessary_reshape
                            remove unnecessary reshape ops
      --remove_unnecessary_slice
                            remove unnecessary slice ops
      --remove_unnecessary_strided_slice
                            remove unnecessary strided slice ops
      --remove_unnecessary_split
                            remove unnecessary split ops
      --replace_non_const_fc_with_batch_matmul
                            replace FullyConnected op with non-const weights to BatchMatMul op
      --replace_sub_with_add
                            replace Sub op with Add op
      --resolve_customop_add
                            convert Custom(Add) op to Add op
      --resolve_customop_batchmatmul
                            convert Custom(BatchMatmul) op to BatchMatmul op
      --resolve_customop_matmul
                            convert Custom(Matmul) op to Matmul op
      --resolve_customop_max_pool_with_argmax
                            convert Custom(MaxPoolWithArgmax) to net of builtin operators
      --resolve_customop_splitv
                            convert Custom(SplitV) op to SplitV op
      --shuffle_weight_to_16x1float32
                            convert weight format of FullyConnected op to SHUFFLED16x1FLOAT32. Note that it only converts weights whose row is a multiple of 16
      --substitute_pack_to_reshape
                            convert single input Pack op to Reshape op
      --substitute_padv2_to_pad
                            convert certain condition PadV2 to Pad
      --substitute_splitv_to_split
                            convert certain condition SplitV to Split
      --substitute_squeeze_to_reshape
                            convert certain condition Squeeze to Reshape
      --substitute_strided_slice_to_reshape
                            convert certain condition StridedSlice to Reshape
      --substitute_transpose_to_reshape
                            convert certain condition Transpose to Reshape
      --transform_min_max_to_relu6
                            transform Minimum-Maximum pattern to Relu6 op
      --transform_min_relu_to_relu6
                            transform Minimum(6)-Relu pattern to Relu6 op
    ```

    

## Quantize circle model

Floating-point circle model은 더 빠른 추론 속도를 위해 더 낮은 정밀도 형식(ex: uint8 or int16)으로 양자화 될 수 있다.

가중치와 활성화를 나타내는 비트 수를 줄임으로써 모델 크기를 줄일 수 있다. 

다음은 circle model을 양자화 하는 예입니다.

```
$ one-quantize --input_path mymodel.circle --output_path quantmodel.circle
```

- `--help`로 실행하면 현재 필수/선택 인자가 표시됩니다.

    ```
    $ one-quantize -h
    usage: one-quantize [-h] [-v] [-V] [-C CONFIG] [-i INPUT_PATH] [-d INPUT_DATA] [-f INPUT_DATA_FORMAT] [-o OUTPUT_PATH] [-p] [--save_intermediate]
                        [--input_dtype INPUT_DTYPE] [--input_model_dtype INPUT_MODEL_DTYPE] [--quantized_dtype QUANTIZED_DTYPE] [--granularity GRANULARITY]
                        [--input_type INPUT_TYPE] [--output_type OUTPUT_TYPE] [--min_percentile MIN_PERCENTILE] [--max_percentile MAX_PERCENTILE] [--mode MODE]
                        [--TF-style_maxpool] [--quant_config QUANT_CONFIG] [--evaluate_result] [--test_data TEST_DATA] [--print_mae] [--print_mape] [--print_mpeir]
                        [--print_top1_match] [--print_top5_match] [--print_mse] [--force_quantparam] [--tensor_name TENSOR_NAME] [--scale SCALE] [--zero_point ZERO_POINT]
                        [--copy_quantparam] [--src_tensor_name SRC_TENSOR_NAME] [--dst_tensor_name DST_TENSOR_NAME] [--fake_quantize]
    
    command line tool to quantize circle model
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -V, --verbose         output additional information to stdout or stderr
      -C CONFIG, --config CONFIG
                            run with configuation file
      -i INPUT_PATH, --input_path INPUT_PATH
                            full filepath of the input circle model
      -d INPUT_DATA, --input_data INPUT_DATA
                            full filepath of the input data used for post-training quantization. if not specified, run with random input data.
      -f INPUT_DATA_FORMAT, --input_data_format INPUT_DATA_FORMAT
                            file format of input data. h5/hdf5 (default), list/filelist (a text file where a file path of input data is written in each line), or
                            dir/directory (a directory where input data are saved)
      -o OUTPUT_PATH, --output_path OUTPUT_PATH
                            full filepath of the output quantized model
      -p, --generate_profile_data
                            generate profiling data
      --save_intermediate   Save intermediate files to output folder
    
    arguments for quantization:
      --input_dtype INPUT_DTYPE
                            input model data type (supported: float32, default=float32). Deprecated (Use input_model_dtype)
      --input_model_dtype INPUT_MODEL_DTYPE
                            input model data type (supported: float32, default=float32)
      --quantized_dtype QUANTIZED_DTYPE
                            data type of output quantized model (supported: uint8, int16, default=uint8)
      --granularity GRANULARITY
                            quantization granularity (supported: layer, channel, default=layer)
      --input_type INPUT_TYPE
                            data type of inputs of quantized model (supported: uint8, int16, float32, default=quantized_dtype). QUANTIZE Op will be inserted at the
                            beginning of the quantized model if input_type is different from quantized_dtype.
      --output_type OUTPUT_TYPE
                            data type of outputs of quantized model (supported: uint8, int16, float32, default=quantized_dtype). QUANTIZE Op will be inserted at the end of
                            the quantized model if output_type is different from quantized_dtype.
      --min_percentile MIN_PERCENTILE
                            minimum percentile (0.0~100.0, default=1.0). Algorithm parameter for calibration. This is valid when calibration algorithm is percentile.
      --max_percentile MAX_PERCENTILE
                            maximum percentile (0.0~100.0, default=99.0). Algorithm parameter for calibration. This is valid when calibration algorithm is percentile.
      --mode MODE           calibration algorithm for post-training quantization (supported: percentile/moving_average, default=percentile). 'percentile' mode uses the n-th
                            percentiles as min/max values. 'moving_average' mode records the moving average of min/max.
      --TF-style_maxpool    Force MaxPool Op to have the same input/output quantparams. NOTE: This option can degrade accuracy of some models.)
      --quant_config QUANT_CONFIG
                            Path to the quantization configuration file.
      --evaluate_result     Evaluate accuracy of quantized model. Run inference for both fp32 model and the quantized model, and compare the inference results.
      --test_data TEST_DATA
                            Path to the test data used for evaluation.
      --print_mae           Print MAE (Mean Absolute Error) of inference results between quantized model and fp32 model.
      --print_mape          Print MAPE (Mean Absolute Percentage Error) of inference results between quantized model and fp32 model.
      --print_mpeir         Print MPEIR (Mean Peak Error to Interval Ratio) of inference results between quantized model and fp32 model.
      --print_top1_match    Print Top-1 match ratio of inference results between quantized model and fp32 model.
      --print_top5_match    Print Top-5 match ratio of inference results between quantized model and fp32 model.
      --print_mse           Print MSE (Mean Squared Error) of inference results between quantized model and fp32 model.
    
    arguments for force_quantparam option:
      --force_quantparam    overwrite quantparam (scale, zero_point) to the specified tensor in the quantized model.
      --tensor_name TENSOR_NAME
                            tensor name (string)
      --scale SCALE         scale (float)
      --zero_point ZERO_POINT
                            zero point (int)
    
    arguments for copy_quantparam option:
      --copy_quantparam     copy quantparam (scale, zero_point) of a tensor to another tensor.
      --src_tensor_name SRC_TENSOR_NAME
                            tensor name (string)
      --dst_tensor_name DST_TENSOR_NAME
                            tensor name (string)
    
    arguments for fake_quantize option:
      --fake_quantize       convert quantized model to fake-quantized fp32 model.
    ```

- 실행

    ```
    $ one-quantize --input_path inception_v3.circle --output_path quantmodel.circle
    Recording 0'th data
    Recording 1'th data
    Recording 2'th data
    Recording finished. Number of recorded data: 3
    ```

    

## Pack circle model

`one-pack` command로 패키지를 만들 수 있습니다

```
$ one-pack -i mymodel.circle -o nnpackage
```

nnpackage는 circle model과 추가 파일이 들어있는 폴더입니다. 

- 실행

    ```
    $ one-pack -i inception_v3.circle -o nnpackage
    ```

- 결과 비교 

    - 이전

        ```
        $ tree
        .
        ├── bcqmodel.circle
        ├── bcqmodel.circle.log
        ├── inception_v3.circle
        ├── inception_v3.circle.log
        ├── inception_v3.pb
        ├── inception_v3.tflite
        ├── inception_v3_2018_04_27.tgz
        ├── inception_v3_tflite.circle
        ├── inception_v3_tflite.circle.log
        ├── labels.txt
        ├── optmodel.circle
        ├── optmodel.circle.log
        ├── quantmodel.circle
        └── quantmodel.circle.log
        ```

    - 이후

        ```
        $ tree
        .
        ├── bcqmodel.circle
        ├── bcqmodel.circle.log
        ├── inception_v3.circle
        ├── inception_v3.circle.log
        ├── inception_v3.pb
        ├── inception_v3.tflite
        ├── inception_v3_2018_04_27.tgz
        ├── inception_v3_tflite.circle
        ├── inception_v3_tflite.circle.log
        ├── labels.txt
        ├── nnpackage
        │   └── inception_v3
        │       ├── inception_v3.circle
        │       └── metadata
        │           └── MANIFEST
        ├── nnpackage.log
        ├── optmodel.circle
        ├── optmodel.circle.log
        ├── quantmodel.circle
        └── quantmodel.circle.log
        ```

- `--help`로 실행하면 현재 필수/선택 인자가 표시됩니다.

    ```
    $ one-pack --help
    usage: one-pack [-h] [-v] [-V] [-C CONFIG] [-i INPUT_PATH] [-o OUTPUT_PATH]
    
    command line tool to package circle and metadata into nnpackage
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -V, --verbose         output additional information to stdout or stderr
      -C CONFIG, --config CONFIG
                            run with configuation file
    
    arguments for packaging:
      -i INPUT_PATH, --input_path INPUT_PATH
                            full filepath of the input file
      -o OUTPUT_PATH, --output_path OUTPUT_PATH
                            full filepath of the output file
    ```

    
