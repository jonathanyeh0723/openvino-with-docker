#!/bin/bash
python3 /opt/intel/openvino/deployment_tools/tools/benchmark_tool/benchmark_app.py -m /opt/intel/openvino_models/public/googlenet-v4-tf/FP16-INT8/googlenet-v4-tf.xml -d GPU -api async -t 60 > rich_test_data.txt
cat rich_test_data.txt | grep Throughput >> benchmark_result.txt
python3 /opt/intel/openvino/deployment_tools/tools/benchmark_tool/benchmark_app.py -m /opt/intel/openvino_models/public/resnet-50-tf/FP16-INT8/resnet-50-tf.xml -d GPU -api async -t 60 > rich_test_data.txt
cat rich_test_data.txt | grep Throughput >> benchmark_result.txt
python3 /opt/intel/openvino/deployment_tools/tools/benchmark_tool/benchmark_app.py -m /opt/intel/openvino_models/public/vgg19/FP16-INT8/vgg19.xml -d GPU -api async -t 60 > rich_test_data.txt
cat rich_test_data.txt | grep Throughput >> benchmark_result.txt
python3 /opt/intel/openvino/deployment_tools/tools/benchmark_tool/benchmark_app.py -m /opt/intel/openvino_models/public/ssd_mobilenet_v2_coco/FP16-INT8/ssd_mobilenet_v2_coco.xml -d GPU -api async -t 60 > rich_test_data.txt
cat rich_test_data.txt | grep Throughput >> benchmark_result.txt
python3 /opt/intel/openvino/deployment_tools/tools/benchmark_tool/benchmark_app.py -m /opt/intel/openvino_models/public/yolo-v3-tf/FP16-INT8/yolo-v3-tf.xml -d GPU -api async -t 60 > rich_test_data.txt
cat rich_test_data.txt | grep Throughput >> benchmark_result.txt
python3 /opt/intel/openvino/deployment_tools/tools/benchmark_tool/benchmark_app.py -m /opt/intel/openvino_models/public/yolo-v4-tf/FP16-INT8/yolo-v4-tf.xml -d GPU -api async -t 60 > rich_test_data.txt
cat rich_test_data.txt | grep Throughput >> benchmark_result.txt
python3 /opt/intel/openvino/deployment_tools/tools/benchmark_tool/benchmark_app.py -m /opt/intel/openvino_models/public/unet_256/FP16-INT8/unet_256.xml -d GPU -api async -t 60 > rich_test_data.txt
cat rich_test_data.txt | grep Throughput >> benchmark_result.txt
rm rich_test_data.txt
python3 automation.py
rm benchmark_result.txt
