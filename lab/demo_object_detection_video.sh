#!/bin/bash
cd /opt/intel/openvino_2023/open_model_zoo/demos/object_detection_demo/python
python3 object_detection_demo.py -m yolo-v3-tf/FP16-INT8/yolo-v3-tf.xml -i highway_car.mp4 -at yolo --label /home/openvino/lab/labels/coco_80cl.txt -d GPU
