## Introduction 
- Containers are a form of operating system virtualization. However, containers do not contain operating system images. This makes them more lightweight and portable, with significantly less overhead.

-  A container includes all the necessary executables, binary codes, libraries, and configuration files. Therefore, it can be run anything from a small microservice or software process to a larger application.

- In large-scale application deployments, multiple containers may be deployed as one or more container clusters. Such clusters might be managed by a container orchestrator such as Docker Swarm, Kubernetes.

In a nutshell, using containers could be more streamlined to build, test, and deploy the applications on multiple environments, from a developer’s local laptop to an on-premises data center and even the cloud.

![architecture](./resources/ov_docker_architecture.png)

## Build

First, you will need [git](https://git-scm.com/) to clone this repository to your local computer. If you’re using Linux system like Ubuntu, you can simply do this by:
```
sudo apt-get install git
```

Next, clone the repo:
```
git clone https://github.com/jonathanyeh0723/openvino-with-docker
```

After that, go to the main folder with Dockerfile inside:
```
cd openvino-with-docker/
```

To build the image, run
```
docker build . --build-arg package_url=https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/linux/l_openvino_toolkit_ubuntu20_2023.0.0.10926.b4452d56304_x86_64.tgz -t dockerflamejc/advanipc:latest --no-cache
```

The above commands would build an image from a Dockerfile:<br>
- `docker build .`: This is the default option to look for a Dockerfile at the root of the build context.<br>
- `--build-arg`: Set the build-time variables, in this case is `package_url`. It points to the OpenVINO dev packages directly from [public storage](https://storage.openvinotoolkit.org/repositories/openvino/packages/).<br>
- `-t`: Name and optionally a tag in the name:tag format for easier identify our image.<br>
- `--no-cache`: For sake of hardened microservice security, not to use cache when building the image.

Reference of successful build logs:
```
[+] Building 1194.8s (53/53) FINISHED                                                                                                                         
 => [internal] load build definition from Dockerfile                                                                                                     0.0s
 => => transferring dockerfile: 14.59kB                                                                                                                  0.0s
 => [internal] load .dockerignore                                                                                                                        0.0s
 => => transferring context: 2B                                                                                                                          0.0s
 => [internal] load metadata for docker.io/library/ubuntu:22.04                                                                                          1.6s
 => [auth] library/ubuntu:pull token for registry-1.docker.io                                                                                            0.0s
 => [internal] load build context                                                                                                                        0.1s
 => => transferring context: 22.96MB                                                                                                                     0.1s
 => CACHED [base 1/8] FROM docker.io/library/ubuntu:22.04@sha256:0bced47fffa3361afa981854fcabcd4577cd43cebbb808cea2b1f33a3dd7f508                        0.0s
 => CACHED https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/linux/l_openvino_toolkit_ubuntu20_2023.0.0.10926.b4452d56304_x86_6  1.0s
 => [ov_base  2/34] RUN sed -ri -e 's@^UMASK[[:space:]]+[[:digit:]]+@UMASK 000@g' /etc/login.defs &&  grep -E "^UMASK" /etc/login.defs && useradd -ms /  0.3s
 => [base 2/8] RUN apt-get update &&     apt-get install -y --no-install-recommends curl tzdata ca-certificates &&     rm -rf /var/lib/apt/lists/*      12.2s
 => [ov_base  3/34] RUN mkdir /opt/intel                                                                                                                 0.3s
 => [base 3/8] WORKDIR /tmp/openvino_installer                                                                                                           0.1s 
 => [base 4/8] ADD https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/linux/l_openvino_toolkit_ubuntu20_2023.0.0.10926.b4452d563  0.3s 
 => [base 5/8] RUN useradd -ms /bin/bash -G users openvino                                                                                               0.2s 
 => [base 6/8] RUN tar -xzf "/tmp/openvino_installer"/*.tgz &&     OV_BUILD="$(find . -maxdepth 1 -type d -name "*openvino*" | grep -oP '(?<=_)\d+.\d+.  1.2s 
 => [base 7/8] RUN rm -rf /opt/intel/openvino/.distribution && mkdir /opt/intel/openvino/.distribution &&     touch /opt/intel/openvino/.distribution/d  0.4s 
 => [opencv 1/7] RUN apt-get update;     apt-get install -y --no-install-recommends         git         python3-dev         python3-pip         build-  99.9s 
 => [ov_base  4/34] COPY --from=base /opt/intel/ /opt/intel/                                                                                             0.2s 
 => [ov_base  5/34] WORKDIR /thirdparty                                                                                                                  0.0s 
 => [ov_base  6/34] RUN apt-get update &&     dpkg --get-selections | grep -v deinstall | awk '{print $1}' > base_packages.txt  &&     apt-get install  13.1s
 => [ov_base  7/34] RUN apt-get update && apt-get reinstall -y ca-certificates && rm -rf /var/lib/apt/lists/* && update-ca-certificates                 21.4s
 => [ov_base  8/34] RUN apt-get update &&     apt-get install -y --no-install-recommends ${LGPL_DEPS} &&     ${INTEL_OPENVINO_DIR}/install_dependencie  43.2s
 => [ov_base  9/34] RUN curl -L -O  https://github.com/oneapi-src/oneTBB/releases/download/v2021.9.0/oneapi-tbb-2021.9.0-lin.tgz &&     tar -xzf  oneap  3.2s
 => [ov_base 10/34] WORKDIR /opt/intel/openvino/licensing                                                                                                0.0s
 => [ov_base 11/34] RUN if [ "no" = "no" ]; then         echo "This image doesn't contain source for 3d party components under LGPL/GPL licenses. They   0.3s
 => [ov_base 12/34] RUN python3.10 -m pip install --upgrade pip                                                                                          2.3s
 => [ov_base 13/34] WORKDIR /opt/intel/openvino                                                                                                          0.0s
 => [ov_base 14/34] RUN apt-get update && apt-get install -y --no-install-recommends cmake make git && rm -rf /var/lib/apt/lists/* &&     if [ -z "$O  369.6s
 => [opencv 2/7] RUN python3 -m pip install --no-cache-dir numpy==1.23.1                                                                                12.8s
 => [opencv 3/7] WORKDIR /opt/repo                                                                                                                       0.0s
 => [opencv 4/7] RUN git clone https://github.com/opencv/opencv.git --depth 1 -b 4.7.0                                                                  23.9s
 => [opencv 5/7] WORKDIR /opt/repo/opencv/build                                                                                                          0.0s
 => [opencv 6/7] RUN . "/opt/intel/openvino"/setupvars.sh;     cmake -G Ninja     -D BUILD_INFO_SKIP_EXTRA_MODULES=ON     -D BUILD_EXAMPLES=OFF     -  714.8s
 => [ov_base 15/34] WORKDIR /opt/intel/openvino/licensing                                                                                                0.0s
 => [ov_base 16/34] COPY third-party-programs-docker-dev.txt /opt/intel/openvino/licensing                                                               0.0s
 => [opencv 7/7] WORKDIR /opt/repo/opencv/build/install                                                                                                  0.1s
 => [ov_base 17/34] COPY --from=opencv /opt/repo/opencv/build/install /opt/intel/openvino/extras/opencv                                                  0.1s
 => [ov_base 18/34] RUN  echo "export OpenCV_DIR=/opt/intel/openvino/extras/opencv/cmake" | tee -a "/opt/intel/openvino/extras/opencv/setupvars.sh";     0.2s
 => [ov_base 19/34] RUN apt-get update && apt-get install -y --no-install-recommends opencl-headers ocl-icd-opencl-dev && rm -rf /var/lib/apt/lists/*   10.2s
 => [ov_base 20/34] RUN apt-get update &&     apt-get install libopencv-dev -y                                                                          82.7s
 => [ov_base 21/34] WORKDIR /opt/intel/openvino/samples/cpp                                                                                              0.0s
 => [ov_base 22/34] RUN ./build_samples.sh -b build &&     cp -R build/intel64/Release samples_bin &&     rm -Rf build                                  16.6s
 => [ov_base 23/34] RUN git clone https://github.com/openvinotoolkit/open_model_zoo &&     sed -i '/opencv-python/d' open_model_zoo/demos/common/pytho  73.6s
 => [ov_base 24/34] RUN apt-get update &&     apt-get install -y --no-install-recommends ocl-icd-libopencl1 &&     apt-get clean ;     rm -rf /var/lib/  2.6s
 => [ov_base 25/34] RUN mkdir /tmp/gpu_deps && cd /tmp/gpu_deps &&     curl -L -O https://github.com/intel/compute-runtime/releases/download/23.05.255  18.6s
 => [ov_base 26/34] RUN apt-get update &&     apt-get autoremove -y gfortran &&     rm -rf /var/lib/apt/lists/*                                          9.5s
 => [ov_base 27/34] WORKDIR /opt/intel/openvino                                                                                                          0.0s
 => [ov_base 28/34] RUN apt-get update &&     apt-get install curl vim git -y                                                                           11.6s
 => [ov_base 29/34] RUN python3.10 -m pip install matplotlib                                                                                             6.6s
 => [ov_base 30/34] RUN python3.10 -m pip install pyqt5                                                                                                 22.6s
 => [ov_base 31/34] RUN git clone --recurse-submodules https://github.com/openvinotoolkit/open_model_zoo.git                                            58.7s
 => [ov_base 32/34] WORKDIR /home/openvino                                                                                                               0.0s
 => [ov_base 33/34] COPY lab .                                                                                                                           0.0s
 => exporting to image                                                                                                                                  13.1s
 => => exporting layers                                                                                                                                 13.1s
 => => writing image sha256:c830995236f5160d2e57375575fe541e898cb782fc676c778a7fe6ea340d9fb5                                                             0.0s
 => => naming to docker.io/dockerflamejc/advanipc:latest                        
```

Checking the image built by running `docker image ls`
```
REPOSITORY                TAG           IMAGE ID       CREATED          SIZE
dockerflamejc/advanipc    latest        c830995236f5   27 minutes ago   6.21GB
```

For more information about building and running the image, refer to https://github.com/openvinotoolkit/docker_ci.

## Run

To directly use the latest image built from Docker Hub, run:
```
docker image pull dockerflamejc/advanipc:latest
```

Default run the container with interactive mode:
```
docker run --interactive --tty dockerflamejc/advanipc:latest
```

Note currently only the `CPU` plugin is available, we can check by running `python3` with following command:
```
Python 3.10.6 (main, May 29 2023, 11:10:38) [GCC 11.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from openvino.runtime import Core
>>> core = Core()
>>> core.available_devices
['CPU', 'GNA']
>>> 
```

To use `GPU` accelerator, we need to add the argument `--device /dev/dri:/dev/dri` like this:
```
docker run --interactive --tty --device /dev/dri:/dev/dri dockerflamejc/advanipc:latest
```

Inside the container, running `python3` again for plugins confirmation:
```
Python 3.10.6 (main, May 29 2023, 11:10:38) [GCC 11.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from openvino.runtime import Core
>>> core = Core()
>>> devices = core.available_devices
>>> for device in devices:
...     full_device_name = core.get_property(device, "FULL_DEVICE_NAME")
...     print(device, full_device_name)
... 
CPU 11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz
GNA GNA_SW
GPU Intel(R) Iris(R) Xe Graphics (iGPU)
>>> 
```

Now the `GPU` is ready for inference.

In real-world practical use cases, it's more convenient to add volume for easier data usage and webcam for live streaming. For example:<br>
- Bind the local `/home/<user>/Downloads` directory to `/mnt` the container directory: `--volume ~/Downloads:/mnt`
- Link the USB video camera: `--device /dev/video0:/dev/video0`

Putting all together:
```
docker run --interactive --tty --device /dev/dri:/dev/dri --volume ~/Downloads:/mnt --device /dev/video0:/dev/video0 dockerflamejc/advanipc:latest
```

### Test for more labs
```
lab/
├── 0_devices_check.py
├── 1_classification.py
├── 2_object_detection.py
├── 3_segmentation.py
├── demo_object_detection_camera.sh
├── demo_object_detection_video.sh
├── images
│   ├── empty_road_mapillary.jpg
│   └── neymar.jpg
├── inferenced
│   ├── 1.png
│   ├── 2.png
│   └── 3.png
├── intel
│   └── road-segmentation-adas-0001
│       └── FP16
│           ├── road-segmentation-adas-0001.bin
│           └── road-segmentation-adas-0001.xml
├── labels
│   ├── coco_80cl.txt
│   ├── coco_91cl_bkgr.txt
│   └── imagenet_2015.txt
└── public
    ├── googlenet-v2
    │   └── FP16
    │       ├── googlenet-v2.bin
    │       └── googlenet-v2.xml
    └── ssdlite_mobilenet_v2
        └── FP16
            ├── ssdlite_mobilenet_v2.bin
            └── ssdlite_mobilenet_v2.xml

11 directories, 20 files
```

To play more ambitious labs, you'll have to run the container with verbose arguments:
```
docker run -it --device /dev/dri:/dev/dri --volume ~/Downloads:/mnt -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --rm dockerflamejc/advanipc:latest
```

In addition, you would need to allow the root user access to the X server with `sudo xhost +` command. Input sudo password, you should be able to see the following from the console, if successful:
```
access control disabled, clients can connect from any host
```

Inside the container, go to the `lab` directory.<br>
- Classification: `1_classification.py`<br>
To run classification:
```
python3 1_classification.py
```

![lab_1_result](lab/inferenced/1.png)

- Object Detection: `2_object_detection.py`<br>
To run object detection:
```
python3 2_object_detection.py
```

![lab_2_result](lab/inferenced/2.png)

- Segmentation: `3_segmentation.py`<br>
To run segmentation:
```
python3 3_segmentation.py
```

![lab_3_result](lab/inferenced/3.png)

- Benchmark Performance Test Result Visualization: `4_benchmark_plot.py`<br>
To quickly check the platform plugins AI computing capability we used, run:
```
python3 4_benchmark_plot.py
```
You would need to wait for a couple of minutes for the testing.
```
[ INFO ] Found CPU plugin: 11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz
[ INFO ] Found GNA plugin: GNA_SW
[ INFO ] Found GPU plugin: Intel(R) Iris(R) Xe Graphics (iGPU)
Starting to perform benchmark performance visualization...
```

![lab_4-1_result](lab/plot/benchmark_1_cpu_gpu.png)

In addition, in case of integrated graphic card is not successfully activated (this usually due to the use of unverified Linux Kernel version, missing some Docker run command arguments, or in [WSL](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux) environment not performing post configuration), the plot script also can also handle situation of CPU plugin scenario only.

```
python3 4_benchmark_plot.py
```
In such case, You would **not** see the *GPU plugin found* message reflected from the console.  
```
[ INFO ] Found CPU plugin: 11th Gen Intel(R) Core(TM) i7-1185G7 @ 3.00GHz
[ INFO ] Found GNA plugin: GNA_SW
Starting to perform benchmark performance visualization...
```

![lab_4-2_result](lab/plot/benchmark_2_cpu.png)

- Object Detection: <br>

```
cd lab/

./demo_object_detection_video.sh  # video 

./demo_object_detection_camera.sh # webcam
```

![object_detection_plot](resources/what_was_i_made_for.png)

- YOLOv8 Implementation

Integrated from [OpenVINO Notebooks](https://github.com/openvinotoolkit/openvino_notebooks/tree/main) repo. For detailed information you could further visit [230-yolov8-optimization](https://github.com/openvinotoolkit/openvino_notebooks/tree/main/notebooks/230-yolov8-optimization).<br>

Docker run commands:
```
docker run --interactive --tty --device /dev/dri:/dev/dri --volume /tmp/.X11-unix/:/tmp/.X11-unix --volume /home/cnai/Downloads/:/mnt --env DISPLAY=$DISPLAY --device /dev/video0:/dev/video0 --rm --hostname openvino dockerflamejc/advanipc:latest
```

To run YOLOv8 inference with a video:
```
cd poc
python3 object-detection-yolov8.py --input /opt/intel/openvino_2023/open_model_zoo/demos/object_detection_demo/python/highway_car.mp4
```
![yolov8_video](resources/yolov8_video_demo.png)

To run YOLOv8 real-time inference with webcam:
```
cd poc
python3 object-detection-yolov8.py --input /dev/video0
```

Below is a sample figure for reference.<br>
![yolov8_webcam](resources/yolov8_live_demo.png)

### Benchmark Performance Test
You could also use automation tools [Benchmark Python Tool](https://docs.openvino.ai/2023.1/openvino_inference_engine_tools_benchmark_tool_README.html) to estimate deep learning inference performance on supported devices, by using command `benchmark_app`.

The Python benchmark_app is automatically installed when you install OpenVINO Developer Tools using PyPI.
```
python -m pip install openvino-dev
```

The benchmark_app includes a lot of device-specific options, but the primary usage is as simple as:
```
benchmark_app -m <model> -d <device> 
```

- Test for YOLOv8
```
benchmark_app -m /home/openvino/poc/models/yolov8n_openvino_int8_model/yolov8n_with_preprocess.xml -d AUTO
```

- Test for YOLOv3
```
benchmark_app -m /opt/intel/openvino_2023/open_model_zoo/demos/object_detection_demo/python/yolo-v3-tf/FP16-INT8/yolo-v3-tf.xml -d AUTO
```

- YOLOv3 v.s. YOLOv8 Benchmark Performance
```
python3 5_benchmark_yolo_plot.py
```
![yolo_benchmark](resources/benchmark_yolo.png)


If you run inference for some tasks, while showing the results encountering warning message like below:
```
(python3:87): dbind-WARNING **: 07:06:46.828: Couldn't connect to accessibility bus: Failed to connect to socket /run/user/1000/at-spi/bus_1: No such file or directory
```
you could try the following to suppress the errors:
```
export NO_AT_BRIDGE=1
```

## Add-ons

### Store the image 
Once you have completed validation of this development kit environment, and would like to further deploy to other computer for easier use in the future, you could either push the image to your own Docker Hub repository, or save it as a tar file. 

- **Push to Docker Hub**:

Refer to [docker push](https://docs.docker.com/engine/reference/commandline/push/), once you have created your own account and repository on the Docker Hub, you could simply push the image built to the desired location by running `docker push <dockerhub_account>/<repo_name>:<tag>`

```
docker push dockerflamejc/advanipc:latest
```

You should be able to see the logs like below, if successful:

```
The push refers to repository [docker.io/dockerflamejc/advanipc]
5f70bf18a086: Preparing 
...
2db60c1b32cb: Layer already exists 
dc0585a4b8b7: Layer already exists 
latest: digest: sha256:da119027d0b33a4aa5752a23052b57a3547c2e2da6fcd6bb48ff08bc4dcae66e size: 8493
```

- **Save as a tar file**:
First, check the image built by running `docker image ls dockerflamejc/advanipc:v3`, this would output:
```
REPOSITORY               TAG       IMAGE ID       CREATED      SIZE
dockerflamejc/advanipc   v3        f7103e24dce6   2 days ago   6.21GB
```

And then, refer to [docker save](https://docs.docker.com/engine/reference/commandline/save/) to save the image using the following command:
```
docker save dockerflamejc/advanipc:v3 | gzip > sertek_advanipc_ov.tar.gz
```

Run a simple `ls -lh sertek_advanipc_ov.tar.gz` command for a quick check:
```
-rw-rw-r-- 1 cnai cnai 2.4G  九  25 17:36 sertek_advanipc_ov.tar.gz
```

That's it! Now you have successfully saved the image as a tarball. You could upload to the cloud or copy the a portable USB flash drive.<br>
To load the image, run:
```
docker load -i sertek_advanipc_ov.tar.gz
```

You should be able to see the logs like below, if successful:
```
...
4b56c869dd40: Loading layer   2.56kB/2.56kB
845e284721d7: Loading layer  22.64MB/22.64MB
28ff8a20904e: Loading layer  114.5MB/114.5MB
Loaded image: dockerflamejc/advanipc:v3
```

### Useful tools
If you download or built various images, you want to count the total size of the images so that you can better manage your own space. You could use the python class method `count_images_size()` prepared. Type `python3` in the command line to get into the python prompt:
```
Python 3.10.12 (main, Jun 11 2023, 05:26:28) [GCC 11.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from lab.utils import utils
>>> utils.count_images_size()
Total docker images size downloaded:
42.54GB,  0MB,  13.3kB
>>> 
```

Taking the downloaded images in my computer for instance:
```
REPOSITORY                TAG       IMAGE ID       CREATED        SIZE
dockerflamejc/advanipc    v3        f7103e24dce6   3 days ago     6.21GB
dockerflamejc/advanipc    latest    1f31b8535cc2   3 weeks ago    6.08GB
dockerflamejc/advanipc    v2        1f31b8535cc2   3 weeks ago    6.08GB
advanipc/demo             latest    59ffd52622f0   8 weeks ago    7.3GB
openvino-yolov8           latest    5d9f8f729d2f   2 months ago   11.6GB
sertek_hero_project       latest    572d6a933ec1   3 months ago   2.89GB
ov_2023_ubuntu22_pyt311   latest    020d8c9ba799   3 months ago   2.38GB
hello-world               latest    9c7a54a9a43c   4 months ago   13.3kB
```

## References

- **OpenVINO repo**: https://storage.openvinotoolkit.org/repositories/openvino/packages/
