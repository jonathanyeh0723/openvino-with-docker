## Introduction 
- Containers are a form of operating system virtualization. However, containers do not contain operating system images. This makes them more lightweight and portable, with significantly less overhead.

-  A container includes all the necessary executables, binary codes, libraries, and configuration files. Therefore, it can be run anything from a small microservice or software process to a larger application.

- In large-scale application deployments, multiple containers may be deployed as one or more container clusters. Such clusters might be managed by a container orchestrator such as Docker Swarm, Kubernetes.

In a nutshell, using containers could be more streamlined to build, test, and deploy the applications on multiple environments, from a developer’s local laptop to an on-premises data center and even the cloud.

## Build

Hierarchy
```
.
├── Dockerfile
├── lab
│   ├── 0_devices_check.py
│   ├── 1_classification.py
│   ├── imagenet_2015.txt
│   ├── neymar.jpg
│   └── public
│       └── googlenet-v2
│           └── FP16
│               ├── googlenet-v2.bin
│               └── googlenet-v2.xml
├── LICENSE
├── README.md
└── third-party-programs-docker-dev.txt
```

To build the image, run
```
docker build . --build-arg package_url=https://storage.openvinotoolkit.org/repositories/openvino/packages/2023.0/linux/l_openvino_toolkit_ubuntu20_2023.0.0.10926.b4452d56304_x86_64.tgz -t dockerflamejc/advanipc:v1 --no-cache
```

Reference logs:
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
 => => naming to docker.io/dockerflamejc/advanipc:v1                        
```

Checking the image built by running `docker image ls`
```
REPOSITORY                TAG       IMAGE ID       CREATED          SIZE
dockerflamejc/advanipc    v1        c830995236f5   27 minutes ago   6.03GB
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
docker run --interactive --tty --device /dev/dri:/dev/dri dockerflamejc/advanipc:v1
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
docker run --interactive --tty --device /dev/dri:/dev/dri --volume ~/Downloads:/mnt --device /dev/video0:/dev/video0 dockerflamejc/advanipc:v1
```

### Test for more labs
```
.
├── 0_devices_check.py
├── 1_classification.py
├── 2_object_detection.py
├── coco_91cl_bkgr.txt
├── imagenet_2015.txt
├── neymar.jpg
└── public
    ├── googlenet-v2
    │   └── FP16
    │       ├── googlenet-v2.bin
    │       └── googlenet-v2.xml
    └── ssdlite_mobilenet_v2
        └── FP16
            ├── ssdlite_mobilenet_v2.bin
            └── ssdlite_mobilenet_v2.xml

5 directories, 10 files
```

To play more ambitious labs, you'll have to run the container with verbose arguments:
```
docker run -it --device /dev/dri:/dev/dri --volume ~/Downloads:/mnt -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --rm dockerflamejc/advanipc:latest
```

Inside the container, go to the `lab` directory.<br>
- Classification: `python3 1_classification.py`

- Object Detection: `2_object_detection.py`

If you run inference for object detection tasks, while showing the results encountering warning message like below:
```
(python3:87): dbind-WARNING **: 07:06:46.828: Couldn't connect to accessibility bus: Failed to connect to socket /run/user/1000/at-spi/bus_1: No such file or directory
```
you could try the following to suppress the errors:
```
export NO_AT_BRIDGE=1
```

## References

- **OpenVINO repo**: https://storage.openvinotoolkit.org/repositories/openvino/packages/
