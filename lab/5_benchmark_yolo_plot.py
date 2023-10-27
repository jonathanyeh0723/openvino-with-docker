"""Import required librabires."""
import subprocess
from openvino.runtime import Core
import matplotlib.pyplot as plt
import numpy as np


core = Core()
devices = core.available_devices
for device in devices:
    full_device_name = core.get_property(device, "FULL_DEVICE_NAME")
    print(f"[ INFO ] Found {device} plugin: {full_device_name}")

print("Starting to perform benchmark performance visualization...")

models = ['/opt/intel/openvino_2023/open_model_zoo/demos/object_detection_demo/python/yolo-v3-tf/FP16-INT8/yolo-v3-tf.xml',
          '/home/openvino/poc/models/yolov8n_openvino_int8_model/yolov8n_with_preprocess.xml']

np.random.seed(19680801)

cpu_performance = []
gpu_performance = []

if 'CPU' and 'GPU' in devices:
    for model in models:
        subprocess.call([f"benchmark_app -m {model} -d CPU > rich_test_data.txt"], shell=True)
        subprocess.call(["cat rich_test_data.txt | grep Throughput >> benchmark_result_cpu.txt"], shell=True)
        subprocess.call([f"benchmark_app -m {model} -d GPU > rich_test_data.txt"], shell=True)
        subprocess.call(["cat rich_test_data.txt | grep Throughput >> benchmark_result_gpu.txt"], shell=True)

    for txt in ('benchmark_result_cpu.txt', 'benchmark_result_gpu.txt'):
        with open(txt) as f:
            result = f.readlines()
            for x in result:
                element = float(x.split(':')[-1].strip('\n').strip('FPS').strip(' '))
                if txt == 'benchmark_result_cpu.txt':
                    cpu_performance.append(element)
                else:
                    gpu_performance.append(element)
else:
    for model in models:
        subprocess.call([f"benchmark_app -m {model} -d CPU > rich_test_data.txt"], shell=True)
        subprocess.call(["cat rich_test_data.txt | grep Throughput >> benchmark_result_cpu.txt"], shell=True)
    with open('benchmark_result_cpu.txt') as f:
        result = f.readlines()
        for x in result:
            element = float(x.split(':')[-1].strip('\n').strip('FPS').strip(' '))
            cpu_performance.append(element)

labels = ["YOLOv3", "YOLOv8"]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()

ax.set_ylabel('Throughput (FPS)')
ax.set_title('Benchmark Performance Test Results')
ax.set_xticks(x)
ax.set_xticklabels(labels)

if 'CPU' and 'GPU' in devices:
    rects1 = ax.bar(x - width/2, cpu_performance, width, label='CPU')
    rects2 = ax.bar(x + width/2, gpu_performance, width, label='GPU')
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.legend(loc='upper left', title='Device')
else:
    ax.bar(x, cpu_performance, width, label='CPU')
    ax.legend(loc='upper left', title='Device')

fig.tight_layout()
plt.show()

subprocess.call(["rm benchmark_result_*"], shell=True)
subprocess.call(["rm rich_test_data.txt"], shell=True)
