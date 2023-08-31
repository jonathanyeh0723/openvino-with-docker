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

models = ['public/googlenet-v2/FP16/googlenet-v2.xml',
          'public/ssdlite_mobilenet_v2/FP16/ssdlite_mobilenet_v2.xml',
          'intel/road-segmentation-adas-0001/FP16/road-segmentation-adas-0001.xml']

try:
    if 'CPU' and 'GPU' in devices:
        for model in models:
            subprocess.call([f"benchmark_app -m {model} -d CPU > rich_test_data.txt"], shell=True)
            subprocess.call(["cat rich_test_data.txt | grep Throughput >> benchmark_result_cpu.txt"], shell=True)
            subprocess.call([f"benchmark_app -m {model} -d GPU > rich_test_data.txt"], shell=True)
            subprocess.call(["cat rich_test_data.txt | grep Throughput >> benchmark_result_gpu.txt"], shell=True)
except Exception:
    print("Not found iGPU plugin. It seemed configuration is not correct!")

np.random.seed(19680801)

cpu_performance = []
gpu_performance = []

for txt in ('benchmark_result_cpu.txt', 'benchmark_result_gpu.txt'):
    with open(txt) as f:
        result = f.readlines()
        for x in result:
            element = float(x.split(':')[-1].strip('\n').strip('FPS').strip(' '))
            if txt == 'benchmark_result_cpu.txt':
                cpu_performance.append(element)
            else:
                gpu_performance.append(element)

labels = ["googlenet-v2", "ssdlite_mobilenet_v2", "road-segmentation\n-adas-0001"]

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, cpu_performance, width, label='CPU')
rects2 = ax.bar(x + width/2, gpu_performance, width, label='GPU')

ax.set_ylabel('Throughput (FPS)')
ax.set_title('Benchmark Performance Test Results')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

fig.tight_layout()
plt.show()

subprocess.call(["rm benchmark_result_*"], shell=True)
subprocess.call(["rm rich_test_data.txt"], shell=True)